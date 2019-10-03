import * as AS from './abstractSyntax.js'
import {
  recursiveMap,
  checkType,
  checkArity,
  isLiteralExpr,
  toString,
  chooseConstructorLike
} from './utils.js'
import { encodeNumber } from './parse.js'

import buildArithmetics from './builtins/arithmetics.js'
import buildconstructors from './builtins/constructors.js'
import buildFunctional from './builtins/functional.js'
import buildIO from './builtins/io.js'
import buildLogic from './builtins/logic.js'
import buildModule from './builtins/module.js'
import buildSequence from './builtins/sequence.js'
import buildString from './builtins/string.js'

const BUILTINS = [
  buildArithmetics,
  buildconstructors,
  buildFunctional,
  buildIO,
  buildLogic,
  buildModule,
  buildSequence,
  buildString
].reduce((acc, builder) => Object.assign(acc, builder(procFunctional, strict)), {})

/* Finds the built-in function corresponding to the builtin function id.
Args:
    id: Built-in Function ID
Returns:
    Return corresponding function that takes arguments */
function findBuiltin (id) {
  const inst = encodeNumber(id)
  const builtinFun = BUILTINS[inst]
  if (builtinFun) return builtinFun
  throw EvalError('Unexpected builtin functions ' + inst)
}

/* Forces strict evaluation of the value */
function strict (value) {
  if (value instanceof AS.ExprV) {
    if (value.cache) return value.cache
    else {
      value.cache = strict(interpret(value.expr, value.env))
      return value.cache
    }
  } else return value
}

function _accessArray (arr, rel) {
  if (rel >= 0) return arr[rel]
  else return arr[arr.length + rel]
}
function _accessBuffer (buf, rel) {
  if (rel < 0) rel += buf.byteLength
  return buf.slice(rel, rel+1)
}

/* Evaluates the expression in given environment and
 * returns a value */
function interpret (expr, env) {
  if (expr instanceof AS.Literal) {
    return new AS.NumberV(expr.value)
  } else if (expr instanceof AS.FunRef) {
    return _accessArray(env.funs, -expr.rel - 1)
  } else if (expr instanceof AS.ArgRef) {
    if (env.funs.length !== env.args.length) {
      throw EvalError(
        'Assertion Error: Environment has ' +
        env.funs.length +
        ' funs and ' +
        env.args.length +
        ' args.'
      )
    }
    var args = _accessArray(env.args, -expr.relF - 1)
    var relA = strict(interpret(expr.relA, env))
    checkType(relA, AS.NumberV)
    relA = Math.round(relA.value)
    if (relA < 0 || relA >= args.length) {
      throw EvalError(
        'Out of Range: ' +
        args.length +
        ' args received ' +
        'but ' +
        relA +
        '-th argument requested'
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
    var recipe = procFunctional(fun, AS.CallableV)
    return recipe(argv)
  }
  throw EvalError('Unexpected expression: ' + expr)
}

/*
Args:
  fun: A maybe-Expr value that may correspond to a function.
  allow: A list of types that are allowed for execution.
Returns:
  A recipe function that receives argument list and returns the value.
*/
function procFunctional (fun, allow, stricted) {
  if (isLiteralExpr(fun)) {
    return findBuiltin(fun.expr.value)
  }
  fun = stricted || strict(fun)
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
      const arg = recursiveMap(argv[0], strict)
      const value = fun.value[toString(arg, strict)]
      if (value) return value
      throw EvalError('Key Error: dict ' + fun.value + ' has no key ' + arg)
    }
  } else {
    const _access = fun instanceof AS.BytesV? _accessBuffer: _accessArray
    return function (argv) {
      checkArity(argv, 1)
      const arg = strict(argv[0])
      checkType(arg, AS.NumberV)
      const idx = Math.round(arg.value)
      var item = _access(fun.value, idx)
      const V = chooseConstructorLike(fun, [AS.StringV, AS.BytesV])
      if (V) item = new V(item)
      return item
    }
  }
}

export {
  strict,
  interpret,
  procFunctional
}
