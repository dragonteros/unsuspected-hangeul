import * as AS from '../abstractSyntax'
import { checkArity, checkType } from '../utils'

class PipeV extends AS.FunctionV {
  constructor(private funs: AS.Evaluation[]) {
    super('연결된 ')
  }

  execute(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ) {
    const result = this.funs.reduce(
      (argv, f) => [f(context, metadata, argv)],
      argv
    )
    return result[0]
  }
}
class CollectV extends AS.FunctionV {
  constructor(private context: AS.EvalContextBase, private fn: AS.Evaluation) {
    super('모아 받는 ')
  }

  execute(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ) {
    checkArity(metadata, argv, 1)
    const seq = this.context.strict(argv[0])
    const [_seq] = checkType(metadata, [seq], [AS.ListV, AS.ErrorV])
    return this.fn(context, metadata, _seq.value)
  }
}
class SpreadV extends AS.FunctionV {
  constructor(private fn: AS.Evaluation) {
    super('펼쳐 받는 ')
  }

  execute(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ) {
    return this.fn(context, metadata, [new AS.ListV(argv)])
  }
}

function _proc(context: AS.EvalContextBase, metadata: AS.Metadata) {
  return (fun: AS.Value) => context.procFunctional(metadata, fun, true)
}
function _pipe(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  return new PipeV(argv.map(_proc(context, metadata)))
}
function _collect(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, 1)
  return new CollectV(context, _proc(context, metadata)(argv[0]))
}
function _spread(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, 1)
  return new SpreadV(_proc(context, metadata)(argv[0]))
}
export default {
  ㄴㄱ: _pipe,
  ㅁㅂ: _collect,
  ㅂㅂ: _spread,
}
