import * as AS from '../abstractSyntax'
import { checkArity, checkType, recursiveMap } from '../utils'

function _throw(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
): AS.Value {
  checkArity(metadata, argv, 1)
  const [arg] = checkType(
    metadata,
    argv.map((x) => context.strict(x)),
    [AS.ErrorV]
  )
  throw new AS.UnsuspectedHangeulError(arg)
}
function _try(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, 2)
  try {
    return recursiveMap(argv[0], (x) => context.strict(x))
  } catch (error) {
    if (error instanceof AS.UnsuspectedHangeulError) {
      const fun = context.procFunctional(metadata, argv[1])
      return fun(context, metadata, [error.err])
    }
    throw error
  }
}

export default {
  ㄷㅈ: _throw,
  ㅅㄷ: _try,
}
