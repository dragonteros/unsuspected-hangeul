import * as AS from '../abstractSyntax'
import * as E from '../error'
import { arrayToInt, intToArray } from '../numbers'
import { checkArity, checkType } from '../utils'

function _isBigEndianSystem() {
  // Copied from:
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView#endianness
  const buffer = new ArrayBuffer(2)
  new DataView(buffer).setInt16(0, 256, false /* big endian */)
  // Int16Array uses the platform's endianness.
  return new Int16Array(buffer)[0] === 256
}

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
  if (signed) return -bound / 2n <= integer && integer < bound / 2n
  return 0n <= integer && integer < bound
}

const CODEC_TBL = ['utf', 'unsigned', 'signed', 'float'] as const

class Codec extends AS.FunctionV {
  private scheme: (typeof CODEC_TBL)[number]
  private numBytes: number
  private bigEndian?: boolean
  private endianness: 'big' | 'little' | ''
  private codec: AS.Evaluation
  constructor(
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

  execute(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ) {
    const _argv = argv.map((x) => context.strict(x))
    try {
      return this.codec(context, metadata, _argv)
    } catch (error) {
      if (error instanceof AS.UnsuspectedHangeulError) throw error
      throw new E.UnsuspectedHangeulValueError(
        metadata,
        `요청된 변환을 수행하지 못했습니다. 변환기: ${this.str}, 인수: ${_argv}`
      )
    }
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

  unicodeCodec(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ) {
    checkArity(metadata, argv, 1)
    const [arg] = checkType(
      metadata,
      argv.map((x) => context.strict(x)),
      [AS.StringV, AS.BytesV]
    )
    if (arg instanceof AS.StringV) {
      if (this.numBytes === 1) {
        const encoder = new TextEncoder()
        return new AS.BytesV(encoder.encode(arg.str).buffer)
      }

      let arr: number[]
      if (this.numBytes === 2) {
        arr = arg.str.split('').map((c) => c.charCodeAt(0))
      } else if (this.numBytes === 4) {
        arr = arg.value
          .map((c) => c.codePointAt(0))
          .filter((x): x is number => x != null)
      } else {
        throw new E.UnsuspectedHangeulValueError(
          metadata,
          `UTF-${this.numBytes * 8} 형식은 존재하지 않습니다.`
        )
      }

      if (this.endianness === '') {
        arr.unshift(0xfeff)
      }
      const buf = new ArrayBuffer(arr.length * this.numBytes)
      _write(new DataView(buf), arr, this.numBytes, this.bigEndian)
      return new AS.BytesV(buf)
    } else {
      const buf = arg.value
      if (this.numBytes === 1) {
        const decoder = new TextDecoder()
        return new AS.StringV(decoder.decode(new Uint8Array(buf)))
      }

      let view = new DataView(buf)
      let bigEndian = this.bigEndian ?? _isBigEndianSystem()
      if (this.endianness === '') {
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
      return new AS.StringV(String.fromCodePoint(...arr))
    }
  }

  integerCodec(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ) {
    checkArity(metadata, argv, 1)
    const signed = this.scheme === 'signed'
    const [arg] = checkType(
      metadata,
      argv.map((x) => context.strict(x)),
      [AS.IntegerV, AS.BytesV]
    )
    if (arg instanceof AS.IntegerV) {
      let num = arg.value
      const isNegative = num < 0

      if (isNegative && !signed)
        throw Error('음수는 부호 없는 정수 형식으로 변환할 수 없습니다.')
      if (!isExpressible(num, BigInt(this.numBytes), signed))
        throw Error(
          `${this.numBytes}바이트로 표현할 수 없는 정수를 받았습니다.`
        )

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

  floatingPointCodec(
    context: AS.EvalContextBase,
    metadata: AS.Metadata,
    argv: AS.Value[]
  ): AS.Value {
    throw EvalError('Not yet implemented')
  }
}

function codec(
  context: AS.EvalContextBase,
  metadata: AS.Metadata,
  argv: AS.Value[]
) {
  checkArity(metadata, argv, [2, 3])
  const _argv = argv.map((x) => context.strict(x))
  const scheme = _argv[0]
  const numBytes = _argv[1]
  const bigEndian = _argv.length > 2 ? _argv[2] : undefined
  return new Codec(metadata, scheme, numBytes, bigEndian)
}

export default { ㅂ: codec }
