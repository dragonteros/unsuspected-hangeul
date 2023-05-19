import * as AS from '../abstractSyntax.js'
import * as E from '../error.js'
import { encodeNumber, normalize, parse, parseNumber } from '../parse.js'
import {
  checkArity,
  checkMinArity,
  checkType,
  isLiteralExpr,
} from '../utils.js'

import buildBitwise from '../modules/bitwise.js'
import buildByte from '../modules/byte.js'
import buildMath from '../modules/math.js'

interface ModuleTable
  extends Record<string, number | AS.Evaluation | ModuleTable> {}
const BUILDERS: ((
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
) => ModuleTable)[] = [buildBitwise, buildByte, buildMath]

var MODULE_REGISTRY: Record<string, AS.Value> = {}
var BUILTIN_MODULE_REGISTRY = new AS.DictV({})

function loadFromPath(path: string, utils: AS.LoadUtils) {
  path = utils.normalizePath(path)
  var module = MODULE_REGISTRY[path]
  if (module) return module
  const program = utils.load(path)
  const exprs = parse(path, program)
  if (exprs.length !== 1) {
    throw new E.UnsuspectedHangeulValueError(
      exprs[0].metadata,
      `모듈에는 표현식이 하나만 있어야 하는데 ${exprs.length}개가 있습니다.`
    )
  }
  const env = new AS.Env([], [], utils)
  module = new AS.ExprV(exprs[0], env, null)
  MODULE_REGISTRY[path] = module
  return module
}

function loadFromLiteral(
  metadata: AS.Metadata,
  literals: bigint[],
  utils: AS.LoadUtils
) {
  const name = literals.map(encodeNumber).join(' ')
  const errMsg = `정수 리터럴열 ${name}에 맞는 모듈을 찾지 못했습니다.`
  // Search builtins
  if (literals[0] === 5n) {
    var module: AS.Value = BUILTIN_MODULE_REGISTRY
    for (const idx of literals.slice(1)) {
      if (module instanceof AS.DictV) {
        module = module.value[idx.toString()]
      } else throw new E.UnsuspectedHangeulNotFoundError(metadata, errMsg)
    }
    return module
  }
  const path = searchLiteral(metadata, literals, '.', utils)
  if (!path) throw new E.UnsuspectedHangeulNotFoundError(metadata, errMsg)
  return loadFromPath(path, utils)
}

function searchLiteral(
  metadata: AS.Metadata,
  literals: bigint[],
  location: string,
  utils: AS.LoadUtils
): string | null {
  if (literals.length === 0) {
    return utils.isFile(location) ? location : null
  }
  const cur = literals[0]
  const sub = literals.slice(1)

  const subentries = utils.listdir(location)
  const found = subentries
    .map((entry) => {
      if (!matchesLiteral(entry, cur)) return null
      const searchPath = utils.joinPath(location, entry)
      return searchLiteral(metadata, sub, searchPath, utils)
    })
    .filter((x) => x)

  if (found.length > 1) {
    throw new E.UnsuspectedHangeulImportError(
      metadata,
      `${location}에 정수 리터럴열 ${literals}에 맞는 모듈이 ` +
        `${found.length}개 있어 모호합니다.`
    )
  }
  return found.length ? found[0] : null
}

function matchesLiteral(string: string, literal: bigint) {
  string = normalize(string).join(' ').trim()
  try {
    return parseNumber(string) === literal
  } catch (e) {
    return false
  }
}

type LeafData = number | AS.Evaluation | ModuleData
interface ModuleData extends Record<string, LeafData> {}
function constructBuiltinModule(data: LeafData, keys: string[]) {
  if (typeof data === 'function') {
    return new AS.BuiltinModuleV(data, keys.join(' '))
  } else if (typeof data === 'number') {
    return new AS.FloatV(data) // ad-hoc
  }
  return constructBuiltinModules(data, keys)
}
function constructBuiltinModules(data: ModuleData, keys: string[]) {
  let newObj: Record<string, AS.Value> = {}
  for (const key in data) {
    newObj[parseNumber(key).toString()] = constructBuiltinModule(
      data[key],
      keys.concat([key])
    )
  }
  return new AS.DictV(newObj)
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _registerBuiltinModule(
    builder: (
      procFunctional: AS.ProcFunctionalFn,
      strict: AS.StrictFn,
      loadUtils: AS.LoadUtils
    ) => ModuleTable
  ) {
    let module = builder(procFunctional, strict, loadUtils)
    const _module = constructBuiltinModules(module, ['ㅂ'])
    Object.assign(BUILTIN_MODULE_REGISTRY.value, _module.value)
  }
  BUILDERS.forEach(_registerBuiltinModule)

  function _load(metadata: AS.Metadata, argv: AS.Value[]) {
    checkMinArity(metadata, argv, 1)
    if (argv.every(isLiteralExpr)) {
      var literals = argv.map((arg) => arg.expr.value)
      return loadFromLiteral(metadata, literals, loadUtils)
    }
    checkArity(metadata, argv, 1)
    const [filepath] = checkType(metadata, [strict(argv[0])], [AS.StringV])
    return loadFromPath(filepath.value, loadUtils)
  }

  return {
    ㅂ: _load,
  }
}
