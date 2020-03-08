import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, extractValue } from '../utils.js'

export default function(procFunctional, strict) {
  function _wrap(opName, arity) {
    return function(argv) {
      checkArity(argv, arity)
      argv = argv.map(strict)
      checkType(argv, AS.IntegerV)
      argv = argv.map(extractValue)
      var value = argv[0][opName](argv[1]) // assume 1 or 2
      return new AS.IntegerV(value)
    }
  }

  return {
    ㅂㄷ: {
      ㄱ: _wrap('and', 2),
      ㄷ: _wrap('or', 2),
      ㅁ: _wrap('not', 1),
      ㅂ: _wrap('xor', 2),
      ㅈ: _wrap('shiftLeft', 2)
    }
  }
}
