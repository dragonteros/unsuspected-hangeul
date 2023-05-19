import * as AS from '../abstractSyntax.js'
import { checkArity, checkType } from '../utils.js'

class PipeV extends AS.FunctionV {
  constructor(private funs: AS.Evaluation[]) {
    super('Piped ')
  }

  execute(metadata: AS.Metadata, args: AS.Value[]) {
    const result = this.funs.reduce((argv, f) => [f(metadata, argv)], args)
    return result[0]
  }
}
class CollectV extends AS.FunctionV {
  constructor(private fn: AS.Evaluation, private strict: AS.StrictFn) {
    super('Collectedly-Receiving ')
  }

  execute(metadata: AS.Metadata, args: AS.Value[]) {
    checkArity(metadata, args, 1)
    const seq = this.strict(args[0])
    const [_seq] = checkType(metadata, [seq], [AS.ListV])
    return this.fn(metadata, _seq.value)
  }
}
class SpreadV extends AS.FunctionV {
  constructor(private fn: AS.Evaluation) {
    super('Spreadly-Receiving ')
  }

  execute(metadata: AS.Metadata, args: AS.Value[]) {
    return this.fn(metadata, [new AS.ListV(args)])
  }
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _proc(metadata: AS.Metadata) {
    return (fun: AS.Value) => procFunctional(metadata, fun, true)
  }
  function _pipe(metadata: AS.Metadata, argv: AS.Value[]) {
    return new PipeV(argv.map(_proc(metadata)))
  }
  function _collect(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    return new CollectV(_proc(metadata)(argv[0]), strict)
  }
  function _spread(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    return new SpreadV(_proc(metadata)(argv[0]))
  }
  return {
    ㄴㄱ: _pipe,
    ㅁㅂ: _collect,
    ㅂㅂ: _spread,
  }
}
