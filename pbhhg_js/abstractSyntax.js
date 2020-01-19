/** Abstract syntax and values. **/

/* Parser */
function Literal (value) {
  this.value = value // BigInteger
}
function FunRef (rel) {
  this.rel = rel // int
}
function ArgRef (relA, relF) {
  this.relA = relA
  this.relF = relF // int
}
function FunDef (body) {
  this.body = body
}
function FunCall (fun, argv) {
  this.fun = fun
  this.argv = argv
}

/** Interpreter **/
function Env (funs, args, utils) {
  this.funs = funs
  this.args = args
  this.utils = utils
}

function NumberV (value) {
  this.value = value // BigInteger || Number
}
NumberV.displayName = 'Number'

function BooleanV (value) {
  this.value = value
}
BooleanV.displayName = 'Boolean'

function ListV (value) {
  this.value = value
}
ListV.displayName = 'List'

function StringV (value) {
  this.value = value
}
StringV.displayName = 'String'

class BytesV {
  constructor (value) {
    this.value = value
    this.str = null
  }

  formatByte (c) {
    c = c.toString(16).toUpperCase()
    return '\\x' + ('0' + c).slice(-2)
  }

  toString () {
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
  constructor (value) {
    this.value = value
    this._keys = null
    this._values = null
  }

  keys () {
    if (!this._keys) {
      this._keys = Object.keys(this.value).sort()
    }
    return this._keys
  }

  values () {
    if (!this._values) {
      this._values = this._keys.map(k => this.value[k])
    }
    return this._values
  }
}
DictV.displayName = 'Dict'

function IOV (inst, argv) {
  this.inst = inst
  this.argv = argv
}
IOV.displayName = 'IO'

function NilV () {
}
NilV.displayName = 'Nil'

var FUNCTION_ID_GEN = 0
class FunctionV {
  constructor (adj = '') {
    this.id = FUNCTION_ID_GEN++
    this.str = '<' + adj + 'Function #' + this.id + '>'
  }

  toString () {
    return this.str
  }
}
FunctionV.displayName = 'Function'

class ClosureV extends FunctionV {
  constructor (body, env) {
    super()
    this.body = body
    this.env = env
    this.str = ('<Closure #' + this.id + ' from depth ' + this.env.args.length + '>')
  }

  execute (argv) {
    const newArgs = this.env.args.concat([argv])
    const newEnv = new Env(this.env.funs, newArgs, this.env.utils)
    return new ExprV(this.body, newEnv, null)
  }
}

class BuiltinModuleV extends FunctionV {
  constructor (module, name) {
    super()
    this.module = module
    this.str = '<Builtin Module ' + name + '>'
  }

  execute (args) {
    return this.module(args)
  }
}

function ExprV (expr, env, cache) {
  this.expr = expr
  this.env = env
  this.cache = cache
}
const CallableV = [FunctionV, BooleanV, ListV, DictV, StringV, BytesV]
const AnyV = [NumberV, IOV, NilV].concat(CallableV)

export {
  Literal,
  FunRef,
  FunDef,
  ArgRef,
  FunCall,

  Env,
  NumberV,
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
  CallableV,
  AnyV
}
