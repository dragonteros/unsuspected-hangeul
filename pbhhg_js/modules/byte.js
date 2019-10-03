import BigInteger from 'big-integer'

import * as AS from '../abstractSyntax.js'
import { checkType, checkArity } from '../utils.js'

function _write(view, arr, numBytes, bigEndian) {
  const _set = ({
    1: view.setUint8,
    2: view.setUint16,
    4: view.setUint32
  }[numBytes]).bind(view)
  for (let i = 0; i < arr.length; i++) {
    _set(i * numBytes, arr[i], !bigEndian)
  }
}

function _read(view, numBytes, bigEndian) {
  const _get = ({
    1: view.getUint8,
    2: view.getUint16,
    4: view.getUint32
  }[numBytes]).bind(view)
  var arr = []
  for (let i = 0; i < view.byteLength; i += numBytes) {
    arr.push(_get(i, !bigEndian))
  }
  return arr
}

const CODEC_TBL = ['utf', 'unsigned', 'signed', 'float']

class Codec extends AS.FunctionV {
  constructor(strict, scheme, numBytes, bigEndian) {
    super()
    this.strict = strict
    checkType([scheme, numBytes], AS.NumberV)
    this.scheme = CODEC_TBL[scheme.value]
    this.numBytes = numBytes.value
    this.bigEndian = bigEndian && bigEndian.value
    this.codec = this.getCodec()

    this.endianness = ''
    if (bigEndian !== undefined) {
      checkType(bigEndian, AS.BooleanV)
      this.endianness = bigEndian.value ? 'big' : 'little'
    }

    this.str = ('<Codec(scheme=' + this.scheme + ', num_bytes=' + this.numBytes +
      ', big_endian=' + this.bigEndian + ')>')
  }

  execute(argv) {
    argv = argv.map(this.strict)
    return this.codec(...argv)
  }

  getCodec() {
    switch (this.scheme) {
      case 'utf': return this.unicodeCodec
      case 'signed': return this.integerCodec
      case 'unsigned': return this.integerCodec
      case 'float': return this.floatingPointCodec
    }
  }

  unicodeCodec(argument) { // TODO: proper UTF-32
    checkType(argument, [AS.StringV, AS.BytesV])
    if (argument instanceof AS.StringV) {
      var encoded = argument.value
      if (this.numBytes == 1) {
        encoded = unescape(encodeURIComponent(encoded))
      } else if (this.endianness === '') {
        encoded = '\uFEFF' + encoded
      }
      const arr = encoded.split('').map(c => c.charCodeAt(0))
      const buf = new ArrayBuffer(arr.length * this.numBytes)
      _write(new DataView(buf), arr, this.numBytes, this.bigEndian)
      return new AS.BytesV(buf)
    } else {
      const buf = argument.value
      var view = new DataView(buf)
      var bigEndian = this.bigEndian || false
      if (this.endianness === '' && this.numBytes > 1) {
        const getter = (this.numBytes > 2 ? view.getUint32 : view.getUint16).bind(view)
        const guessBigEndian = (getter(0) === 0xFEFF)
        if (guessBigEndian || getter(0, true) === 0xFEFF) {
          bigEndian = guessBigEndian
          view = new DataView(buf, this.numBytes)
        }
      }
      const arr = _read(view, this.numBytes, bigEndian)
      var decoded = arr.map(c => String.fromCharCode(c)).join('')
      if (this.numBytes == 1) {
        decoded = decodeURIComponent(escape(decoded))
      }
      return new AS.StringV(decoded)
    }
  }

  integerCodec(argument) {
    const signed = (this.scheme === 'signed')
    checkType(argument, [AS.NumberV, AS.BytesV])
    if (argument instanceof AS.NumberV) {
      let num = BigInteger(argument.value)
      const isNegative = num.isNegative()
      if (isNegative && !signed) {
        throw EvalError('Unsigned Integer Converter expected nonnegative number but received: ' + argument)
      }
      const bitlen = num.bitLength() + (signed ? 1 : 0)
      if (bitlen > this.numBytes * 8) {
        throw EvalError('Cannot encode ' + argument.value + ' in ' + this.numBytes + ' bytes.')
      }
      if (isNegative) num = num.not()
      const arr = num.toArray(256).value
      let buf = new ArrayBuffer(this.numBytes)
      let u8 = new Uint8Array(buf)
      u8.set(arr, this.numBytes - arr.length)
      if (isNegative) u8.forEach((n, i) => u8[i] = ~n)
      if (!this.bigEndian) u8.reverse()
      return new AS.BytesV(buf)
    } else {
      const buf = argument.value.slice(0)
      let u8 = new Uint8Array(buf)
      if (!this.bigEndian) u8.reverse()
      const isNegative = signed && (u8[0] & 0x80)
      if (isNegative) u8.forEach((n, i) => u8[i] = ~n)
      const arr = Array.from(u8)
      let num = BigInteger.fromArray(arr, 256)
      if (isNegative) num = num.not()
      return new AS.NumberV(num)
    }
  }

  floatingPointCodec(argument) {
    throw EvalError('Not yet implemented')
  }
}

export default function (procFunctional, strict) {
  function codec(argv) {
    checkArity(argv, [2, 3])
    argv = argv.map(strict)
    return new Codec(strict, ...argv)
  }

  return {
    5:
      new AS.DictV({
        5: new AS.BuiltinModuleV(
          codec, 'ㅂ ㅂ'
        )
      })
  }
}
