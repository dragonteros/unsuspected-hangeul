import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, extractValue } from '../utils.js'

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _split(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [1, 2])
    const _argv = checkType(metadata, argv.map(strict), [AS.StringV])
    var src = _argv[0].value
    var delimiter = argv.length > 1 ? _argv[1].value : ''
    var pieces = src.split(delimiter)
    return new AS.ListV(pieces.map((piece) => new AS.StringV(piece)))
  }

  function _join(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [1, 2])
    var seq = strict(argv[0])
    var delimiter = argv.length > 1 ? strict(argv[1]) : new AS.StringV('')
    const [_seq] = checkType(metadata, [seq], [AS.ListV])
    const [_delim] = checkType(metadata, [delimiter], [AS.StringV])
    var pieces = checkType(metadata, _seq.value.map(strict), [AS.StringV])
    return new AS.StringV(pieces.map(extractValue).join(_delim.value))
  }

  return {
    ㅂㄹ: _split,
    ㄱㅁ: _join,
  }
}
