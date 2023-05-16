/** Abstract syntax and values. **/
import stringWidth from 'string-width'
import { isclose } from './numbers.js'

export class Metadata {
  constructor(filename, line_no, start_col, end_col, line) {
    this.filename = filename
    this.line_no = line_no
    this.start_col = start_col
    this.end_col = end_col
    this.line = line

    this.str = null
  }

  toString() {
    if (this.str == null) {
      this.str =
        this.line +
        '\n' +
        ' '.repeat(stringWidth(this.line.slice(0, start_col))) +
        '^'.repeat(stringWidth(line.slice(start_col, end_col)))
    }
    return this.str
  }
}

/* Parser */
export class Literal {
  constructor(metadata, value) {
    this.metadata = metadata
    this.value = value // BigInteger
  }
}
export class FunRef {
  constructor(metadata, rel) {
    this.metadata = metadata
    this.rel = rel // int
  }
}
export class ArgRef {
  constructor(metadata, relA, relF) {
    this.metadata = metadata
    this.relA = relA
    this.relF = relF // int
  }
}
export class FunDef {
  constructor(metadata, body) {
    this.metadata = metadata
    this.body = body
  }
}
export class FunCall {
  constructor(metadata, fun, argv) {
    this.metadata = metadata
    this.fun = fun
    this.argv = argv
  }
}

/* Interpreter */
export class Env {
  constructor(funs, args, utils) {
    this.funs = funs
    this.args = args
    this.utils = utils
  }
}

export class UnsuspectedHangeulError extends Error {
  constructor(err) {
    let message = ''
    for (const metadata of err.metadatas) {
      message += `${metadata.filename} ${metadata.line_no + 1}번줄 `
      message += `${metadata.start_col + 1}~${metadata.end_col + 1}번째 글자:\n`
      message += metadata.toString() + '\n'
    }
    super(message)
    this.err = err
  }
}

/* Values */
function _isPossibleInt(num) {
  return isFinite(num) && isclose(num, Math.floor(num))
}

function _formatFloat(num) {
  if (isFinite(num)) return num.toString()
  if (isNaN(num)) return 'nan'
  return num > 0 ? 'inf' : '-inf'
}

export class IntegerV {
  constructor(value) {
    this.typeName = '정수'
    this.value = value // BigInteger
  }
  toString() {
    return this.value.toString()
  }
  asKey(strict) {
    return this.toString()
  }
}

export class FloatV {
  constructor(value) {
    this.typeName = '실수'
    this.value = value
  }
  toString() {
    const str = _formatFloat(this.value)
    const trailing = _isPossibleInt(this.value) ? '.0' : ''
    return str + trailing
  }
  asKey(strict) {
    return _formatFloat(this.value)
  }
}

export class ComplexV {
  constructor(value) {
    this.typeName = '복소수'
    this.value = value // Complex
  }

  toString() {
    const re = this.value.re
    const im = this.value.im
    const reStr = _formatFloat(re) + (im < 0 ? '' : '+')
    const imStr = im == 1 ? '' : im == -1 ? '-' : _formatFloat(im)
    return (re === 0 ? '' : reStr) + imStr + 'i'
  }

  asKey(strict) {
    return this.value.im ? this.toString() : _formatFloat(this.value.re)
  }
}

export class BooleanV {
  constructor(value) {
    this.typeName = '논릿값'
    this.value = value
  }
  toString() {
    return value.value ? 'True' : 'False'
  }
  asKey(strict) {
    return this.toString()
  }
}

export class ListV {
  constructor(value) {
    this.typeName = '목록'
    this.value = value
  }
  asKey(strict) {
    const children = this.value.map((value) => strict(value).asKey(strict)).join
    return `[${children.join(', ')}]`
  }
}

export class StringV {
  constructor(value) {
    this.typeName = '문자열'
    this.value = value
  }
  toString() {
    return "'" + this.value + "'"
  }
  asKey(strict) {
    return this.toString()
  }
}

export class BytesV {
  constructor(value) {
    this.typeName = '바이트열'
    this.value = value
    this.str = null
  }

  formatByte(c) {
    c = c.toString(16).toUpperCase()
    return '\\x' + ('0' + c).slice(-2)
  }

  toString() {
    if (!this.str) {
      const arr = Array.from(new Uint8Array(this.value))
      const formatted = arr.map(this.formatByte)
      this.str = "b'" + formatted.join('') + "'"
    }
    return this.str
  }

  asKey(strict) {
    return this.toString()
  }
}

export class DictV {
  constructor(value) {
    this.typeName = '사전'
    this.value = value
    this._keys = null
    this._values = null
  }

  keys() {
    if (!this._keys) {
      this._keys = Object.keys(this.value).sort()
    }
    return this._keys
  }

  values() {
    if (!this._values) {
      this._values = this._keys.map((k) => this.value[k])
    }
    return this._values
  }
}

export class IOV {
  constructor(inst, argv, continuation) {
    this.typeName = '드나듦'
    this.inst = inst
    this.argv = argv
    this.continuation = continuation
  }

  asKey(strict) {
    const formatted = this.value.map((value) => value.asKey(strict)).join(', ')
    return `<예외: [${formatted}]>`
  }
}

export class NilV {
  constructor() {
    this.typeName = '빈값'
  }
  toString() {
    return 'Nil'
  }
  asKey(strict) {
    return 'Nil'
  }
}

let FUNCTION_ID_GEN = 0
export class FunctionV {
  constructor(adj = '') {
    this.typeName = '함수'
    this.id = FUNCTION_ID_GEN++
    this.str = '<' + adj + 'Function>'
  }
  toString() {
    return this.str
  }
  asKey(strict) {
    return this.str.replace('>', ' #' + this.id + '>')
  }
}

export class ClosureV extends FunctionV {
  constructor(body, env) {
    super()
    this.body = body
    this.env = env
    this.str = '<Closure created at depth ' + this.env.args.length + '>'
  }

  execute(argv) {
    const newArgs = this.env.args.concat([argv])
    const newEnv = new Env(this.env.funs, newArgs, this.env.utils)
    return new ExprV(this.body, newEnv, null)
  }
}

export class BuiltinModuleV extends FunctionV {
  constructor(module, name) {
    super()
    this.module = module
    this.str = '<Builtin Module ' + name + '>'
  }

  execute(args) {
    return this.module(args)
  }
}

export class ErrorV {
  constructor(metadatas, message, value) {
    this.typeName = '예외'
    this.metadatas = metadatas
    this.message = message
    this.value = value
  }
  asKey(strict) {
    const formatted = this.value.map(strict).join(', ')
    return `<예외: [${formatted}]>`
  }
}

export class ExprV {
  constructor(expr, env, cache) {
    this.expr = expr
    this.env = env
    this.cache = cache
  }
}

export const RealV = [IntegerV, FloatV]
export const NumberV = [ComplexV].concat(RealV)
export const SequenceV = [ListV, StringV, BytesV]
export const CallableV = [FunctionV, BooleanV, DictV, ComplexV, ErrorV].concat(
  SequenceV
)
export const AnyV = [IOV, NilV].concat(CallableV, NumberV)
