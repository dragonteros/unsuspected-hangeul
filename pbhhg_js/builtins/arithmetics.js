import BigInteger from 'big-integer'

import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, checkMinArity, isType, extractValue } from '../utils.js'

export default function (procFunctional, strict) {
  function _multiply (argv) {
    checkMinArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, [AS.NumberV, AS.BooleanV])
    if (isType(argv, AS.BooleanV)) {
      return new AS.BooleanV(argv.every(extractValue))
    } else {
      return new AS.NumberV(argv.map(extractValue).reduce(
        function (a, b) {
          return isType([a, b], BigInteger) ? a.times(b) : a * b
        }, BigInteger.one))
    }
  }
  function _add (argv) {
    checkMinArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, [AS.NumberV, AS.BooleanV, AS.ListV, AS.StringV, AS.BytesV, AS.DictV])
    if (isType(argv, AS.BooleanV)) {
      return new AS.BooleanV(argv.some(extractValue))
    } else if (isType(argv, AS.StringV)) {
      return new AS.StringV(argv.map(extractValue).join(''))
    } else if (isType(argv, AS.BytesV)) {
      argv = argv.map(extractValue)
      const size = argv.map(a => a.byteLength).reduce((a, b) => a + b, 0)
      const newBuf = new ArrayBuffer(size)
      const view = new Uint8Array(newBuf)
      argv.reduce(function (idx, buf) {
        view.set(new Uint8Array(buf), idx)
        return idx + buf.byteLength
      }, 0)
      return new AS.BytesV(newBuf)
    } else if (isType(argv, AS.ListV)) {
      return new AS.ListV(argv.map(extractValue).reduce(
        function (a, b) { return a.concat(b) }, []))
    } else if (isType(argv, AS.DictV)) {
      var result = {}
      argv.forEach(d => Object.assign(result, d.value))
      return new AS.DictV(result)
    } else {
      return new AS.NumberV(argv.map(extractValue).reduce(
        function (a, b) {
          return isType([a, b], BigInteger) ? a.plus(b) : a + b
        }, BigInteger.zero))
    }
  }
  function _exponentiate (argv) {
    checkArity(argv, 2)
    argv = argv.map(strict)
    checkType(argv, AS.NumberV)
    if (isType(argv, BigInteger)) {
      var power = argv[0].value.pow(argv[1].value)
    } else {
      var power = Math.pow(argv[0].value, argv[1].value)
    }
    return new AS.NumberV(power)
  }

  return {
    ㄱ: _multiply,
    ㄷ: _add,
    ㅅ: _exponentiate
  }
}
