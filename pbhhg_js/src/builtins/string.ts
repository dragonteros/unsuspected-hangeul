import * as AS from '../abstractSyntax'
import { checkArity, checkType, joinArrayBuffer } from '../utils'

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _split(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [1, 2])
    const _argv = checkType(metadata, argv.map(strict), [AS.StringV, AS.BytesV])
    if (_argv[0] instanceof AS.StringV) {
      const __argv = checkType(metadata, _argv, [AS.StringV])
      const src = __argv[0].str
      const delimiter = __argv.length > 1 ? __argv[1].str : ''
      const pieces = src.split(delimiter)
      return new AS.ListV(pieces.map((piece) => new AS.StringV(piece)))
    }
    const __argv = checkType(metadata, _argv, [AS.BytesV])
    const src = String.fromCharCode(...new Uint8Array(__argv[0].value))
    const delimiter =
      __argv.length > 1
        ? String.fromCharCode(...new Uint8Array(__argv[1].value))
        : ''
    const pieces = src.split(delimiter)
    const buf = pieces.map(
      (piece) =>
        new AS.BytesV(
          new Uint8Array(piece.split('').map((c) => c.charCodeAt(0))).buffer
        )
    )
    return new AS.ListV(buf)
  }

  function _join(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [1, 2])

    const [seq] = checkType(metadata, [strict(argv[0])], [AS.ListV])
    const pieces = checkType(metadata, seq.value.map(strict), [
      AS.StringV,
      AS.BytesV,
    ])

    if (pieces[0] instanceof AS.StringV) {
      const _pieces = checkType(metadata, pieces, [AS.StringV])
      const delimiter = argv.length > 1 ? strict(argv[1]) : new AS.StringV('')
      const [_delimiter] = checkType(metadata, [delimiter], [AS.StringV])
      return new AS.StringV(_pieces.map((x) => x.str).join(_delimiter.str))
    }

    const _pieces = checkType(metadata, pieces, [AS.BytesV])
    const delimiter =
      argv.length > 1 ? strict(argv[1]) : new AS.BytesV(new ArrayBuffer(0))
    const [_delimiter] = checkType(metadata, [delimiter], [AS.BytesV])

    if (_pieces.length === 0) return new AS.BytesV(new ArrayBuffer(0))
    const buffers = [_pieces[0].value]
    for (const piece of _pieces.slice(1)) {
      buffers.push(_delimiter.value)
      buffers.push(piece.value)
    }
    return new AS.BytesV(joinArrayBuffer(buffers))
  }

  return {
    ㅂㄹ: _split,
    ㄱㅁ: _join,
  }
}
