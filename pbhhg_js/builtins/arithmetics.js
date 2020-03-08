import BigInteger from 'big-integer'
import Complex from 'complex.js'

import * as AS from '../abstractSyntax.js'
import {
  checkArity,
  checkType,
  checkMinArity,
  isType,
  extractValue,
  checkSameType
} from '../utils.js'
import { add, mul, div, mod, pow } from '../numbers.js'

function _joinArrayBuffer(bufs) {
  const size = bufs.map(a => a.byteLength).reduce((a, b) => a + b, 0)
  const newBuf = new ArrayBuffer(size)
  const view = new Uint8Array(newBuf)
  bufs.reduce(function(idx, buf) {
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

export default function(procFunctional, strict) {
  function _multiply(argv) {
    checkMinArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, [AS.BooleanV].concat(AS.NumberV))
    if (isType(argv, AS.NumberV)) {
      return wrapNumber(argv.map(extractValue).reduce(mul))
    }
    checkSameType(argv)
    return new AS.BooleanV(argv.every(extractValue))
  }

  function _add(argv) {
    checkMinArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, [AS.BooleanV, AS.DictV].concat(AS.NumberV, AS.SequenceV))
    const extracted = argv.map(extractValue)
    if (isType(argv, AS.NumberV)) {
      return wrapNumber(extracted.reduce(add))
    }
    checkSameType(argv)
    if (isType(argv, AS.BooleanV)) {
      return new AS.BooleanV(extracted.some(x => x))
    } else if (isType(argv, AS.StringV)) {
      return new AS.StringV(extracted.join(''))
    } else if (isType(argv, AS.BytesV)) {
      return new AS.BytesV(_joinArrayBuffer(extracted))
    } else if (isType(argv, AS.ListV)) {
      return new AS.ListV(extracted.reduce((a, b) => a.concat(b)))
    } else if (isType(argv, AS.DictV)) {
      var result = {}
      extracted.forEach(d => Object.assign(result, d))
      return new AS.DictV(result)
    }
  }

  function _exponentiate(argv) {
    checkArity(argv, [2, 3])
    argv = argv.map(strict)
    checkType(argv, AS.NumberV)
    if (argv.length === 3) {
      checkType(argv, AS.IntegerV)
      argv = argv.map(extractValue)
      return new AS.IntegerV(argv[0].modPow(argv[1], argv[2]))
    }
    checkArity(argv, 2)
    return wrapNumber(pow(argv[0].value, argv[1].value))
  }

  function _integerDivision(argv) {
    checkArity(argv, 2)
    argv = argv.map(strict)
    checkType(argv, AS.RealV)
    return wrapNumber(div(argv[0].value, argv[1].value))
  }

  function _remainder(argv) {
    checkArity(argv, 2)
    argv = argv.map(strict)
    checkType(argv, AS.RealV)
    return wrapNumber(mod(argv[0].value, argv[1].value))
  }

  return {
    ㄱ: _multiply,
    ㄷ: _add,
    ㅅ: _exponentiate,
    ㄴㄴ: _integerDivision,
    ㄴㅁ: _remainder
  }
}
