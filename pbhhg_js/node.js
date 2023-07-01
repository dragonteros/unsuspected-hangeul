/* IO & Load utilities for Node.js */
import { Buffer } from 'node:buffer'
import fs from 'node:fs'
import path from 'node:path'
import { StringDecoder } from 'node:string_decoder'

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
      return this._read(stats.size - (this.cursor ?? 0))
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
      fs.readSync(this.fd, buf, 0, numBytes, null)
      this.cursor = undefined
    }
    return buf
  }
  async read(numBytes) {
    return new Uint8Array(this._read(numBytes)).buffer
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
      this.cursor = undefined
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
    if (size == null) throw Error('이 파일은 읽고 쓰는 위치를 알 수 없습니다.')
    fs.ftruncateSync(this.fd, size)
    return size
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
export class BufferedReader extends DummyFile {
  constructor() {
    super()
    this.buffer = null
    this.cursor = 0
  }
  async _fillBuffer() {
    if (this.buffer != null && this.cursor < this.buffer.length) return
    this.buffer = null
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
      this.cursor += bytesToRead
    }
    return new Uint8Array(Buffer.concat(buffers)).buffer
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
export class BufferedWriter extends DummyFile {
  write(bytes) {
    process.stdout.write(Buffer.from(bytes))
    return bytes.byteLength
  }
  writeLine(line) {
    process.stdout.write(line + '\n')
  }
}

export function getLoadUtils(stdin, stdout) {
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
