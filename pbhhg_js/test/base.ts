import assert from 'node:assert'
import { StringDecoder } from 'node:string_decoder'

import { loadUtils as noadLoadUtils } from '../cli'
import { File, IOUtils, LoadUtils } from '../src/abstractSyntax'
import { main } from '../src/main'

class DummyFile implements File {
  close(): void {
    throw 'NotImplemented'
  }
  read(numBytes: number): ArrayBuffer {
    throw 'NotImplemented'
  }
  write(bytes: ArrayBuffer): number {
    throw 'NotImplemented'
  }
  seek(offset: number, whence: 'SEEK_SET' | 'SEEK_CUR'): number {
    throw 'NotImplemented'
  }
  tell(): number {
    throw 'NotImplemented'
  }
  truncate(size?: number): number {
    throw 'NotImplemented'
  }
}
class BufferedReader extends DummyFile {
  private cursor = 0
  constructor(private content: string = '') {
    super()
  }
  read(numBytes: number): ArrayBuffer {
    const encoder = new TextEncoder()

    const anchor = this.cursor
    let numBytesRead = 0
    while (this.cursor < this.content.length && numBytesRead < numBytes) {
      const delta = this.content[this.cursor]
      const numBytesDelta = encoder.encode(delta).byteLength
      if (numBytesRead + numBytesDelta > numBytes) break

      this.cursor += 1
      numBytesRead += numBytesDelta
    }
    const content = this.content.slice(anchor, this.cursor)
    return encoder.encode(content).buffer
  }
  readLine(): string | undefined {
    if (this.cursor >= this.content.length) return

    let sepIdx = this.content.indexOf('\n', this.cursor)
    if (sepIdx === -1) sepIdx = this.content.length
    const line = this.content.slice(this.cursor, sepIdx)
    this.cursor = sepIdx + 1
    return line
  }
}
class BufferedWriter extends DummyFile {
  private buffer: string[]
  private decoder: StringDecoder
  constructor() {
    super()
    this.buffer = []
    this.decoder = new StringDecoder('utf-8')
  }
  write(bytes: ArrayBuffer): number {
    this.buffer.push(this.decoder.write(Buffer.from(bytes)))
    return bytes.byteLength
  }
  writeLine(line: string) {
    this.buffer.push(line + '\n')
  }
  getContent(): string {
    this.buffer.push(this.decoder.end())
    return this.buffer.join('')
  }
}

function wrapLoadUtils(
  stdin: BufferedReader,
  stdout: BufferedWriter
): LoadUtils {
  return {
    ...noadLoadUtils,
    open(
      path: string | number,
      flags: 'a' | 'a+' | 'r' | 'r+' | 'w' | 'w+'
    ): File {
      if (path === 0 && flags === 'r') return stdin
      if (path === 1 && flags === 'w') return stdout
      return noadLoadUtils.open(path, flags)
    },
  }
}

export async function test(
  program: string,
  value: string,
  input?: string,
  output?: string
) {
  const stdin = new BufferedReader(input)
  const stdout = new BufferedWriter()

  const ioUtils: IOUtils = {
    input: () => Promise.resolve(stdin.readLine()),
    print: (s: string) => stdout.writeLine(s),
  }
  const loadUtils = wrapLoadUtils(stdin, stdout)
  const result = await main('<test>', program, ioUtils, loadUtils, false)
  assert.deepStrictEqual(result, [value])
  if (output) {
    const printed = stdout.getContent()
    assert.strictEqual(printed.trim(), output.trim())
  }
}
