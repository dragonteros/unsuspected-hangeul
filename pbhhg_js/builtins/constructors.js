import BigInteger from 'big-integer'
import Complex from 'complex.js'

import * as AS from '../abstractSyntax.js'
import * as E from '../error.js'
import { toComplex } from '../numbers.js'
import {
  checkArity,
  checkType,
  extractValue,
  isType,
  matchDefaults,
} from '../utils.js'

function _parseStrToNumber(argv) {
  argv = matchDefaults(argv, 2, [new AS.IntegerV(BigInteger[10])])
  checkType(argv[0], AS.StringV)
  checkType(argv[1], AS.IntegerV)
  return argv.map(extractValue)
}

export default function (procFunctional, strict) {
  function _list(metadata, argv) {
    return new AS.ListV(argv)
  }
  function _dict(metadata, argv) {
    const len = argv.length
    if (len % 2 === 1) {
      throw new E.UnsuspectedHangeulValueError(
        metadata,
        `ㅅㅈ 함수에는 인수를 짝수 개로 주어야 하는데 ${len}개를 주었습니다.`
      )
    }
    var keys = argv.filter((_, i) => i % 2 === 0)
    var values = argv.filter((_, i) => i % 2 === 1)
    keys = keys.map(strict).map((key) => key.asKey(strict))
    var result = {}
    for (let i = 0; i < len / 2; i++) {
      result[keys[i]] = values[i]
    }
    return new AS.DictV(result)
  }
  function _string(metadata, argv) {
    checkArity(metadata, argv, [0, 1])
    if (argv.length === 0) return new AS.StringV('')
    var arg = strict(argv[0])
    checkType(metadata, arg, [AS.StringV].concat(AS.NumberV))
    if (arg instanceof AS.StringV) return arg
    if (arg instanceof AS.IntegerV) {
      return new AS.StringV(arg.value.toString())
    } else {
      return new AS.StringV(arg.toString())
    }
  }
  function _integer(metadata, argv) {
    checkArity(metadata, argv, [1, 2])
    argv = argv.map(strict)
    checkType(metadata, argv, [AS.StringV].concat(AS.RealV))
    if (isType(argv[0], AS.RealV)) {
      checkArity(metadata, argv, 1)
      if (isType(argv, AS.IntegerV)) return argv[0]
      let value = Math.trunc(argv[0].value)
      return new AS.IntegerV(BigInteger(value))
    }
    argv = _parseStrToNumber(argv)
    return new AS.IntegerV(BigInteger(argv[0], argv[1]))
  }
  function _float(metadata, argv) {
    checkArity(metadata, argv, [1, 2])
    argv = argv.map(strict)
    checkType(metadata, argv, [AS.StringV].concat(AS.RealV))
    if (isType(argv[0], AS.RealV)) {
      checkArity(metadata, argv, 1)
      return new AS.FloatV(argv[0].value)
    }
    argv = _parseStrToNumber(argv)
    if (argv[1] == 10) {
      return new AS.FloatV(+argv[0])
    }
    const splitted = argv[0].trim().split('.')
    let significant = splitted.join('')
    if (significant[0] === '+') significant = significant.slice(1)
    significant = BigInteger(significant, argv[1])
    const order = splitted.length > 1 ? splitted[1].length : 0
    return new AS.FloatV(significant / argv[1].pow(order))
  }
  function _complex(metadata, argv) {
    checkArity(metadata, argv, [1, 2])
    argv = argv.map(strict)
    checkType(metadata, argv, [AS.StringV].concat(AS.NumberV))
    const values = argv.map(extractValue).map(toComplex)
    if (argv.length === 1) {
      return new AS.ComplexV(values[0])
    }
    checkType(metadata, argv, AS.NumberV)
    let re = values[0].re - values[1].im
    let im = values[0].im + values[1].re
    return new AS.ComplexV(Complex({ re, im }))
  }
  function _nil(metadata, argv) {
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
