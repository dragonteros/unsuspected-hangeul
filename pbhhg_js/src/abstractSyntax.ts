/** Abstract syntax and values. **/
import Complex from 'complex.js'
import EastAsianWidth from 'eastasianwidth'
import { isclose } from './numbers'

export class Metadata {
  private str?: string

  constructor(
    public filename: string,
    public line_no: number,
    public start_col: number,
    public end_col: number,
    public line: string
  ) {}

  toString() {
    if (this.str == null) {
      this.str =
        this.line +
        '\n' +
        ' '.repeat(EastAsianWidth.length(this.line.slice(0, this.start_col))) +
        '^'.repeat(
          EastAsianWidth.length(this.line.slice(this.start_col, this.end_col))
        )
    }
    return this.str
  }
}

/* Parser */
export class Literal {
  constructor(public metadata: Metadata, public value: bigint) {}
}
export class FunRef {
  constructor(public metadata: Metadata, public rel: number) {}
}
export class ArgRef {
  constructor(
    public metadata: Metadata,
    public relA: AST,
    public relF: number
  ) {}
}
export class FunDef {
  constructor(public metadata: Metadata, public body: AST) {}
}
export class FunCall {
  constructor(public metadata: Metadata, public fun: AST, public argv: AST[]) {}
}
export type AST = Literal | FunRef | ArgRef | FunDef | FunCall

/* Interpreter */
export type IOUtils = {
  input(): Promise<string | undefined>
  print(content: string): void
}
export type File = {
  close(): void
  read(numBytes: number): Promise<ArrayBuffer>
  write(bytes: ArrayBuffer): number
  seek(offset: number, whence: 'SEEK_SET' | 'SEEK_CUR'): number
  tell(): number
  truncate(size?: number): number
}
export type LoadUtils = {
  open(path: string | number, flags: 'a' | 'a+' | 'r' | 'r+' | 'w' | 'w+'): File
  load(location: string): string
  isFile(location: string): boolean
  listdir(location: string): string[]
  joinPath(...parts: string[]): string
  normalizePath(path: string): string
}
export class Env {
  constructor(
    public funs: ClosureV[],
    public args: Value[][],
    public utils: LoadUtils
  ) {}
}

export class UnsuspectedHangeulError extends Error {
  constructor(public err: ErrorV) {
    let message = ''
    for (const metadata of err.metadatas) {
      message += `${metadata.filename} ${metadata.line_no + 1}번줄 `
      message += `${metadata.start_col + 1}~${metadata.end_col + 1}번째 글자:\n`
      message += metadata.toString() + '\n'
    }
    super(message + '\n' + err.message)
  }
}

/* Values */
abstract class ValueBase {
  abstract format(strict: StrictFn): string
  asKey(strict: StrictFn): string {
    return this.format(strict)
  }
}

function _isPossibleInt(num: number) {
  return isFinite(num) && isclose(num, Math.floor(num))
}

function _formatFloat(num: number) {
  if (isFinite(num)) return num.toString()
  if (isNaN(num)) return 'nan'
  return num > 0 ? 'inf' : '-inf'
}

export class IntegerV extends ValueBase {
  static typeName = '정수'
  constructor(public value: bigint) {
    super()
  }
  format(strict: StrictFn) {
    return this.value.toString()
  }
}

export class FloatV extends ValueBase {
  static typeName = '실수'
  constructor(public value: number) {
    super()
  }
  format(strict: StrictFn) {
    const str = _formatFloat(this.value)
    const trailing = _isPossibleInt(this.value) ? '.0' : ''
    return str + trailing
  }
  asKey(strict: StrictFn) {
    return _formatFloat(this.value)
  }
}

export class ComplexV extends ValueBase {
  static typeName = '복소수'
  constructor(public value: Complex) {
    super()
  }
  format(strict: StrictFn) {
    const re = this.value.re
    const im = this.value.im
    const reStr = _formatFloat(re) + (im < 0 ? '' : '+')
    const imStr = im == 1 ? '' : im == -1 ? '-' : _formatFloat(im)
    return (re === 0 ? '' : reStr) + imStr + 'i'
  }
  asKey(strict: StrictFn): string {
    return this.value.im ? this.format(strict) : _formatFloat(this.value.re)
  }
}

export class BooleanV extends ValueBase {
  static typeName = '논릿값'
  constructor(public value: boolean) {
    super()
  }
  format(strict: StrictFn) {
    return this.value ? 'True' : 'False'
  }
}

export class ListV extends ValueBase {
  static typeName = '목록'
  constructor(public value: Value[]) {
    super()
  }
  format(strict: StrictFn): string {
    const children = this.value.map((value) => strict(value).format(strict))
    return `[${children.join(', ')}]`
  }
  asKey(strict: StrictFn): string {
    const children = this.value.map((value) => strict(value).asKey(strict))
    return `[${children.join(', ')}]`
  }
}

export class StringV extends ValueBase {
  static typeName = '문자열'
  public value: string[]
  constructor(public str: string) {
    super()
    this.value = Array.from(str)
  }
  format(strict: StrictFn) {
    return "'" + this.str + "'"
  }
}

export class BytesV extends ValueBase {
  static typeName = '바이트열'
  private str?: string
  constructor(public value: ArrayBuffer) {
    super()
  }
  formatByte(c: number) {
    const s = c.toString(16).toUpperCase()
    return '\\x' + ('0' + s).slice(-2)
  }
  format(strict: StrictFn) {
    if (!this.str) {
      const arr = Array.from(new Uint8Array(this.value))
      const formatted = arr.map(this.formatByte)
      this.str = "b'" + formatted.join('') + "'"
    }
    return this.str
  }
}

export class DictV extends ValueBase {
  static typeName = '사전'
  private _keys?: string[]
  private _values?: Value[]
  constructor(public value: Record<string, Value>) {
    super()
  }

  keys() {
    if (!this._keys) {
      this._keys = Object.keys(this.value).sort()
    }
    return this._keys
  }
  values() {
    if (!this._values) {
      this._values = this.keys().map((k) => this.value[k])
    }
    return this._values
  }

  format(strict: StrictFn): string {
    const values = this.values().map((v) => strict(v).format(strict))
    const pairs = this.keys().map((k, i) => k + ': ' + values[i])
    return '{' + pairs.join(', ') + '}'
  }
  asKey(strict: StrictFn): string {
    const values = this.values().map((v) => strict(v).asKey(strict))
    const pairs = this.keys().map((k, i) => k + ': ' + values[i])
    return '{' + pairs.join(', ') + '}'
  }
}

export class IOV extends ValueBase {
  static typeName = '드나듦'

  constructor(
    public inst: string,
    public argv: Value[],
    public continuation: (
      doIO: (ioValue: IOV) => Promise<NonIOStrictValue>,
      ioUtils: IOUtils
    ) => Promise<StrictValue>
  ) {
    super()
  }

  format(strict: StrictFn): string {
    const formatted = this.argv
      .map((value) => strict(value).format(strict))
      .join(', ')
    return `<드나듦 ${this.inst}: [${formatted}]>`
  }
  asKey(strict: StrictFn): string {
    const formatted = this.argv
      .map((value) => strict(value).asKey(strict))
      .join(', ')
    return `<드나듦 ${this.inst}: [${formatted}]>`
  }
}

export class NilV extends ValueBase {
  static typeName = '빈값'
  constructor() {
    super()
  }
  format(strict: StrictFn): string {
    return 'Nil'
  }
}

let FUNCTION_ID_GEN = 0
export abstract class FunctionV extends ValueBase {
  static typeName = '함수'
  private id: number
  protected str: string
  constructor(adj = '') {
    super()
    this.id = FUNCTION_ID_GEN++
    this.str = '<' + adj + '함수>'
  }
  format(strict: StrictFn) {
    return this.str
  }
  asKey(strict: StrictFn): string {
    return this.str.replace('>', ' #' + this.id + '>')
  }
  abstract execute(metadata: Metadata, argv: Value[]): Value
}

export class ClosureV extends FunctionV {
  constructor(public body: AST, public env: Env) {
    super(`깊이 ${env.args.length}에서 생성된 `)
  }

  execute(metadata: Metadata, argv: Value[]) {
    const newArgs = this.env.args.concat([argv])
    const newEnv = new Env(this.env.funs, newArgs, this.env.utils)
    return new ExprV(this.body, newEnv, null)
  }
}

export class BuiltinModuleV extends FunctionV {
  constructor(public module: Evaluation, name: string) {
    super()
    this.str = '<기본 제공 모듈 ' + name + '>'
  }

  execute(metadata: Metadata, argv: Value[]) {
    return this.module(metadata, argv)
  }
}

export class ErrorV extends ValueBase {
  static typeName = '예외'
  constructor(
    public metadatas: Metadata[],
    public message: string,
    public value: StrictValue[]
  ) {
    super()
  }
  format(strict: StrictFn): string {
    const formatted = this.value.map((v) => v.format(strict)).join(', ')
    return `<예외: [${formatted}]>`
  }
  asKey(strict: StrictFn): string {
    const formatted = this.value.map((v) => v.asKey(strict)).join(', ')
    return `<예외: [${formatted}]>`
  }
}

export class ExprV {
  constructor(
    public expr: AST,
    public env: Env,
    public cache: StrictValue | UnsuspectedHangeulError | null
  ) {}
}

export const RealV = [IntegerV, FloatV] as const
export const NumberV = [...RealV, ComplexV] as const
export const SequenceV = [ListV, StringV, BytesV] as const
export const CallableV = [
  FunctionV,
  BooleanV,
  DictV,
  ComplexV,
  ErrorV,
  ...SequenceV,
] as const
export const AnyV = [...NumberV, ...CallableV, IOV, NilV] as const

export type StrictValueType = (typeof AnyV)[number]

export type NonIOStrictValue =
  | IntegerV
  | FloatV
  | ComplexV
  | ListV
  | StringV
  | BytesV
  | BooleanV
  | DictV
  | ErrorV
  | FunctionV
  | NilV
export type StrictValue = NonIOStrictValue | IOV
export type Value = StrictValue | ExprV

export type ProcFunctionalFn = (
  metadata: Metadata,
  fun: Value,
  generalCallable?: boolean
) => Evaluation
export type StrictFn = (value: Value) => StrictValue
export type Evaluation = (metadata: Metadata, args: Value[]) => Value
