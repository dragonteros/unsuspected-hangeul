import * as AS from '../abstractSyntax.js'
import { checkArity, checkType } from '../utils.js'

class PipeV extends AS.FunctionV {
  constructor(funs) {
    super('Piped ')
    this.funs = funs
  }

  execute(args) {
    const result = this.funs.reduce((argv, f) => [f(argv)], args)
    return result[0]
  }
}
class CollectV extends AS.FunctionV {
  constructor(fn, strict) {
    super('Collectedly-Receiving ')
    this.fn = fn
    this.strict = strict
  }

  execute(args) {
    checkArity(args, 1)
    const seq = this.strict(args[0])
    checkType(seq, AS.ListV)
    return this.fn(seq.value)
  }
}
class SpreadV extends AS.FunctionV {
  constructor(fn) {
    super('Spreadly-Receiving ')
    this.fn = fn
  }

  execute(args) {
    return this.fn([new AS.ListV(args)])
  }
}

export default function (procFunctional, strict) {
  function _proc(fun) {
    return procFunctional(metadata, fun, AS.CallableV)
  }
  function _pipe(metadata, argv) {
    return new PipeV(argv.map(_proc))
  }
  function _collect(metadata, argv) {
    checkArity(argv, 1)
    return new CollectV(_proc(argv[0]), strict)
  }
  function _spread(metadata, argv) {
    checkArity(argv, 1)
    return new SpreadV(_proc(argv[0]))
  }
  return {
    ㄴㄱ: _pipe,
    ㅁㅂ: _collect,
    ㅂㅂ: _spread,
  }
}
