import * as AS from '../abstractSyntax.js'
import {
  allEqual,
  checkArity,
  checkType,
  extractValue,
  isType,
  isSameType
} from '../utils.js'
import { eq } from '../numbers.js'

function _allNumbersEqual(nums) {
  if (nums.length === 0) return true
  return nums.slice(1).every(x => eq(x, nums[0]))
}

function _allBytesEqual(buffers) {
  if (buffers.length === 0) return true
  if (!allEqual(buffers.map(buf => buf.byteLength))) return false
  const len = buffers[0].byteLength
  const views = buffers.map(buf => new Uint8Array(buf))
  for (let i = 0; i < len; i++) {
    if (!allEqual(views.map(view => view[i]))) return false
  }
  return true
}

export default function(procFunctional, strict) {
  function _listedEquals(arrs) {
    if (arrs.length === 0) return true
    if (!allEqual(arrs.map(arr => arr.length))) return false
    var len = arrs[0].length
    for (var i = 0; i < len; i++) {
      // compare among tiers
      if (!_equals(arrs.map(arr => arr[i])).value) return false
    }
    return true
  }

  function _dictEquals(dicts) {
    if (dicts.length === 0) return true
    const keys = dicts.map(d => d.keys())
    if (!allEqual(keys.map(JSON.stringify))) return false
    const values = keys[0].map(k => dicts.map(d => d.value[k]))
    return values.map(_equals).every(extractValue)
  }

  function _equals(argv) {
    argv = argv.map(strict)
    if (isType(argv, AS.FunctionV)) {
      return new AS.BooleanV(allEqual(argv))
    } else if (isType(argv, AS.DictV)) {
      return new AS.BooleanV(_dictEquals(argv))
    } else if (isType(argv, AS.IOV)) {
      if (!allEqual(argv.map(arg => arg.inst))) {
        return new AS.BooleanV(false)
      }
      return new AS.BooleanV(_listedEquals(argv.map(arg => arg.argv)))
    } else if (isType(argv, AS.NilV)) {
      return new AS.BooleanV(true)
    }

    const extracted = argv.map(extractValue)
    if (isType(argv, AS.NumberV)) {
      return new AS.BooleanV(_allNumbersEqual(extracted))
    } else if (isType(argv, AS.ListV)) {
      return new AS.BooleanV(_listedEquals(extracted))
    } else if (isType(argv, AS.BytesV)) {
      return new AS.BooleanV(_allBytesEqual(extracted))
    }
    // StringV, BooleanV
    return new AS.BooleanV(isSameType(argv) && allEqual(extracted))
  }

  function _negate(argv) {
    checkArity(argv, 1)
    argv = argv.map(strict)
    checkType(argv, AS.BooleanV)
    return new AS.BooleanV(!argv[0].value)
  }

  function _lessThan(argv) {
    checkArity(argv, 2)
    argv = argv.map(strict)
    checkType(argv, AS.RealV)
    if (isType(argv, AS.IntegerV)) {
      var value = argv[0].value.lt(argv[1].value)
    } else {
      var value = argv[0].value < argv[1].value
    }
    return new AS.BooleanV(value)
  }

  function _true(argv) {
    checkArity(argv, 0)
    return new AS.BooleanV(true)
  }

  function _false(argv) {
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
