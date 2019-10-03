import BigInteger from 'big-integer'

import * as AS from '../abstractSyntax.js'
import { checkArity, checkType, extractValue, isType } from '../utils.js'

function _allEqual (arr) {
  if (arr.length === 0) return true
  return arr.every(function (a) {
    return a === arr[0]
  })
}

function _allNumbersEqual (nums) {
  if (nums.length === 0) return true
  function _eqFirst(num) {
    if (nums[0] instanceof BigInteger) {
      return nums[0].eq(num)
    } else if (num instanceof BigInteger) {
      return num.eq(nums[0])
    }
    return nums[0] == num
  }
  return nums.slice(1).every(_eqFirst)
}

function _allBytesEqual (buffers) {
  if (buffers.length === 0) return true
  if (!_allEqual(buffers.map(buf => buf.byteLength))) return false
  const len = buffers[0].byteLength
  const views = buffers.map(buf => new Uint8Array(buf))
  for (let i=0; i<len; i++) {
    if (!_allEqual(views.map(view => view[i]))) return false
  }
  return true
}

export default function (procFunctional, strict) {
  function _listedEquals (arrs) {
    if (arrs.length === 0) return true
    if (!_allEqual(arrs.map(arr => arr.length))) return false
    var len = arrs[0].length
    for (var i = 0; i < len; i++) { // compare among tiers
      if (!_equals(arrs.map(arr => arr[i])).value) return false
    }
    return true
  }
  function _dictEquals (dicts) {
    if (dicts.length === 0) return true
    const keys = dicts.map(d => d.keys())
    if (!_allEqual(keys.map(JSON.stringify))) return false
    const values = keys[0].map(k => dicts.map(d => d.value[k]))
    return values.map(_equals).every(extractValue)
  }
  function _equals (argv) {
    argv = argv.map(strict)
    if (!isType(argv, AS.AnyV)) return new AS.BooleanV(false)
    if (isType(argv, AS.NilV)) return new AS.BooleanV(true)
    if (isType(argv, AS.NumberV)) {
      return new AS.BooleanV(_allNumbersEqual(argv.map(extractValue)))
    }
    if (isType(argv, AS.FunctionV)) {
      return new AS.BooleanV(_allEqual(argv))
    }
    if (isType(argv, AS.ListV)) {
      return new AS.BooleanV(_listedEquals(argv.map(extractValue)))
    }
    if (isType(argv, AS.BytesV)) {
      return new AS.BooleanV(_allBytesEqual(argv.map(extractValue)))
    }
    if (isType(argv, AS.DictV)) {
      return new AS.BooleanV(_dictEquals(argv))
    }
    if (isType(argv, AS.IOV)) {
      if (!_allEqual(argv.map(function (arg) { return arg.inst }))) {
        return new AS.BooleanV(false)
      }
      return new AS.BooleanV(_listedEquals(argv.map(function (arg) { return arg.argv })))
    }
    return new AS.BooleanV(_allEqual(argv.map(extractValue)))
  }

  function _negate (argv) {
    checkArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, AS.BooleanV)
    return new AS.BooleanV(!argv[0].value)
  }
  function _lessThan (argv) {
    checkArity(argv, 2)
    argv = argv.map(strict)
    checkType(argv, AS.NumberV)
    if (isType(argv, BigInteger)) {
      var value = argv[0].value.lt(argv[1].value)
    } else {
      var value = argv[0].value < argv[1].value
    }
    return new AS.BooleanV(value)
  }
  function _true (argv) {
    checkArity(argv, 0)
    return new AS.BooleanV(true)
  }
  function _false (argv) {
    checkArity(argv, 0)
    return new AS.BooleanV(false)
  }

  return {
    ㄴ: _equals,
    ㅁ: _negate,
    ㅈ: _lessThan,
    ㅈㅈ: _true,
    ㄱㅈ: _false
  }
}
