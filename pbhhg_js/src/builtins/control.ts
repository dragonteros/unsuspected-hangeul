import * as AS from '../abstractSyntax'
import { checkArity, checkType } from '../utils'

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _throw(metadata: AS.Metadata, argv: AS.Value[]): AS.Value {
    checkArity(metadata, argv, 1)
    const [arg] = checkType(metadata, argv.map(strict), [AS.ErrorV])
    throw new AS.UnsuspectedHangeulError(arg)
  }
  function _try(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 2)
    try {
      return strict(argv[0])
    } catch (error) {
      if (error instanceof AS.UnsuspectedHangeulError) {
        const fun = procFunctional(metadata, argv[1])
        return fun(metadata, [error.err])
      }
      throw error
    }
  }

  return {
    ㄷㅈ: _throw,
    ㅅㄷ: _try,
  }
}
