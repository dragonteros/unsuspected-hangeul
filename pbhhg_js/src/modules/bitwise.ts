import * as AS from '../abstractSyntax'
import { checkArity, checkType, extractValue } from '../utils'

function _wrap(
  op: (...args: bigint[]) => bigint,
  arity: number
): AS.Evaluation {
  return function (
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ) {
    checkArity(metadata, argv, arity)
    const _argv = checkType(
      metadata,
      argv.map((x) => context.strict(x)),
      [AS.IntegerV]
    )
    return new AS.IntegerV(op(..._argv.map(extractValue)))
  }
}

export default {
  ㅂㄷ: {
    ㄱ: _wrap((a, b) => a & b, 2),
    ㄷ: _wrap((a, b) => a | b, 2),
    ㅁ: _wrap((a) => ~a, 1),
    ㅂ: _wrap((a, b) => a ^ b, 2),
    ㅈ: _wrap((a, b) => a << b, 2),
  },
}
