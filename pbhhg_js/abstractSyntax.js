/** Abstract syntax and values. **/
import { isclose } from './numbers.js'

/* Parser */
function Literal(value) {
  this.value = value // BigInteger
}
function FunRef(rel) {
  this.rel = rel // int
}
function ArgRef(relA, relF) {
  this.relA = relA
  this.relF = relF // int
}
function FunDef(body) {
  this.body = body
}
function FunCall(fun, argv) {
  this.fun = fun
  this.argv = argv
}

/** Interpreter **/
function Env(funs, args, utils) {
  this.funs = funs
  this.args = args
  this.utils = utils
}

function _isPossibleInt(num) {
  return isFinite(num) && isclose(num, Math.floor(num))
}

function _formatFloat(num) {
  if (isFinite(num)) return num.toString()
  if (isNaN(num)) return 'nan'
  return num > 0 ? 'inf' : '-inf'
}

function IntegerV(value) {
  this.value = value // BigInteger
}
IntegerV.displayName = 'Integer'

class FloatV {
  constructor(value) {
    this.value = value
  }

  toString() {
    const str = _formatFloat(this.value)
    const trailing = _isPossibleInt(this.value) ? '.0' : ''
    return str + trailing
  }
}
FloatV.displayName = 'Float'

class ComplexV {
  constructor(value) {
    this.value = value // Complex
  }

  toString() {
    const re = this.value.re
    const im = this.value.im
    const reStr = _formatFloat(re) + (im < 0 ? '' : '+')
    const imStr = im == 1 ? '' : im == -1 ? '-' : _formatFloat(im)
    return (re === 0 ? '' : reStr) + imStr + 'i'
  }
}
ComplexV.displayName = 'Complex'

function BooleanV(value) {
  this.value = value
}
BooleanV.displayName = 'Boolean'

function ListV(value) {
  this.value = value
}
ListV.displayName = 'List'

function StringV(value) {
  this.value = value
}
StringV.displayName = 'String'

class BytesV {
  constructor(value) {
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
}
BytesV.displayName = 'Bytes'

class DictV {
  constructor(value) {
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
      this._values = this._keys.map(k => this.value[k])
    }
    return this._values
  }
}
DictV.displayName = 'Dict'

function IOV(inst, argv) {
  this.inst = inst
  this.argv = argv
}
IOV.displayName = 'IO'

function NilV() {}
NilV.displayName = 'Nil'

var FUNCTION_ID_GEN = 0
class FunctionV {
  constructor(adj = '') {
    this.id = FUNCTION_ID_GEN++
    this.str = '<' + adj + 'Function #' + this.id + '>'
  }

  toString() {
    return this.str
  }
}
FunctionV.displayName = 'Function'

class ClosureV extends FunctionV {
  constructor(body, env) {
    super()
    this.body = body
    this.env = env
    this.str =
      '<Closure #' + this.id + ' from depth ' + this.env.args.length + '>'
  }

  execute(argv) {
    const newArgs = this.env.args.concat([argv])
    const newEnv = new Env(this.env.funs, newArgs, this.env.utils)
    return new ExprV(this.body, newEnv, null)
  }
}

class BuiltinModuleV extends FunctionV {
  constructor(module, name) {
    super()
    this.module = module
    this.str = '<Builtin Module ' + name + '>'
  }

  execute(args) {
    return this.module(args)
  }
}

function ExprV(expr, env, cache) {
  this.expr = expr
  this.env = env
  this.cache = cache
}

const RealV = [IntegerV, FloatV]
const NumberV = [ComplexV].concat(RealV)
const SequenceV = [ListV, StringV, BytesV]
const CallableV = [FunctionV, BooleanV, DictV, ComplexV].concat(SequenceV)
const AnyV = [IOV, NilV].concat(CallableV, NumberV)

export {
  Literal,
  FunRef,
  FunDef,
  ArgRef,
  FunCall,
  Env,
  IntegerV,
  FloatV,
  ComplexV,
  BooleanV,
  ListV,
  DictV,
  StringV,
  BytesV,
  IOV,
  NilV,
  FunctionV,
  ClosureV,
  BuiltinModuleV,
  ExprV,
  RealV,
  NumberV,
  SequenceV,
  CallableV,
  AnyV
}
