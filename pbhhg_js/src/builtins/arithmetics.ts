import Complex from 'complex.js'

import * as AS from '../abstractSyntax'
import * as E from '../error'
import { add, div, mod, mul, pow } from '../numbers'
import {
  checkArity,
  checkMinArity,
  checkType,
  extractValue,
  isType,
} from '../utils'

function _joinArrayBuffer(bufs: ArrayBuffer[]) {
  const size = bufs.map((a) => a.byteLength).reduce((a, b) => a + b, 0)
  const newBuf = new ArrayBuffer(size)
  const view = new Uint8Array(newBuf)
  bufs.reduce(function (idx, buf) {
    view.set(new Uint8Array(buf), idx)
    return idx + buf.byteLength
  }, 0)
  return newBuf
}

export function wrapNumber(num: bigint | number | Complex) {
  if (typeof num === 'bigint') return new AS.IntegerV(num)
  if (num instanceof Complex) return new AS.ComplexV(num)
  return new AS.FloatV(num)
}

/** Returns (g, x, y) such that a*x + b*y = g = gcd(a, b) */
function extendedGcd(a: bigint, b: bigint): [bigint, bigint, bigint] {
  let [x, x_old, y, y_old] = [0n, 1n, 1n, 0n]
  while (a !== 0n) {
    const quotient = b / a
    ;[a, b] = [b % a, a]
    ;[y, y_old] = [y_old, y - quotient * y_old]
    ;[x, x_old] = [x_old, x - quotient * x_old]
  }
  return [b, x, y]
}

function modularInverse(num: bigint, modulo: bigint) {
  const [g, inverse, _] = extendedGcd(num % modulo, modulo)
  if (g === 1n) return inverse % modulo
  throw Error(`법 ${modulo}에 대한 ${num}의 역원이 없습니다.`)
}

function modPow(base: bigint, exponent: bigint, modulo: bigint): bigint {
  base = base % modulo
  let result = 1n
  if (exponent < 0n) {
    exponent = -exponent
    base = modularInverse(base, modulo)
  }
  while (exponent > 0n) {
    if (base === 0n) return 0n
    if (exponent % 2n === 1n) result = (result * base) % modulo
    exponent /= 2n
    base = base ** 2n % modulo
  }
  return result
}

export default function (
  procFunctional: AS.ProcFunctionalFn,
  strict: AS.StrictFn,
  loadUtils: AS.LoadUtils
): Record<string, AS.Evaluation> {
  function _multiply(metadata: AS.Metadata, argv: AS.Value[]) {
    checkMinArity(metadata, argv, 1)
    const first = checkType(
      metadata,
      [strict(argv[0])],
      [AS.BooleanV, ...AS.NumberV]
    )
    if (isType(first, AS.NumberV)) {
      const _argv = checkType(metadata, argv.map(strict), AS.NumberV)
      return wrapNumber(_argv.map((arg) => arg.value).reduce(mul))
    }

    // short-circuiting
    for (const arg of argv) {
      const [_arg] = checkType(metadata, [strict(arg)], [AS.BooleanV])
      if (!_arg.value) return new AS.BooleanV(false)
    }
    return new AS.BooleanV(true)
  }

  function _add(metadata: AS.Metadata, argv: AS.Value[]) {
    checkMinArity(metadata, argv, 1)
    const first = checkType(
      metadata,
      [strict(argv[0])],
      [AS.BooleanV, AS.DictV, ...AS.NumberV, ...AS.SequenceV]
    )
    if (isType(first, [AS.BooleanV])) {
      // short-circuiting
      for (const arg of argv) {
        const [_arg] = checkType(metadata, [strict(arg)], [AS.BooleanV])
        if (_arg.value) return new AS.BooleanV(true)
      }
      return new AS.BooleanV(false)
    }

    if (isType(first, [AS.StringV])) {
      const _argv = checkType(metadata, argv.map(strict), [AS.StringV])
      return new AS.StringV(_argv.map(extractValue).join(''))
    }
    if (isType(first, [AS.BytesV])) {
      const _argv = checkType(metadata, argv.map(strict), [AS.BytesV])
      return new AS.BytesV(_joinArrayBuffer(_argv.map(extractValue)))
    }
    if (isType(first, [AS.ListV])) {
      const _argv = checkType(metadata, argv.map(strict), [AS.ListV])
      return new AS.ListV(_argv.map(extractValue).reduce((a, b) => a.concat(b)))
    }
    if (isType(first, [AS.DictV])) {
      const _argv = checkType(metadata, argv.map(strict), [AS.DictV])
      const result = {}
      _argv.map(extractValue).forEach((d) => Object.assign(result, d))
      return new AS.DictV(result)
    }
    const _argv = checkType(metadata, argv.map(strict), AS.NumberV)
    return wrapNumber(_argv.map((arg) => arg.value).reduce(add))
  }

  function _exponentiate(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, [2, 3])
    const _argv = checkType(metadata, argv.map(strict), AS.NumberV)
    if (_argv.length === 3) {
      const [base, exp, mod] = checkType(metadata, _argv, [AS.IntegerV])
      try {
        return new AS.IntegerV(modPow(base.value, exp.value, mod.value))
      } catch (err) {
        if (err instanceof Error) {
          throw new E.UnsuspectedHangeulArithmeticError(metadata, err.message)
        }
        throw err
      }
    }
    checkArity(metadata, _argv, 2)
    try {
      return wrapNumber(pow(_argv[0].value, _argv[1].value))
    } catch (error) {
      if (error instanceof Error) {
        throw new E.UnsuspectedHangeulArithmeticError(metadata, error.message)
      }
      throw error
    }
  }

  function _integerDivision(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 2)
    const _argv = checkType(metadata, argv.map(strict), AS.RealV)
    try {
      return wrapNumber(div(_argv[0].value, _argv[1].value))
    } catch (error) {
      if (error instanceof RangeError) {
        throw new E.UnsuspectedHangeulArithmeticError(
          metadata,
          '0의 역수를 구하려고 했습니다.'
        )
      }
      throw error
    }
  }

  function _remainder(metadata: AS.Metadata, argv: AS.Value[]) {
    checkArity(metadata, argv, 2)
    const _argv = checkType(metadata, argv.map(strict), AS.RealV)
    try {
      return wrapNumber(mod(_argv[0].value, _argv[1].value))
    } catch (error) {
      if (error instanceof RangeError) {
        throw new E.UnsuspectedHangeulArithmeticError(
          metadata,
          '0의 역수를 구하려고 했습니다.'
        )
      }
      throw error
    }
  }

  return {
    ㄱ: _multiply,
    ㄷ: _add,
    ㅅ: _exponentiate,
    ㄴㄴ: _integerDivision,
    ㄴㅁ: _remainder,
  }
}
