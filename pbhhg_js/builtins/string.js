import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, extractValue } from '../utils.js'

export default function (procFunctional, strict) {
  function _split(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    checkType(argv, AS.StringV)
    var src = argv[0].value
    var delimiter = argv.length > 1 ? argv[1].value : ''
    var pieces = src.split(delimiter)
    return new AS.ListV(pieces.map(piece => new AS.StringV(piece)))
  }

  function _join(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    var seq = argv[0]
    var delimiter = argv.length > 1 ? argv[1] : new AS.StringV('')
    checkType(seq, AS.ListV)
    checkType(delimiter, AS.StringV)
    var pieces = seq.value.map(strict)
    checkType(pieces, AS.StringV)
    return new AS.StringV(pieces.map(extractValue).join(delimiter.value))
  }

  return {
    ㅂㄹ: _split,
    ㄱㅁ: _join
  }
}
