/** Abstract syntax and values. **/
import Complex from 'complex.js'
import stringWidth from 'string-width'
import { isclose } from './numbers.js'

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
        ' '.repeat(stringWidth(this.line.slice(0, this.start_col))) +
        '^'.repeat(stringWidth(this.line.slice(this.start_col, this.end_col)))
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
  input(): string | undefined
  print(content: string): void
}
export type LoadUtils = {
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
    super(message)
  }
}

/* Values */
interface ValueBase {
  asKey(strict: StrictFn): string
}

function _isPossibleInt(num: number) {
  return isFinite(num) && isclose(num, Math.floor(num))
}

function _formatFloat(num: number) {
  if (isFinite(num)) return num.toString()
  if (isNaN(num)) return 'nan'
  return num > 0 ? 'inf' : '-inf'
}

export class IntegerV implements ValueBase {
  static typeName = '정수'
  constructor(public value: bigint) {}
  toString() {
    return this.value.toString()
  }
  asKey(strict: StrictFn) {
    return this.toString()
  }
}

export class FloatV implements ValueBase {
  static typeName = '실수'
  constructor(public value: number) {}
  toString() {
    const str = _formatFloat(this.value)
    const trailing = _isPossibleInt(this.value) ? '.0' : ''
    return str + trailing
  }
  asKey(strict: StrictFn) {
    return _formatFloat(this.value)
  }
}

export class ComplexV implements ValueBase {
  static typeName = '복소수'
  constructor(public value: Complex) {}

  toString() {
    const re = this.value.re
    const im = this.value.im
    const reStr = _formatFloat(re) + (im < 0 ? '' : '+')
    const imStr = im == 1 ? '' : im == -1 ? '-' : _formatFloat(im)
    return (re === 0 ? '' : reStr) + imStr + 'i'
  }

  asKey(strict: StrictFn): string {
    return this.value.im ? this.toString() : _formatFloat(this.value.re)
  }
}

export class BooleanV implements ValueBase {
  static typeName = '논릿값'
  constructor(public value: boolean) {}
  toString() {
    return this.value ? 'True' : 'False'
  }
  asKey(strict: StrictFn) {
    return this.toString()
  }
}

export class ListV implements ValueBase {
  static typeName = '목록'
  constructor(public value: Value[]) {}
  asKey(strict: StrictFn): string {
    const children = this.value.map((value) => strict(value).asKey(strict))
    return `[${children.join(', ')}]`
  }
}

export class StringV implements ValueBase {
  static typeName = '문자열'
  constructor(public value: string) {}
  toString() {
    return "'" + this.value + "'"
  }
  asKey(strict: StrictFn): string {
    return this.toString()
  }
}

export class BytesV implements ValueBase {
  static typeName = '바이트열'
  private str?: string
  constructor(public value: ArrayBuffer) {}

  formatByte(c: number) {
    const s = c.toString(16).toUpperCase()
    return '\\x' + ('0' + s).slice(-2)
  }

  toString() {
    if (!this.str) {
      const arr = Array.from(new Uint8Array(this.value))
      const formatted = arr.map(this.formatByte)
      this.str = "b'" + formatted.join('') + "'"
    }
    return this.str
  }

  asKey(strict: StrictFn): string {
    return this.toString()
  }
}

export class DictV implements ValueBase {
  static typeName = '사전'
  private _keys?: string[]
  private _values?: Value[]
  constructor(public value: Record<string, Value>) {}

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

  asKey(strict: StrictFn): string {
    const values = this.values().map((v) => strict(v).asKey(strict))
    const pairs = this.keys().map((k, i) => k + ': ' + values[i])
    return '{' + pairs.join(', ') + '}'
  }
}

export class IOV implements ValueBase {
  static typeName = '드나듦'
  constructor(
    public inst: string,
    public argv: Value[],
    public continuation: (
      doIO: (ioValue: IOV) => NonIOStrictValue,
      ioUtils: IOUtils
    ) => StrictValue
  ) {}

  asKey(strict: StrictFn): string {
    const formatted = this.argv
      .map((value) => strict(value).asKey(strict))
      .join(', ')
    return `<드나듦 ${this.inst}: [${formatted}]>`
  }
}

export class NilV implements ValueBase {
  static typeName = '빈값'
  constructor() {}
  toString() {
    return 'Nil'
  }
  asKey(strict: StrictFn): string {
    return 'Nil'
  }
}

let FUNCTION_ID_GEN = 0
export abstract class FunctionV implements ValueBase {
  static typeName = '함수'
  private id: number
  protected str: string
  constructor(adj = '') {
    this.id = FUNCTION_ID_GEN++
    this.str = '<' + adj + 'Function>'
  }
  toString() {
    return this.str
  }
  asKey(strict: StrictFn): string {
    return this.str.replace('>', ' #' + this.id + '>')
  }
  abstract execute(metadata: Metadata, argv: Value[]): Value
}

export class ClosureV extends FunctionV {
  constructor(public body: AST, public env: Env) {
    super()
    this.str = '<Closure created at depth ' + this.env.args.length + '>'
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
    this.str = '<Builtin Module ' + name + '>'
  }

  execute(metadata: Metadata, argv: Value[]) {
    return this.module(metadata, argv)
  }
}

export class ErrorV implements ValueBase {
  static typeName = '예외'
  constructor(
    public metadatas: Metadata[],
    public message: string,
    public value: StrictValue[]
  ) {}
  asKey(strict: StrictFn) {
    const formatted = this.value.map(strict).join(', ')
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
