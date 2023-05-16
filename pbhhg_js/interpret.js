import * as AS from './abstractSyntax.js'
import * as E from './error.js'
import { encodeNumber } from './parse.js'
import {
  checkArity,
  checkType,
  chooseConstructorLike,
  isLiteralExpr,
} from './utils.js'

import buildArithmetics from './builtins/arithmetics.js'
import buildConstructors from './builtins/constructors.js'
import buildFunctional from './builtins/functional.js'
import buildIO from './builtins/io.js'
import buildLogic from './builtins/logic.js'
import buildModule from './builtins/module.js'
import buildSequence from './builtins/sequence.js'
import buildString from './builtins/string.js'

const BUILTINS = [
  buildArithmetics,
  buildConstructors,
  buildFunctional,
  buildIO,
  buildLogic,
  buildModule,
  buildSequence,
  buildString,
].reduce(
  (acc, builder) => Object.assign(acc, builder(procFunctional, strict)),
  {}
)

/**
 * Finds the built-in function corresponding to the builtin function id.
 * @param {AS.Metadata} metadata Caller's metadata.
 * @param {Number} id Built-in function ID.
 * @returns {Function} corresponding function that takes arguments.
 */
function findBuiltin(metadata, id) {
  const inst = encodeNumber(id)
  const builtinFun = BUILTINS[inst]
  if (builtinFun) return builtinFun
  throw new E.UnsuspectedHangeulNotFoundError(
    metadata,
    `${inst}라는 이름의 기본 제공 함수를 찾지 못했습니다.`
  )
}

/** Forces strict evaluation of the value */
export function strict(value) {
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

function _accessArray(arr, rel) {
  if (rel >= 0) return arr[rel]
  else return arr[arr.length + rel]
}
function _accessBuffer(buf, rel) {
  if (rel >= buf.byteLength) return undefined
  if (rel < 0) rel += buf.byteLength
  return buf.slice(rel, rel + 1)
}

/** Evaluates the expression in given environment and returns a value */
export function interpret(expr, env) {
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
    var args = _accessArray(env.args, -expr.relF - 1)
    if (args == null) {
      throw new E.UnsuspectedHangeulOutOfRangeError(
        expr.metadata,
        '존재하지 않는 함수에 대한 인수 참조를 시도했습니다.'
      )
    }
    var relA = strict(interpret(expr.relA, env))
    checkType(relA, AS.IntegerV)
    relA = relA.value
    if (relA.lt(0) || relA.geq(args.length)) {
      throw new E.UnsuspectedHangeulOutOfRangeError(
        expr.metadata,
        `${relA}번째 인수를 참조하는데 ${args.length}개의 인수만 받았습니다.`
      )
    } else return args[relA]
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
    var recipe = procFunctional(expr.metadata, fun, AS.CallableV)
    return recipe(argv)
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
export function procFunctional(metadata, fun, allow) {
  if (isLiteralExpr(fun)) return findBuiltin(metadata, fun.expr.value)

  fun = strict(fun)
  allow = allow || []
  allow = allow.concat([AS.FunctionV]) // default
  checkType(fun, allow)

  if (fun instanceof AS.FunctionV) {
    return fun.execute.bind(fun)
  } else if (fun instanceof AS.BooleanV) {
    return function (argv) {
      checkArity(argv, 2)
      return argv[fun.value ? 0 : 1]
    }
  } else if (fun instanceof AS.DictV) {
    return function (argv) {
      checkArity(argv, 1)
      const argKey = strict(argv[0]).asKey(strict)
      const value = fun.value[argKey]
      if (value) return value
      throw new E.UnsuspectedHangeulNotFoundError(
        metadata,
        `사전에 다음 표제가 없습니다: ${argKey}`
      )
    }
  } else if (fun instanceof AS.ComplexV) {
    return function (argv) {
      checkArity(argv, 1)
      const arg = strict(argv[0])
      checkType(arg, AS.IntegerV)
      if (arg.value == 0 || arg.value == 1) {
        return new AS.FloatV(fun.value.toVector()[arg.value])
      }
      throw new E.UnsuspectedHangeulValueError(
        metadata,
        `복소수 객체의 ${arg.value}번째 요소를 접근하려고 했습니다.`
      )
    }
  } else {
    const _access = fun instanceof AS.BytesV ? _accessBuffer : _accessArray
    const length =
      fun instanceof AS.BytesV ? fun.value.byteLength : fun.value.length
    return function (argv) {
      checkArity(argv, 1)
      const arg = strict(argv[0])
      checkType(arg, AS.IntegerV)
      const idx = arg.value
      var item = _access(fun.value, idx)
      if (item == null) {
        throw new E.UnsuspectedHangeulOutOfRangeError(
          expr.metadata,
          `길이 ${length}의 객체의 ${idx}번째 요소를 요청했습니다.`
        )
      }
      const V = chooseConstructorLike(fun, [AS.StringV, AS.BytesV])
      if (V) item = new V(item)
      return item
    }
  }
}
