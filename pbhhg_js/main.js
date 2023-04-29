import * as AS from './abstractSyntax.js'
import { interpret, procFunctional, strict } from './interpret.js'
import { parse } from './parse.js'
import { checkType, toString } from './utils.js'

/* Receives an IOV and produces non-ExprV value. */
function _doSingleIO(ioValue, ioUtils) {
  checkType(ioValue, AS.IOV)
  var inst = ioValue.inst
  var argv = ioValue.argv
  switch (inst) {
    case 'ㄹ':
      var input = ioUtils.input()
      return input == null ? new AS.NilV() : new AS.StringV(input)
    case 'ㅈㄹ':
      ioUtils.print(argv[0].value)
      return new AS.NilV()
    case 'ㄱㅅ':
      return strict(argv[0])
    case 'ㄱㄹ':
      var args = argv.slice()
      var binder = args.pop()
      args = args.map(strict)
      checkType(args, AS.IOV)
      args = args.map(a => doIO(a, ioUtils))
      var result = strict(procFunctional(binder)(args))
      checkType(result, AS.IOV)
      return result
  }
}

/* Receives an IOV and produces non-IOV non-ExprV value. */
function doIO(ioValue, ioUtils) {
  checkType(ioValue, AS.IOV)
  while (ioValue instanceof AS.IOV) {
    ioValue = _doSingleIO(ioValue, ioUtils)
  }
  return ioValue
}

/* Main procedure. Parses, evaluates, and converts to str.
    Args:
        arg: raw string that encodes a program
    Returns:
        A string representing the resulting value */
function main(arg, ioUtils, loadUtils, formatIO = true) {
  var exprs = parse(arg)
  var env = new AS.Env([], [], loadUtils)
  var values = exprs.map(function (expr) {
    return interpret(expr, env)
  })
  ioUtils['doIO'] = doIO
  return values.map(v => toString(v, strict, ioUtils, formatIO))
}

exports.main = main
