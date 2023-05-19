import { arrayToInt, intToArray } from '@/numbers.js'
import * as AS from '../abstractSyntax.js'
import { checkArity, checkType } from '../utils.js'

function _write(
  view: DataView,
  arr: number[],
  numBytes: number,
  bigEndian?: boolean
) {
  const _set = {
    1: view.setUint8.bind(view),
    2: view.setUint16.bind(view),
    4: view.setUint32.bind(view),
  }[numBytes]
  if (_set == null) throw Error()
  for (let i = 0; i < arr.length; i++) {
    _set(i * numBytes, arr[i], !bigEndian)
  }
}

function _read(view: DataView, numBytes: number, bigEndian?: boolean) {
  const _get = {
    1: view.getUint8.bind(view),
    2: view.getUint16.bind(view),
    4: view.getUint32.bind(view),
  }[numBytes]
  if (_get == null) throw Error()
  var arr = []
  for (let i = 0; i < view.byteLength; i += numBytes) {
    arr.push(_get(i, !bigEndian))
  }
  return arr
}

function isExpressible(integer: bigint, numBytes: bigint, signed: boolean) {
  const bound = 2n << (8n * numBytes)
  if (signed) return 0n <= integer && integer < bound
  return -bound / 2n <= integer && integer < bound / 2n
}

const CODEC_TBL = ['utf', 'unsigned', 'signed', 'float'] as const

class Codec extends AS.FunctionV {
  private scheme: (typeof CODEC_TBL)[number]
  private numBytes: number
  private bigEndian?: boolean
  private endianness: 'big' | 'little' | ''
  private codec: AS.Evaluation
  constructor(
    public strict: AS.StrictFn,
    metadata: AS.Metadata,
    scheme: AS.StrictValue,
    numBytes: AS.StrictValue,
    bigEndian?: AS.StrictValue
  ) {
    super()
    const [_scheme, _numBytes] = checkType(
      metadata,
      [scheme, numBytes],
      [AS.IntegerV]
    )
    this.scheme = CODEC_TBL[Number(_scheme.value)]
    this.numBytes = Number(_numBytes.value)
    this.endianness = ''
    if (bigEndian) {
      const [_bigEndian] = checkType(metadata, [bigEndian], [AS.BooleanV])
      this.bigEndian = _bigEndian.value
      this.endianness = this.bigEndian ? 'big' : 'little'
    }
    this.codec = this.getCodec()

    this.str =
      '<Codec(scheme=' +
      this.scheme +
      ', num_bytes=' +
      this.numBytes +
      ', big_endian=' +
      this.bigEndian +
      ')>'
  }

  execute(metadata: AS.Metadata, argv: AS.Value[]) {
    return this.codec(metadata, argv.map(this.strict))
  }

  getCodec(): AS.Evaluation {
    switch (this.scheme) {
      case 'utf':
        return this.unicodeCodec
      case 'signed':
        return this.integerCodec
      case 'unsigned':
        return this.integerCodec
      case 'float':
        return this.floatingPointCodec
    }
  }

  unicodeCodec(metadata: AS.Metadata, argv: AS.Value[]) {
    // TODO: proper UTF-32
    checkArity(metadata, argv, 1)
    const [arg] = checkType(metadata, argv.map(this.strict), [
      AS.StringV,
      AS.BytesV,
    ])
    if (arg instanceof AS.StringV) {
      if (this.numBytes == 1) {
        const encoder = new TextEncoder()
        return new AS.BytesV(encoder.encode(arg.value).buffer)
      }
      let encoded = arg.value
      if (this.endianness === '') {
        encoded = '\uFEFF' + encoded
      }
      const arr = encoded.split('').map((c) => c.charCodeAt(0))
      const buf = new ArrayBuffer(arr.length * this.numBytes)
      _write(new DataView(buf), arr, this.numBytes, this.bigEndian)
      return new AS.BytesV(buf)
    } else {
      const buf = arg.value
      var view = new DataView(buf)
      var bigEndian = this.bigEndian || false
      if (this.endianness === '' && this.numBytes > 1) {
        const getter = (
          this.numBytes > 2 ? view.getUint32 : view.getUint16
        ).bind(view)
        const guessBigEndian = getter(0) === 0xfeff
        if (guessBigEndian || getter(0, true) === 0xfeff) {
          bigEndian = guessBigEndian
          view = new DataView(buf, this.numBytes)
        }
      }
      const arr = _read(view, this.numBytes, bigEndian)
      var decoded = arr.map((c) => String.fromCharCode(c)).join('')
      if (this.numBytes == 1) {
        decoded = decodeURIComponent(escape(decoded))
      }
      return new AS.StringV(decoded)
    }
  }

  integerCodec(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    const signed = this.scheme === 'signed'
    const [arg] = checkType(metadata, argv.map(this.strict), [
      AS.IntegerV,
      AS.BytesV,
    ])
    if (arg instanceof AS.IntegerV) {
      let num = arg.value
      const isNegative = num < 0
      if (isNegative && !signed) throw Error()
      if (!isExpressible(num, BigInt(this.numBytes), signed)) throw Error()

      if (isNegative) num = ~num
      const arr = intToArray(num, 256n).map(Number)
      const buf = new ArrayBuffer(this.numBytes)
      const u8 = new Uint8Array(buf)
      u8.set(arr, this.numBytes - arr.length)
      if (isNegative) u8.forEach((n, i) => (u8[i] = ~n))
      if (!this.bigEndian) u8.reverse()
      return new AS.BytesV(buf)
    } else {
      const buf = arg.value.slice(0)
      const u8 = new Uint8Array(buf)
      if (!this.bigEndian) u8.reverse()
      const isNegative = signed && u8[0] & 0x80
      if (isNegative) u8.forEach((n, i) => (u8[i] = ~n))
      const arr = Array.from(u8)
      let num = arrayToInt(arr, 256)
      if (isNegative) num = ~num
      return new AS.IntegerV(num)
    }
  }

  floatingPointCodec(metadata: AS.Metadata, argv: AS.Value[]): AS.Value {
    throw EvalError('Not yet implemented')
  }
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function codec(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [2, 3])
    const _argv = argv.map(strict)
    const scheme = _argv[0]
    const numBytes = _argv[1]
    const bigEndian = _argv.length > 2 ? _argv[2] : undefined
    return new Codec(strict, metadata, scheme, numBytes, bigEndian)
  }

  return { ㅂ: codec }
}
