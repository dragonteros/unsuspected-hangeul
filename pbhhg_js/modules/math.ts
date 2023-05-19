import { wrapNumber } from '@/builtins/arithmetics.js'
import * as AS from '../abstractSyntax.js'
import { JSNumber, abs, isclose, isinf, isnan, toComplex } from '../numbers.js'
import { checkArity, checkType, isType } from '../utils.js'

function _rountToInf(x: number) {
  return x > 0 ? Math.ceil(x) : Math.floor(x)
}
function _rountToEven(x: number) {
  let rounded = Math.round(x)
  if (x % 1 === 0.5 || x % 1 === -0.5) {
    if (rounded % 2 === 1 || rounded % 2 === -1) rounded--
  }
  return rounded
}
function _wrapType<T, V>(type: { new (arg: V): T }) {
  return (arg: V) => new type(arg)
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
) {
  function _wrap<
    ReturnInnerValue,
    ReturnValue extends AS.StrictValue & { value: ReturnInnerValue },
    ArgInnerValue extends InstanceType<ArgValue>['value'],
    ArgValue extends (typeof AS.NumberV)[number]
  >(
    _fn: (...args: ArgInnerValue[]) => ReturnInnerValue,
    arity: number,
    retWrapper: (inner: ReturnInnerValue) => ReturnValue,
    argType: readonly ArgValue[]
  ) {
    return function (metadata: AS.Metadata, argv: AS.Value[]) {
      checkArity(metadata, argv, arity)
      const _argv = checkType(metadata, argv.map(strict), argType)
      const values = _argv.map(
        (arg: InstanceType<ArgValue>) => arg.value as ArgInnerValue
      )
      return retWrapper(_fn(...values))
    }
  }

  function _wrap2(
    fnName: 'log' | 'sin' | 'asin' | 'cos' | 'acos' | 'tan' | 'atan'
  ) {
    return function (metadata: AS.Metadata, argv: AS.Value[]) {
      checkArity(metadata, argv, 1)
      const _argv = checkType(metadata, [strict(argv[0])], AS.NumberV)
      if (isType(_argv, AS.RealV)) {
        const value = Math[fnName](Number(_argv[0].value))
        if (!isNaN(value)) return new AS.FloatV(value)
      }
      return new AS.ComplexV(toComplex(_argv[0].value)[fnName]())
    }
  }

  function _wrapRound(_rounder: (x: number) => number) {
    return function (metadata: AS.Metadata, argv: AS.Value[]) {
      checkArity(metadata, argv, 1)
      const [arg] = checkType(metadata, [strict(argv[0])], AS.RealV)
      if (arg instanceof AS.IntegerV) return arg
      const _arg = BigInt(_rounder(arg.value))
      return new AS.IntegerV(_arg)
    }
  }
  const _atan1 = _wrap2('atan')
  const _atan2 = _wrap(Math.atan2, 2, _wrapType(AS.FloatV), AS.RealV)
  function _atan(metadata: AS.Metadata, argv: AS.Value[]) {
    return argv.length === 2 ? _atan2(metadata, argv) : _atan1(metadata, argv)
  }
  return {
    ㅅ: {
      ㅂ: Math.PI,
      ㅈ: Math.E,
      ㅁ: Infinity,
      ㄴ: NaN,
      ㄱ: _wrap(
        (a: JSNumber, b: JSNumber) => isclose(a, b),
        2,
        _wrapType(AS.BooleanV),
        AS.NumberV
      ),
      ㄴㄴ: _wrap(isnan, 1, _wrapType(AS.BooleanV), AS.NumberV),
      ㅁㄴ: _wrap(isinf, 1, _wrapType(AS.BooleanV), AS.NumberV),
      ㅈㄷ: _wrap(abs, 1, wrapNumber, AS.NumberV),
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
