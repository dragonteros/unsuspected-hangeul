import * as AS from './abstractSyntax'
import * as E from './error'
import { encodeNumber } from './parse'
import { checkArity, checkType, isLiteralExpr } from './utils'

import buildArithmetics from './builtins/arithmetics'
import buildConstructors from './builtins/constructors'
import buildControl from './builtins/control'
import buildFunctional from './builtins/functional'
import buildIO from './builtins/io'
import buildLogic from './builtins/logic'
import buildModule from './builtins/module'
import buildSequence from './builtins/sequence'
import buildString from './builtins/string'

type BuiltinFunctionMap = Record<string, AS.Evaluation>
const BUILTINS: BuiltinFunctionMap = {
  ...buildArithmetics,
  ...buildConstructors,
  ...buildControl,
  ...buildFunctional,
  ...buildIO,
  ...buildLogic,
  ...buildModule,
  ...buildSequence,
  ...buildString,
}

export class EvalContext implements AS.EvalContextBase {
  constructor(public loadUtils: AS.LoadUtils) {}

  /** Forces strict evaluation of the value */
  strict(value: AS.Value): AS.StrictValue {
    if (value instanceof AS.ExprV) {
      if (value.cache) {
        if (value.cache instanceof AS.UnsuspectedHangeulError) {
          throw value.cache
        }
        return value.cache
      }
      try {
        value.cache = this.strict(interpret(this, value.expr, value.env))
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

  /**
   * Converts function-like values into functions.
   * @param metadata Caller's metadata.
   * @param fun A maybe-Expr value that may correspond to a function.
   * @param generalCallable Whether to allow callable other than function.
   * @returns A recipe function that receives argument list and returns the value.
   */
  procFunctional(
    metadata: AS.Metadata,
    fun: AS.Value,
    generalCallable?: boolean | undefined
  ): AS.Evaluation {
    if (isLiteralExpr(fun)) return findBuiltin(metadata, Number(fun.expr.value))

    const allow = generalCallable ? AS.CallableV : [AS.FunctionV]
    const [_fun] = checkType(metadata, [this.strict(fun)], allow)

    if (_fun instanceof AS.FunctionV) {
      return _fun.execute.bind(_fun)
    } else if (_fun instanceof AS.BooleanV) {
      return function (
        context: AS.EvalContextBase,
        metadata: AS.Metadata,
        argv: AS.Value[]
      ): AS.Value {
        checkArity(metadata, argv, 2)
        return argv[_fun.value ? 0 : 1]
      }
    } else if (_fun instanceof AS.DictV) {
      return function (
        context: AS.EvalContextBase,
        metadata: AS.Metadata,
        argv: AS.Value[]
      ): AS.Value {
        checkArity(metadata, argv, 1)
        const argKey = context.strict(argv[0]).asKey(context)
        const value = _fun.value[argKey]
        if (value) return value
        throw new E.UnsuspectedHangeulNotFoundError(
          metadata,
          `사전에 다음 표제가 없습니다: ${argKey}`
        )
      }
    } else if (_fun instanceof AS.ComplexV) {
      return function (
        context: AS.EvalContextBase,
        metadata: AS.Metadata,
        argv: AS.Value[]
      ): AS.Value {
        checkArity(metadata, argv, 1)
        const arg = context.strict(argv[0])
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
      return function (
        context: AS.EvalContextBase,
        metadata: AS.Metadata,
        argv: AS.Value[]
      ): AS.Value {
        checkArity(metadata, argv, 1)
        const arg = context.strict(argv[0])
        const [_arg] = checkType(metadata, [arg], [AS.IntegerV])
        const idx = Number(_arg.value)
        try {
          if (_fun instanceof AS.BytesV) {
            return new AS.BytesV(_accessBuffer(_fun.value, idx))
          }
          if (_fun instanceof AS.StringV) {
            return new AS.StringV(_accessArray(_fun.value, idx))
          }
          return _accessArray(_fun.value, idx)
        } catch (error) {
          if (error instanceof Error) {
            throw new E.UnsuspectedHangeulOutOfRangeError(
              metadata,
              error.message
            )
          }
          throw error
        }
      }
    }
  }
}

/**
 * Finds the built-in function corresponding to the builtin function id.
 * @param metadata Caller's metadata.
 * @param id Built-in function ID.
 * @returns corresponding function that takes arguments.
 */
function findBuiltin(metadata: AS.Metadata, id: number) {
  const inst = encodeNumber(id)
  const builtinFun = BUILTINS[inst]
  if (builtinFun) return builtinFun
  throw new E.UnsuspectedHangeulNotFoundError(
    metadata,
    `${inst}이라는 이름의 기본 제공 함수를 찾지 못했습니다.`
  )
}

function _accessArray<T>(arr: T[], rel: number): T {
  const idx = rel < 0 ? rel + arr.length : rel
  if (idx < 0 || idx >= arr.length)
    throw Error(`길이 ${arr.length}의 객체의 ${rel}번째 요소를 요청했습니다.`)
  return arr[idx]
}
function _accessBuffer(buf: ArrayBuffer, rel: number): ArrayBuffer {
  const idx = rel < 0 ? rel + buf.byteLength : rel
  if (idx < 0 || idx >= buf.byteLength)
    throw Error(
      `길이 ${buf.byteLength}의 바이트열의 ${rel}번째 요소를 요청했습니다.`
    )
  return buf.slice(idx, idx + 1)
}

/** Evaluates the expression in given environment and returns a value */
export function interpret(
  context: AS.EvalContextBase,
  expr: AS.AST,
  env: AS.Env
) {
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
    const relA = context.strict(interpret(context, expr.relA, env))
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
    var newEnv = new AS.Env(newFuns, env.args)
    var closure = new AS.ClosureV(expr.body, newEnv)
    newEnv.funs.push(closure)
    return closure
  } else if (expr instanceof AS.FunCall) {
    var fun = new AS.ExprV(expr.fun, env, null)
    var argv = expr.argv.map(function (arg) {
      return new AS.ExprV(arg, env, null)
    })
    var recipe = context.procFunctional(expr.metadata, fun, true)
    return recipe(context, expr.metadata, argv)
  }
  throw Error('Unexpected expression: ' + expr)
}
