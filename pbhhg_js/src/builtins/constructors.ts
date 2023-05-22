import Complex from 'complex.js'

import * as AS from '../abstractSyntax'
import * as E from '../error'
import { arrayToInt, toComplex } from '../numbers'
import { checkArity, checkType, isType, matchDefaults } from '../utils'

function _parseStrToNumber(
  metadata: AS.Metadata,
  argv: AS.StrictValue[]
): [string, number] {
  const _argv = matchDefaults(metadata, argv, 2, [new AS.IntegerV(10n)])
  const [str] = checkType(metadata, [_argv[0]], [AS.StringV])
  const [num] = checkType(metadata, [_argv[1]], [AS.IntegerV])
  return [str.value, Number(num.value)]
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _list(metadata: AS.Metadata, argv: AS.Value[]) {
    return new AS.ListV(argv)
  }
  function _dict(metadata: AS.Metadata, argv: AS.Value[]) {
    const len = argv.length
    if (len % 2 === 1) {
      throw new E.UnsuspectedHangeulValueError(
        metadata,
        `ㅅㅈ 함수에는 인수를 짝수 개로 주어야 하는데 ${len}개를 주었습니다.`
      )
    }
    const keys = argv.filter((_, i) => i % 2 === 0)
    const values = argv.filter((_, i) => i % 2 === 1)
    const _keys = keys.map(strict).map((key) => key.asKey(strict))
    const result: Record<string, AS.Value> = {}
    for (let i = 0; i < len / 2; i++) {
      result[_keys[i]] = values[i]
    }
    return new AS.DictV(result)
  }
  function _string(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [0, 1])
    if (argv.length === 0) return new AS.StringV('')
    const [arg] = checkType(
      metadata,
      [strict(argv[0])],
      [AS.StringV, ...AS.NumberV]
    )
    if (arg instanceof AS.StringV) return arg
    return new AS.StringV(arg.toString())
  }
  function _integer(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [1, 2])
    const _argv = checkType(metadata, argv.map(strict), [
      AS.StringV,
      ...AS.RealV,
    ])
    const first = [_argv[0]]
    if (isType(first, AS.RealV)) {
      checkArity(metadata, _argv, 1)
      if (first[0] instanceof AS.IntegerV) return first[0]
      const value = Math.trunc(first[0].value)
      return new AS.IntegerV(BigInt(value))
    }
    const [digits, radix] = _parseStrToNumber(metadata, _argv)
    return new AS.IntegerV(arrayToInt(digits, radix))
  }
  function _float(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [1, 2])
    const _argv = checkType(metadata, argv.map(strict), [
      AS.StringV,
      ...AS.RealV,
    ])
    const first = [_argv[0]]
    if (isType(first, AS.RealV)) {
      checkArity(metadata, _argv, 1)
      return new AS.FloatV(Number(first[0].value))
    }
    const [digits, radix] = _parseStrToNumber(metadata, _argv)
    if (radix === 10) {
      const num = Number(digits)
      if (isNaN(num))
        throw new E.UnsuspectedHangeulValueError(
          metadata,
          `문자열 '${digits}'을 실수값으로 변환할 수 없습니다.`
        )
      return new AS.FloatV(num)
    }
    const splitted = digits.trim().split('.')
    let significant = splitted.join('')
    if (significant[0] === '+') significant = significant.slice(1)
    const _significant = parseInt(significant, radix)
    const order = splitted.length > 1 ? splitted[1].length : 0
    return new AS.FloatV(_significant / radix ** order)
  }
  function _complex(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [1, 2])
    const _argv = checkType(metadata, argv.map(strict), [
      AS.StringV,
      ...AS.NumberV,
    ])
    const values = _argv.map((arg) => toComplex(arg.value))
    if (argv.length === 1) return new AS.ComplexV(values[0])

    checkType(metadata, _argv, AS.NumberV)
    const re = values[0].re - values[1].im
    const im = values[0].im + values[1].re
    return new AS.ComplexV(Complex({ re, im }))
  }
  function _nil(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 0)
    return new AS.NilV()
  }

  return {
    ㅅㅈ: _dict,
    ㅁㄹ: _list,
    ㅁㅈ: _string,
    ㅈㅅ: _integer,
    ㅅㅅ: _float,
    ㅂㅅ: _complex,
    ㅂㄱ: _nil,
  }
}
