import * as AS from '../abstractSyntax.js'
import {
  isLiteralExpr,
  checkArity,
  checkMinArity,
  checkType
} from '../utils.js'
import { parse, normalize, parseNumber, encodeNumber } from '../parse.js'

import buildBitwise from '../modules/bitwise.js'
import buildByte from '../modules/byte.js'
import buildMath from '../modules/math.js'

var BUILDERS = [buildBitwise, buildByte, buildMath]

var MODULE_REGISTRY = {}
var BUILTIN_MODULE_REGISTRY = new AS.DictV({})

function loadFromPath(path, utils) {
  path = utils.normalizePath(path)
  var module = MODULE_REGISTRY[path]
  if (module) return module
  const program = utils.load(path)
  const exprs = parse(program)
  if (exprs.length !== 1) {
    throw SyntaxError(
      'A module file should contain exactly one object but received: ' +
        exprs.length
    )
  }
  const env = new AS.Env([], [], utils)
  module = new AS.ExprV(exprs[0], env, null)
  MODULE_REGISTRY[path] = module
  return module
}

function loadFromLiteral(literals, utils) {
  const name = literals.map(encodeNumber).join(' ')
  const errMsg = 'No module found under literal sequence ' + name
  // Search builtins
  if (literals[0].eq(5)) {
    var module = BUILTIN_MODULE_REGISTRY
    for (const idx of literals.slice(1)) {
      if (module instanceof AS.DictV) {
        module = module.value[idx.toString()]
      } else throw EvalError(errMsg)
    }
    return module
  }
  const path = searchLiteral(literals, '.', utils)
  if (!path) throw EvalError(errMsg)
  return loadFromPath(path, utils)
}

function searchLiteral(literals, location, utils) {
  if (literals.length === 0) {
    return utils.isFile(location) ? location : null
  }
  const cur = literals[0]
  const sub = literals.slice(1)

  const subentries = utils.listdir(location)
  const found = subentries
    .map(entry => {
      if (!matchesLiteral(entry, cur)) return null
      const searchPath = utils.joinPath(location, entry)
      return searchLiteral(sub, searchPath, utils)
    })
    .filter(x => x)

  if (found.length > 1) {
    throw EvalError('Multiple files matched under ' + dir)
  }
  return found.length ? found[0] : null
}

function matchesLiteral(string, literal) {
  string = normalize(string)
  try {
    return parseNumber(string).eq(literal)
  } catch (e) {
    return false
  }
}

function constructBuiltinModule(data, keys) {
  if (typeof data === 'function') {
    return new AS.BuiltinModuleV(data, keys.join(' '))
  } else if (typeof data === 'number') {
    return new AS.FloatV(data) // ad-hoc
  }
  let newObj = {}
  for (const key in data) {
    newObj[parseNumber(key)] = constructBuiltinModule(
      data[key],
      keys.concat([key])
    )
  }
  return new AS.DictV(newObj)
}

export default function(procFunctional, strict) {
  function _registerBuiltinModule(builder) {
    let module = builder(procFunctional, strict)
    module = constructBuiltinModule(module, ['ㅂ'])
    Object.assign(BUILTIN_MODULE_REGISTRY.value, module.value)
  }
  BUILDERS.forEach(_registerBuiltinModule)

  function _load(argv) {
    checkMinArity(argv, 1)
    var utils = argv[0].env.utils
    if (argv.every(isLiteralExpr)) {
      var literals = argv.map(arg => arg.expr.value)
      return loadFromLiteral(literals, utils)
    }
    checkArity(argv, 1)
    var filepath = strict(argv[0])
    checkType(filepath, AS.StringV)
    return loadFromPath(filepath.value, utils)
  }

  return {
    ㅂ: _load
  }
}
