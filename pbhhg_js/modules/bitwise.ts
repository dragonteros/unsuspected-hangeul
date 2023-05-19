import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, extractValue } from '../utils.js'

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
) {
  function _wrap(
    op: (...args: bigint[]) => bigint,
    arity: number
  ): AS.Evaluation {
    return function (metadata: AS.Metadata, argv: AS.Value[]) {
      checkArity(metadata, argv, arity)
      const _argv = checkType(metadata, argv.map(strict), [AS.IntegerV])
      return new AS.IntegerV(op(..._argv.map(extractValue)))
    }
  }

  return {
    ㅂㄷ: {
      ㄱ: _wrap((a, b) => a & b, 2),
      ㄷ: _wrap((a, b) => a | b, 2),
      ㅁ: _wrap((a) => ~a, 1),
      ㅂ: _wrap((a, b) => a ^ b, 2),
      ㅈ: _wrap((a, b) => a << b, 2),
    },
  }
}
