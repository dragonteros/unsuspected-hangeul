import BigInteger from 'big-integer'
import Complex from 'complex.js'

import * as AS from '../abstractSyntax.js'
import { add, div, mod, mul, pow } from '../numbers.js'
import {
  checkArity,
  checkMinArity,
  checkSameType,
  checkType,
  extractValue,
  isType,
} from '../utils.js'

function _joinArrayBuffer(bufs) {
  const size = bufs.map((a) => a.byteLength).reduce((a, b) => a + b, 0)
  const newBuf = new ArrayBuffer(size)
  const view = new Uint8Array(newBuf)
  bufs.reduce(function (idx, buf) {
    view.set(new Uint8Array(buf), idx)
    return idx + buf.byteLength
  }, 0)
  return newBuf
}

export function wrapNumber(num) {
  if (num instanceof BigInteger) return new AS.IntegerV(num)
  if (num instanceof Complex) return new AS.ComplexV(num)
  if (typeof num === 'number') return new AS.FloatV(num)
  return null
}

export default function (procFunctional, strict) {
  function _multiply(metadata, argv) {
    checkMinArity(metadata, argv, 1)
    argv = argv.map(strict)
    checkType(metadata, argv, [AS.BooleanV].concat(AS.NumberV))
    if (isType(argv, AS.NumberV)) {
      return wrapNumber(argv.map(extractValue).reduce(mul))
    }
    checkSameType(metadata, argv)
    return new AS.BooleanV(argv.every(extractValue))
  }

  function _add(metadata, argv) {
    checkMinArity(metadata, argv, 1)
    argv = argv.map(strict)
    checkType(
      metadata,
      argv,
      [AS.BooleanV, AS.DictV].concat(AS.NumberV, AS.SequenceV)
    )
    const extracted = argv.map(extractValue)
    if (isType(argv, AS.NumberV)) {
      return wrapNumber(extracted.reduce(add))
    }
    checkSameType(metadata, argv)
    if (isType(argv, AS.BooleanV)) {
      return new AS.BooleanV(extracted.some((x) => x))
    } else if (isType(argv, AS.StringV)) {
      return new AS.StringV(extracted.join(''))
    } else if (isType(argv, AS.BytesV)) {
      return new AS.BytesV(_joinArrayBuffer(extracted))
    } else if (isType(argv, AS.ListV)) {
      return new AS.ListV(extracted.reduce((a, b) => a.concat(b)))
    } else if (isType(argv, AS.DictV)) {
      var result = {}
      extracted.forEach((d) => Object.assign(result, d))
      return new AS.DictV(result)
    }
  }

  function _exponentiate(metadata, argv) {
    checkArity(metadata, argv, [2, 3])
    argv = argv.map(strict)
    checkType(metadata, argv, AS.NumberV)
    if (argv.length === 3) {
      checkType(metadata, argv, AS.IntegerV)
      argv = argv.map(extractValue)
      return new AS.IntegerV(argv[0].modPow(argv[1], argv[2]))
    }
    checkArity(metadata, argv, 2)
    return wrapNumber(pow(argv[0].value, argv[1].value))
  }

  function _integerDivision(metadata, argv) {
    checkArity(metadata, argv, 2)
    argv = argv.map(strict)
    checkType(metadata, argv, AS.RealV)
    return wrapNumber(div(argv[0].value, argv[1].value))
  }

  function _remainder(metadata, argv) {
    checkArity(metadata, argv, 2)
    argv = argv.map(strict)
    checkType(metadata, argv, AS.RealV)
    return wrapNumber(mod(argv[0].value, argv[1].value))
  }

  return {
    ㄱ: _multiply,
    ㄷ: _add,
    ㅅ: _exponentiate,
    ㄴㄴ: _integerDivision,
    ㄴㅁ: _remainder,
  }
}
