import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, extractValue } from '../utils.js'

export default function (procFunctional, strict) {
  function _split(metadata, argv) {
    checkArity(metadata, argv, [1, 2])
    argv = argv.map(strict)
    checkType(metadata, argv, AS.StringV)
    var src = argv[0].value
    var delimiter = argv.length > 1 ? argv[1].value : ''
    var pieces = src.split(delimiter)
    return new AS.ListV(pieces.map((piece) => new AS.StringV(piece)))
  }

  function _join(metadata, argv) {
    checkArity(metadata, argv, [1, 2])
    argv = argv.map(strict)
    var seq = argv[0]
    var delimiter = argv.length > 1 ? argv[1] : new AS.StringV('')
    checkType(metadata, seq, AS.ListV)
    checkType(metadata, delimiter, AS.StringV)
    var pieces = seq.value.map(strict)
    checkType(metadata, pieces, AS.StringV)
    return new AS.StringV(pieces.map(extractValue).join(delimiter.value))
  }

  return {
    ㅂㄹ: _split,
    ㄱㅁ: _join,
  }
}
