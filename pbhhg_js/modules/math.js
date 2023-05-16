import BigInteger from 'big-integer'

import * as AS from '../abstractSyntax.js'
import { wrapNumber } from '../builtins/arithmetics.js'
import { abs, isclose, isinf, isnan, toComplex } from '../numbers.js'
import { checkArity, checkType, extractValue, isType } from '../utils.js'

function _rountToInf(x) {
  return x > 0 ? Math.ceil(x) : Math.floor(x)
}
function _rountToEven(x) {
  let rounded = Math.round(x)
  if (x % 1 === 0.5 || x % 1 === -0.5) {
    if (rounded % 2 === 1 || rounded % 2 === -1) rounded--
  }
  return rounded
}
function _wrapType(type) {
  return function (arg) {
    return new type(arg)
  }
}

export default function (procFunctional, strict) {
  function _wrap(_fn, arity, retWrapper = wrapNumber, argType = AS.NumberV) {
    return function (metadata, argv) {
      checkArity(metadata, argv, arity)
      argv = argv.map(strict)
      checkType(metadata, argv, argType)
      return retWrapper(_fn(...argv.map(extractValue)))
    }
  }

  function _wrap2(fnName) {
    return function (metadata, argv) {
      checkArity(metadata, argv, 1)
      const arg = strict(argv[0])
      checkType(metadata, arg, AS.NumberV)
      if (isType(arg, AS.RealV)) {
        let value = Math[fnName](arg.value)
        if (!isNaN(value)) return new AS.FloatV(value)
      }
      return new AS.ComplexV(toComplex(arg.value)[fnName]())
    }
  }

  function _wrapRound(_rounder) {
    return function (metadata, argv) {
      checkArity(metadata, argv, 1)
      let arg = strict(argv[0])
      checkType(metadata, arg, AS.RealV)
      if (isType(arg, AS.IntegerV)) return arg
      arg = BigInteger(_rounder(arg.value))
      return new AS.IntegerV(arg)
    }
  }
  const _atan1 = _wrap2('atan')
  const _atan2 = _wrap(Math.atan2, 2, _wrapType(AS.FloatV), AS.RealV)
  function _atan(metadata, argv) {
    return argv.length === 2 ? _atan2(metadata, argv) : _atan1(metadata, argv)
  }
  return {
    ㅅ: {
      ㅂ: Math.PI,
      ㅈ: Math.E,
      ㅁ: Infinity,
      ㄴ: NaN,
      ㄱ: _wrap(isclose, 2, _wrapType(AS.BooleanV)),
      ㄴㄴ: _wrap(isnan, 1, _wrapType(AS.BooleanV)),
      ㅁㄴ: _wrap(isinf, 1, _wrapType(AS.BooleanV)),
      ㅈㄷ: _wrap(abs, 1),
      ㄹㄱ: _wrap2('log'),
      ㅅㄴ: _wrap2('sin'),
      ㄴㅅ: _wrap2('asin'),
      ㄱㅅ: _wrap2('cos'),
      ㅅㄱ: _wrap2('acos'),
      ㄷㄴ: _wrap2('tan'),
      ㄴㄷ: _atan,
      ㅂㄹ: {
        ㄱ: _wrapRound(Math.trunc),
        ㄴ: _wrapRound(Math.floor),
        ㄷ: _wrapRound(_rountToEven),
        ㄹ: _wrapRound(Math.ceil),
        ㅁ: _wrapRound(_rountToInf),
      },
    },
  }
}
