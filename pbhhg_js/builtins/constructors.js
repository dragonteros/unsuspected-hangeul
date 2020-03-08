import BigInteger from 'big-integer'
import Complex from 'complex.js'

import * as AS from '../abstractSyntax.js'
import {
  checkArity,
  checkType,
  recursiveMap,
  toString,
  isType,
  matchDefaults,
  extractValue
} from '../utils.js'
import {_toComplex} from '../numbers.js'

function _parseStrToNumber(argv) {
  argv = matchDefaults(argv, 2, [new AS.IntegerV(BigInteger[10])])
  checkType(argv[0], AS.StringV)
  checkType(argv[1], AS.IntegerV)
  return argv.map(extractValue)
}

export default function(procFunctional, strict) {
  function _list(argv) {
    return new AS.ListV(argv)
  }
  function _dict(argv) {
    const len = argv.length
    if (len % 2 === 1) {
      throw SyntaxError(
        'Dict requires even numbers of arguments ' + 'but received: ' + len
      )
    }
    var keys = argv.filter((_, i) => i % 2 === 0)
    var values = argv.filter((_, i) => i % 2 === 1)
    keys = keys.map(item => recursiveMap(item, strict))
    keys = keys.map(v => toString(v, strict))
    var result = {}
    for (let i = 0; i < len / 2; i++) {
      result[keys[i]] = values[i]
    }
    return new AS.DictV(result)
  }
  function _string(argv) {
    checkArity(argv, [0, 1])
    if (argv.length === 0) return new AS.StringV('')
    var arg = strict(argv[0])
    checkType(arg, [AS.StringV].concat(AS.NumberV))
    if (arg instanceof AS.StringV) return arg
    if (arg instanceof AS.IntegerV) {
      return new AS.StringV(arg.value.toString())
    } else {
      return new AS.StringV(arg.toString())
    }
  }
  function _integer(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    checkType(argv, [AS.StringV].concat(AS.RealV))
    if (isType(argv[0], AS.RealV)) {
      checkArity(argv, 1)
      if (isType(argv, AS.IntegerV)) return argv[0]
      let value = Math.trunc(argv[0].value)
      return new AS.IntegerV(BigInteger(value))
    }
    argv = _parseStrToNumber(argv)
    return new AS.IntegerV(BigInteger(argv[0], argv[1]))
  }
  function _float(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    checkType(argv, [AS.StringV].concat(AS.RealV))
    if (isType(argv[0], AS.RealV)) {
      checkArity(argv, 1)
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
  function _complex(argv) {
    checkArity(argv, [1, 2])
    argv = argv.map(strict)
    checkType(argv, [AS.StringV].concat(AS.NumberV))
    const values = argv.map(extractValue).map(_toComplex)
    if (argv.length === 1) {
      return new AS.ComplexV(values[0])
    }
    checkType(argv, AS.NumberV)
    let re = values[0].re - values[1].im
    let im = values[0].im + values[1].re
    return new AS.ComplexV(Complex({re, im}))
  }
  function _nil(argv) {
    checkArity(argv, 0)
    return new AS.NilV()
  }

  return {
    ㅅㅈ: _dict,
    ㅁㄹ: _list,
    ㅁㅈ: _string,
    ㅈㅅ: _integer,
    ㅅㅅ: _float,
    ㅂㅅ: _complex,
    ㅂㄱ: _nil
  }
}
