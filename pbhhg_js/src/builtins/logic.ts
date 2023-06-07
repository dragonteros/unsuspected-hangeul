import * as AS from '../abstractSyntax'
import { eq, JSNumber } from '../numbers'
import { allEqual, checkArity, checkType, extractValue, isType } from '../utils'

function _allNumbersEqual(nums: JSNumber[]) {
  if (nums.length === 0) return true
  return nums.slice(1).every((x) => eq(x, nums[0]))
}

function _allBytesEqual(buffers: ArrayBuffer[]) {
  if (buffers.length === 0) return true
  if (!allEqual(buffers.map((buf) => buf.byteLength))) return false
  const len = buffers[0].byteLength
  const views = buffers.map((buf) => new Uint8Array(buf))
  for (let i = 0; i < len; i++) {
    if (!allEqual(views.map((view) => view[i]))) return false
  }
  return true
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _listedEquals(arrs: AS.Value[][]): boolean {
    if (arrs.length === 0) return true
    if (!allEqual(arrs.map((arr) => arr.length))) return false
    var len = arrs[0].length
    for (var i = 0; i < len; i++) {
      // compare among tiers
      if (!_valueEquals(arrs.map((arr) => arr[i])).value) return false
    }
    return true
  }

  function _dictEquals(dicts: AS.DictV[]): boolean {
    if (dicts.length === 0) return true
    const keys = dicts.map((d) => d.keys())
    if (!_listedEquals(keys.map((ks) => ks.map((k) => new AS.StringV(k)))))
      return false
    const values = keys[0].map((k) => dicts.map((d) => d.value[k]))
    return values.map(_valueEquals).every(extractValue)
  }

  function _valueEquals(argv: AS.Value[]) {
    const _argv = argv.map(strict)
    if (isType(_argv, [AS.FunctionV])) {
      return new AS.BooleanV(allEqual(_argv))
    } else if (isType(_argv, [AS.DictV])) {
      return new AS.BooleanV(_dictEquals(_argv))
    } else if (isType(_argv, [AS.IOV])) {
      if (!allEqual(_argv.map((arg) => arg.inst))) return new AS.BooleanV(false)
      return new AS.BooleanV(_listedEquals(_argv.map((arg) => arg.argv)))
    } else if (isType(_argv, AS.NumberV)) {
      return new AS.BooleanV(_allNumbersEqual(_argv.map((arg) => arg.value)))
    } else if (isType(_argv, [AS.ListV, AS.ErrorV])) {
      return new AS.BooleanV(_listedEquals(_argv.map(extractValue)))
    } else if (isType(_argv, [AS.BytesV])) {
      return new AS.BooleanV(_allBytesEqual(_argv.map(extractValue)))
    } else if (isType(_argv, [AS.StringV])) {
      return new AS.BooleanV(allEqual(_argv.map((x) => x.str)))
    } else if (isType(_argv, [AS.BooleanV])) {
      return new AS.BooleanV(allEqual(_argv.map(extractValue)))
    } else if (isType(_argv, [AS.NilV])) {
      return new AS.BooleanV(true)
    }
    return new AS.BooleanV(false)
  }

  function _equals(metadata: AS.Metadata, argv: AS.Value[]) {
    return _valueEquals(argv)
  }

  function _negate(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 1)
    const _argv = checkType(metadata, argv.map(strict), [AS.BooleanV])
    return new AS.BooleanV(!_argv[0].value)
  }

  function _lessThan(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 2)
    const _argv = checkType(metadata, argv.map(strict), AS.RealV)
    return new AS.BooleanV(_argv[0].value < _argv[1].value)
  }

  function _true(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 0)
    return new AS.BooleanV(true)
  }

  function _false(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 0)
    return new AS.BooleanV(false)
  }

  return {
    ㄴ: _equals,
    ㅁ: _negate,
    ㅈ: _lessThan,
    ㅈㅈ: _true,
    ㄱㅈ: _false,
  }
}
