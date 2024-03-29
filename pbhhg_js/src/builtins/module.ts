import * as AS from '../abstractSyntax'
import * as E from '../error'
import { encodeNumber, normalize, parse, parseNumber } from '../parse'
import { checkArity, checkMinArity, checkType, isLiteralExpr } from '../utils'

import buildBitwise from '../modules/bitwise'
import buildByte from '../modules/byte'
import buildMath from '../modules/math'

interface ModuleTable
  extends Record<string, number | AS.Evaluation | ModuleTable> {}
const BUILDERS: ModuleTable[] = [buildBitwise, buildByte, buildMath]

var MODULE_REGISTRY: Record<string, AS.Value> = {}
var BUILTIN_MODULE_REGISTRY = new AS.DictV({})

function loadFromPath(context: AS.EvalContextBase, path: string) {
  path = context.loadUtils.normalizePath(path)
  var module = MODULE_REGISTRY[path]
  if (module) return module
  const program = context.loadUtils.load(path)
  const exprs = parse(path, program)
  if (exprs.length !== 1) {
    throw new E.UnsuspectedHangeulValueError(
      exprs[0].metadata,
      `모듈에는 표현식이 하나만 있어야 하는데 ${exprs.length}개가 있습니다.`
    )
  }
  const env = new AS.Env([], [])
  module = new AS.ExprV(exprs[0], env, null)
  MODULE_REGISTRY[path] = module
  return module
}

function loadFromLiteral(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  literals: bigint[]
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
  const path = searchLiteral(context, metadata, literals, '.')
  if (!path) throw new E.UnsuspectedHangeulNotFoundError(metadata, errMsg)
  return loadFromPath(context, path)
}

function searchLiteral(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  literals: bigint[],
  location: string
): string | null {
  if (literals.length === 0) {
    return context.loadUtils.isFile(location) ? location : null
  }
  const cur = literals[0]
  const sub = literals.slice(1)

  const subentries = context.loadUtils.listdir(location)
  const found = subentries
    .map((entry) => {
      if (!matchesLiteral(entry, cur)) return null
      const searchPath = context.loadUtils.joinPath(location, entry)
      return searchLiteral(context, metadata, sub, searchPath)
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

function _registerBuiltinModule(module: ModuleTable) {
  const _module = constructBuiltinModules(module, ['ㅂ'])
  Object.assign(BUILTIN_MODULE_REGISTRY.value, _module.value)
}
BUILDERS.forEach(_registerBuiltinModule)

function _load(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkMinArity(metadata, argv, 1)
  if (argv.every(isLiteralExpr)) {
    var literals = argv.map((arg) => arg.expr.value)
    return loadFromLiteral(context, metadata, literals)
  }
  checkArity(metadata, argv, 1)
  const [filepath] = checkType(
    metadata,
    [context.strict(argv[0])],
    [AS.StringV]
  )
  return loadFromPath(context, filepath.str)
}

export default {
  ㅂ: _load,
}
