/* IO & Load utilities for Node.js */
const { Buffer } = require('node:buffer')
const fs = require('node:fs')
const path = require('node:path')
const readline = require('node:readline')

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
    const count = fs.readSync(this.fd, buf, 0, numBytes, this.cursor)
    this.cursor += count
    return buf
  }
  read(numBytes) {
    return this._read(numBytes).buffer
  }
  write(bytes) {
    const buf = Buffer.from(bytes)
    const count = fs.writeSync(this.fd, buf, 0, buf.byteLength, this.cursor)
    return count
  }
  seek(offset, whence) {
    if (whence === 'SEEK_SET') this.cursor = offset
    else if (whence === 'SEEK_CUR') this.cursor += offset
    return this.cursor
  }
  tell() {
    return this.cursor
  }
  truncate(size) {
    if (size == null) size = this.cursor
    fs.ftruncateSync(this.fd, size)
  }
}

const nodeLoadUtils = {
  open(path, flags) {
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

function interactiveSession() {
  console.log('[평범한 한글 해석기. 종료하려면 Ctrl-D를 누르세요.]')

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> ',
  })

  const nodeIOUtils = {
    input: () => {
      return new Promise((resolve, reject) => {
        rl.question('', resolve)
      })
    },
    print: console.log,
  }

  rl.prompt()
  rl.on('line', async (program) => {
    const result = await pbhhg.main(
      '<command-line>',
      program,
      nodeIOUtils,
      nodeLoadUtils
    )
    if (result.length > 1) {
      console.warn(
        `[!] 주의: 한 줄에 ${result.length}개의 객체를 해석했습니다.`
      )
    }
    console.log(result.join(' '))
    rl.prompt()
  })
}

async function run(filename, program, argv) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  })

  const nodeIOUtils = {
    input: () => {
      return new Promise((resolve, reject) => {
        rl.question('', resolve)
      })
    },
    print: console.log,
  }

  const exitCode = await pbhhg.run(
    filename,
    program,
    argv,
    nodeIOUtils,
    nodeLoadUtils
  )
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
  loadUtils: nodeLoadUtils,
}
