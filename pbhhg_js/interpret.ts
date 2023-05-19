import * as AS from './abstractSyntax.js'
import * as E from './error.js'
import { encodeNumber } from './parse.js'
import { checkArity, checkType, getLength, isLiteralExpr } from './utils.js'

import buildArithmetics from './builtins/arithmetics.js'
import buildConstructors from './builtins/constructors.js'
import buildFunctional from './builtins/functional.js'
import buildIO from './builtins/io.js'
import buildLogic from './builtins/logic.js'
import buildModule from './builtins/module.js'
import buildSequence from './builtins/sequence.js'
import buildString from './builtins/string.js'

type BuiltinFunctionMap = Record<string, AS.Evaluation>
const BUILTINS: BuiltinFunctionMap = {}
let isBuilt = false

const _builders = [
  buildArithmetics,
  buildConstructors,
  buildFunctional,
  buildIO,
  buildLogic,
  buildModule,
  buildSequence,
  buildString,
] as const
function initBuiltins(loadUtils: AS.LoadUtils) {
  if (isBuilt) return
  for (const builder of _builders) {
    Object.assign(BUILTINS, builder(procFunctional, strict, loadUtils))
  }
  isBuilt = true
}

/**
 * Finds the built-in function corresponding to the builtin function id.
 * @param metadata Caller's metadata.
 * @param id Built-in function ID.
 * @returns corresponding function that takes arguments.
 */
function findBuiltin(
  metadata: AS.Metadata,
  id: number,
  loadUtils: AS.LoadUtils
) {
  initBuiltins(loadUtils)
  const inst = encodeNumber(id)
  const builtinFun = BUILTINS[inst]
  if (builtinFun) return builtinFun
  throw new E.UnsuspectedHangeulNotFoundError(
    metadata,
    `${inst}라는 이름의 기본 제공 함수를 찾지 못했습니다.`
  )
}

/** Forces strict evaluation of the value */
export function strict(value: AS.Value): AS.StrictValue {
  if (value instanceof AS.ExprV) {
    if (value.cache) {
      if (value.cache instanceof AS.UnsuspectedHangeulError) {
        throw value.cache
      }
      return value.cache
    }
    try {
      value.cache = strict(interpret(value.expr, value.env))
      return value.cache
    } catch (error) {
      if (error instanceof AS.UnsuspectedHangeulError) {
        value.cache = error
      }
      throw error
    }
  }
  return value
}

function _accessArray<T>(arr: T[], rel: number): T | undefined {
  if (rel >= 0) return arr[rel]
  else return arr[arr.length + rel]
}
function _accessString(s: string, rel: number): string | undefined {
  if (rel >= 0) return s[rel]
  else return s[s.length + rel]
}
function _accessBuffer(buf: ArrayBuffer, rel: number): ArrayBuffer | undefined {
  if (rel >= buf.byteLength) return undefined
  if (rel < 0) rel += buf.byteLength
  return buf.slice(rel, rel + 1)
}

/** Evaluates the expression in given environment and returns a value */
export function interpret(expr: AS.AST, env: AS.Env) {
  if (expr instanceof AS.Literal) {
    return new AS.IntegerV(expr.value)
  } else if (expr instanceof AS.FunRef) {
    const fun = _accessArray(env.funs, -expr.rel - 1)
    if (fun == null) {
      throw new E.UnsuspectedHangeulOutOfRangeError(
        expr.metadata,
        '함수 참조의 범위를 벗어났습니다.'
      )
    }
    return fun
  } else if (expr instanceof AS.ArgRef) {
    if (env.funs.length !== env.args.length) {
      throw Error(
        'Assertion Error: Environment has ' +
          env.funs.length +
          ' funs and ' +
          env.args.length +
          ' args.'
      )
    }
    const args = _accessArray(env.args, -expr.relF - 1)
    if (args == null) {
      throw new E.UnsuspectedHangeulOutOfRangeError(
        expr.metadata,
        '존재하지 않는 함수에 대한 인수 참조를 시도했습니다.'
      )
    }
    const relA = strict(interpret(expr.relA, env))
    const [_relA] = checkType(expr.metadata, [relA], [AS.IntegerV])
    const relAValue = _relA.value
    if (relAValue < 0 || relAValue > args.length) {
      throw new E.UnsuspectedHangeulOutOfRangeError(
        expr.metadata,
        `${relAValue}번째 인수를 참조하는데 ${args.length}개의 인수만 받았습니다.`
      )
    } else return args[Number(relAValue)]
  } else if (expr instanceof AS.FunDef) {
    var newFuns = env.funs.slice()
    var newEnv = new AS.Env(newFuns, env.args, env.utils)
    var closure = new AS.ClosureV(expr.body, newEnv)
    newEnv.funs.push(closure)
    return closure
  } else if (expr instanceof AS.FunCall) {
    var fun = new AS.ExprV(expr.fun, env, null)
    var argv = expr.argv.map(function (arg) {
      return new AS.ExprV(arg, env, null)
    })
    var recipe = procFunctional(expr.metadata, fun, true)
    return recipe(expr.metadata, argv)
  }
  throw Error('Unexpected expression: ' + expr)
}

/**
 * Converts function-like values into functions.
 * @param metadata Caller's metadata.
 * @param fun A maybe-Expr value that may correspond to a function.
 * @param allow A list of types that are allowed for execution.
 * @returns A recipe function that receives argument list and returns the value.
 */
export function procFunctional(
  metadata: AS.Metadata,
  fun: AS.Value,
  generalCallable: boolean = false
): AS.Evaluation {
  if (isLiteralExpr(fun))
    return findBuiltin(metadata, Number(fun.expr.value), fun.env.utils)

  const allow = generalCallable ? AS.CallableV : [AS.FunctionV]
  const [_fun] = checkType(metadata, [strict(fun)], allow)

  if (_fun instanceof AS.FunctionV) {
    return _fun.execute.bind(_fun)
  } else if (_fun instanceof AS.BooleanV) {
    return function (metadata: AS.Metadata, argv: AS.Value[]): AS.Value {
      checkArity(metadata, argv, 2)
      return argv[_fun.value ? 0 : 1]
    }
  } else if (_fun instanceof AS.DictV) {
    return function (metadata: AS.Metadata, argv: AS.Value[]): AS.Value {
      checkArity(metadata, argv, 1)
      const argKey = strict(argv[0]).asKey(strict)
      const value = _fun.value[argKey]
      if (value) return value
      throw new E.UnsuspectedHangeulNotFoundError(
        metadata,
        `사전에 다음 표제가 없습니다: ${argKey}`
      )
    }
  } else if (_fun instanceof AS.ComplexV) {
    return function (metadata: AS.Metadata, argv: AS.Value[]): AS.Value {
      checkArity(metadata, argv, 1)
      const arg = strict(argv[0])
      const [_arg] = checkType(metadata, [arg], [AS.IntegerV])
      if (_arg.value === 0n || _arg.value === 1n) {
        return new AS.FloatV(_fun.value.toVector()[Number(_arg.value)])
      }
      throw new E.UnsuspectedHangeulValueError(
        metadata,
        `복소수 객체의 ${_arg.value}번째 요소를 접근하려고 했습니다.`
      )
    }
  } else {
    const length = getLength(_fun.value)
    return function (metadata: AS.Metadata, argv: AS.Value[]): AS.Value {
      checkArity(metadata, argv, 1)
      const arg = strict(argv[0])
      const [_arg] = checkType(metadata, [arg], [AS.IntegerV])
      const idx = Number(_arg.value)
      const item =
        _fun instanceof AS.BytesV
          ? _accessBuffer(_fun.value, idx)
          : _fun instanceof AS.StringV
          ? _accessString(_fun.value, idx)
          : _accessArray(_fun.value, idx)
      if (item == null) {
        throw new E.UnsuspectedHangeulOutOfRangeError(
          metadata,
          `길이 ${length}의 객체의 ${idx}번째 요소를 요청했습니다.`
        )
      }
      if (item instanceof ArrayBuffer) return new AS.BytesV(item)
      if (typeof item === 'string') return new AS.StringV(item)
      return item
    }
  }
}
