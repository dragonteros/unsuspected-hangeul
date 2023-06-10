/* IO & Load utilities for Node.js */
const { Buffer } = require('node:buffer')
const fs = require('node:fs')
const path = require('node:path')
const readline = require('node:readline')
const { StringDecoder } = require('node:string_decoder')

const pbhhg = require('./dist/pbhhg')

class NodeFile {
  BUFFER_SIZE = 8196
  constructor(fd) {
    this.fd = fd
    this.cursor = 0
  }
  close() {
    fs.closeSync(this.fd)
  }
  _readAll() {
    try {
      const stats = fs.fstatSync(this.fd)
      return this._read(stats.size - this.cursor)
    } catch (error) {
      const buffers = []
      while (true) {
        const buf = this._read(this.BUFFER_SIZE)
        if (buf.byteLength === 0) break
        buffers.push(buf)
      }
      return Buffer.concat(buffers)
    }
  }
  _read(numBytes) {
    if (numBytes < 0) return this._readAll()
    const buf = Buffer.alloc(numBytes)
    try {
      if (this.cursor == null) throw null
      const count = fs.readSync(this.fd, buf, 0, numBytes, this.cursor)
      this.cursor += count
    } catch (error) {
      fs.readSync(this.fd, buf, 0, numBytes)
      this.cursor = null
    }
    return buf
  }
  read(numBytes) {
    return this._read(numBytes).buffer
  }
  write(bytes) {
    const buf = Buffer.from(bytes)
    let count = 0
    try {
      if (this.cursor == null) throw null
      count = fs.writeSync(this.fd, buf, 0, buf.byteLength, this.cursor)
      this.cursor += count
    } catch (error) {
      count = fs.writeSync(this.fd, buf, 0, buf.byteLength)
      this.cursor = null
    }
    return count
  }
  seek(offset, whence) {
    if (this.cursor == null)
      throw Error('이 파일은 읽고 쓰는 위치를 움직일 수 없습니다.')
    if (whence === 'SEEK_SET') this.cursor = offset
    else if (whence === 'SEEK_CUR') this.cursor += offset
    return this.cursor
  }
  tell() {
    if (this.cursor == null)
      throw Error('이 파일은 읽고 쓰는 위치를 알 수 없습니다.')
    return this.cursor
  }
  truncate(size) {
    if (size == null) size = this.cursor
    fs.ftruncateSync(this.fd, size)
  }
}

class DummyFile {
  close() {
    throw 'NotImplemented'
  }
  read(numBytes) {
    throw 'NotImplemented'
  }
  write(bytes) {
    throw 'NotImplemented'
  }
  seek(offset, whence) {
    throw 'NotImplemented'
  }
  tell() {
    throw 'NotImplemented'
  }
  truncate(size) {
    throw 'NotImplemented'
  }
}
class BufferedReader extends DummyFile {
  constructor() {
    super()
    this.buffer = null
    this.cursor = 0
  }
  async _fillBuffer() {
    if (this.buffer != null) return
    const response = await process.stdin.iterator().next()
    if (response.done) return
    this.buffer = response.value
    this.cursor = 0
  }
  async read(numBytes) {
    const buffers = []
    while (numBytes > 0) {
      await this._fillBuffer()
      if (this.buffer == null) break
      const bytesToRead = Math.min(numBytes, this.buffer.length - this.cursor)
      buffers.push(this.buffer.slice(this.cursor, this.cursor + bytesToRead))
      numBytes -= bytesToRead
    }
    return Buffer.concat(buffers).buffer
  }
  async readLine() {
    const decoder = new StringDecoder()
    const strings = []
    while (true) {
      await this._fillBuffer()
      if (this.buffer == null) break

      const newlineIdx = this.buffer.indexOf('\n', this.cursor)
      if (newlineIdx !== -1) {
        strings.push(decoder.write(this.buffer.slice(this.cursor, newlineIdx)))
        this.cursor = newlineIdx + 1
        break
      }

      strings.push(decoder.write(this.buffer.slice(this.cursor)))
      this.buffer = null
    }

    strings.push(decoder.end())
    let result = strings.join('')
    if (this.buffer == null && result === '') return undefined // EOF
    if (result.endsWith('\r')) result = result.slice(0, -1)
    return result
  }
}
class BufferedWriter extends DummyFile {
  write(bytes) {
    process.stdout.write(Buffer.from(bytes))
    return bytes.byteLength
  }
  writeLine(line) {
    process.stdout.write(line + '\n')
  }
}

function getLoadUtils(stdin, stdout) {
  return {
    open(path, flags) {
      if (path === 0 && flags === 'r') return stdin
      if (path === 1 && flags === 'w') return stdout
      const fd = typeof path === 'number' ? path : fs.openSync(path, flags)
      return new NodeFile(fd)
    },
    load(location) {
      return fs.readFileSync(location, 'utf8')
    },
    isFile(location) {
      return fs.statSync(location).isFile()
    },
    listdir: fs.readdirSync,
    joinPath: path.join,
    normalizePath: path.normalize,
  }
}

async function interactiveSession() {
  console.log('[평범한 한글 해석기. 종료하려면 Ctrl-C를 누르세요.]')

  const stdin = new BufferedReader()
  const stdout = new BufferedWriter()
  const ioUtils = {
    input: () => stdin.readLine(),
    print: (s) => stdout.writeLine(s),
  }
  const loadUtils = getLoadUtils(stdin, stdout)

  while (true) {
    process.stdout.write('> ')
    const program = await stdin.readLine()
    if (program == null) return

    const result = await pbhhg.main(
      '<command-line>',
      program,
      ioUtils,
      loadUtils
    )
    if (result.length > 1) {
      console.warn(
        `[!] 주의: 한 줄에 ${result.length}개의 객체를 해석했습니다.`
      )
    }
    console.log(result.join(' '))
  }
}

async function run(filename, program, argv) {
  const stdin = new BufferedReader()
  const stdout = new BufferedWriter()
  const ioUtils = {
    input: () => stdin.readLine(),
    print: (s) => stdout.writeLine(s),
  }
  const loadUtils = getLoadUtils(stdin, stdout)

  const exitCode = await pbhhg.run(filename, program, argv, ioUtils, loadUtils)
  process.exit(exitCode)
}

if (require.main === module) {
  const USAGE = `난해한 프로그래밍 언어 '평범한 한글'의 해석기입니다.

사용법
  node ${process.argv[1]} [-h | <파일> [<인수> ...] | -c <본문> [<인수> ...]]

사용례
  node ${process.argv[1]} -h
  node ${process.argv[1]} --help
    사용법을 안내합니다.

  node ${process.argv[1]} <파일>
  node ${process.argv[1]} <파일> <인수0>
  node ${process.argv[1]} <파일> <인수0> <인수1>
  ...
    <파일>에 있는 '평범한 한글' 함수 모듈을 제공한 인수와 함께 실행합니다.
    실행 결과는 종료 코드가 됩니다.

  node ${process.argv[1]} -c <본문>
  node ${process.argv[1]} -c <본문> <인수0>
  node ${process.argv[1]} -c <본문> <인수0> <인수1>
  ...
    '평범한 한글' 함수 <본문>을 제공한 인수와 함께 실행합니다.
    실행 결과는 종료 코드가 됩니다.`

  const argv = process.argv.slice(2)
  if (argv.length === 0) {
    interactiveSession()
  } else if (argv[0] === '-h' || argv[0] === '--help') {
    console.log(USAGE)
  } else if (argv[0] === '-c') {
    if (argv.length === 1) {
      console.error(
        `다음 명령으로 사용법을 확인하십시오.\n  node ${process.argv[1]} --help`
      )
      process.exit(1)
    }
    run('<command>', argv[1], argv.slice(2))
  } else {
    let fd = argv[0]
    if (fd === '-') fd = 0
    const program = fs.readFileSync(fd, { encoding: 'utf-8' })
    run(argv[0], program, argv.slice(1))
  }
}

module.exports = {
  getLoadUtils,
}
