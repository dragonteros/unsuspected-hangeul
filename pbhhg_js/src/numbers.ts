/**
 * Number operations made generic of argument types
 */

import Complex from 'complex.js'

export type JSNumber = number | bigint | Complex

Math.trunc =
  Math.trunc ||
  function (x) {
    if (isNaN(x)) {
      return NaN
    }
    if (x > 0) {
      return Math.floor(x)
    }
    return Math.ceil(x)
  }

export function toComplex(x: JSNumber | string): Complex {
  const num = typeof x === 'bigint' ? Number(x) : x
  return new Complex(num)
}

export function arrayToInt(
  bigEndianArr: (number | bigint)[] | string,
  radix: number | bigint = 10n
) {
  const _radix = BigInt(radix)
  const arr =
    typeof bigEndianArr === 'string'
      ? bigEndianArr.split('').map(BigInt)
      : bigEndianArr
  let result = 0n
  for (let i = 0; i < arr.length; i++) {
    result *= _radix
    result += BigInt(arr[i])
  }
  return result
}
export function intToArray(num: bigint, radix: number | bigint = 10n) {
  if (num < 0n)
    throw Error('Cannot convert a negative integer into array form.')
  const _radix = BigInt(radix)
  const littleEndianArr: bigint[] = []
  while (num > 0n) {
    littleEndianArr.push(num % _radix)
    num /= _radix
  }
  return littleEndianArr.reverse()
}

/* Logic */
export function isinf(num: JSNumber): boolean {
  if (typeof num === 'bigint') return false
  if (num instanceof Complex) return isinf(num.re) || isinf(num.im)
  return !(isFinite(num) || isNaN(num))
}
export function isnan(num: JSNumber): boolean {
  if (typeof num === 'bigint') return false
  if (num instanceof Complex) return num.isNaN()
  return isNaN(num)
}

function complexEq(complexValue: Complex, numberValue: JSNumber): boolean {
  if (numberValue instanceof Complex) {
    return (
      complexValue.re === numberValue.re && complexValue.im === numberValue.im
    )
  }
  if (complexValue.im !== 0) return false
  if (typeof numberValue === 'bigint')
    return bigIntEq(numberValue, complexValue.re)
  return numberValue === complexValue.re
}
function bigIntEq(bigIntValue: bigint, realValue: number | bigint): boolean {
  if (typeof realValue === 'bigint') return bigIntValue === realValue
  if (Number.isInteger(realValue)) return bigIntValue === BigInt(realValue)
  return false
}
export function eq(a: JSNumber, b: JSNumber) {
  if (a instanceof Complex) return complexEq(a, b)
  if (b instanceof Complex) return complexEq(b, a)
  if (typeof a === 'bigint') return bigIntEq(a, b)
  if (typeof b === 'bigint') return bigIntEq(b, a)
  return a === b
}

export function isclose(
  a: JSNumber,
  b: JSNumber,
  rel_tol = 1e-9,
  abs_tol = 1e-16
) {
  if (rel_tol < 0 || abs_tol < 0) {
    throw RangeError('Tolerances must be non-negative.')
  }
  if (eq(a, b)) {
    return true
  }
  if (isinf(a) || isinf(b)) {
    return false
  }
  const _a = typeof a === 'bigint' ? Number(a) : a
  const _b = typeof b === 'bigint' ? Number(b) : b
  const diff = abs(sub(_a, _b))
  return (
    diff <= rel_tol * abs(_b) || diff <= rel_tol * abs(_a) || diff <= abs_tol
  )
}

/* Arithmetics */
export function abs(num: bigint): bigint
export function abs(num: number | Complex): number
export function abs(num: JSNumber): JSNumber
export function abs(num: JSNumber) {
  if (typeof num === 'bigint') {
    return num >= 0n ? num : -num
  } else if (num instanceof Complex) {
    return num.abs()
  }
  return Math.abs(num)
}

export function add(a: JSNumber, b: JSNumber) {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a + b
  } else if (a instanceof Complex) {
    return a.add(toComplex(b))
  } else if (b instanceof Complex) {
    return b.add(toComplex(a))
  }
  return Number(a) + Number(b)
}
export function sub(a: bigint, b: bigint): bigint
export function sub(a: bigint | number, b: bigint | number): number
export function sub(a: JSNumber, b: JSNumber): Complex
export function sub(a: JSNumber, b: JSNumber): JSNumber {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a - b
  } else if (a instanceof Complex) {
    return a.sub(toComplex(b))
  } else if (b instanceof Complex) {
    return b.sub(toComplex(a))
  }
  return Number(a) - Number(b)
}
export function mul(a: JSNumber, b: JSNumber) {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a * b
  } else if (a instanceof Complex) {
    return a.mul(toComplex(b))
  } else if (b instanceof Complex) {
    return b.mul(toComplex(a))
  }
  return Number(a) * Number(b)
}
export function div(a: number | bigint, b: number | bigint) {
  // integer division
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a / b
  }
  return Math.trunc(Number(a) / Number(b))
}
export function mod(a: number | bigint, b: number | bigint) {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a % b
  }
  return Number(a) % Number(b)
}

export function pow(a: JSNumber, b: JSNumber) {
  if (typeof a === 'bigint' && typeof b === 'bigint' && b >= 0) {
    return a ** b
  } else if (!(a instanceof Complex) && !(b instanceof Complex)) {
    const value = Math.pow(Number(a), Number(b))
    if (!isNaN(value)) return value
  }
  return toComplex(a).pow(toComplex(b))
}
