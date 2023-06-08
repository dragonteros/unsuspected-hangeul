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
function toRealIfPossible(x: JSNumber): JSNumber {
  if (typeof x === 'bigint' || typeof x === 'number') return x
  if (isclose(x.im, 0)) return x.re
  return x
}

export function arrayToInt(
  bigEndianArr: (number | bigint)[] | string,
  radix: number | bigint = 10n
) {
  const TABLE = '0123456789abcdefghijklmnopqrstuvwxyz'.slice(0, Number(radix))
  const _radix = BigInt(radix)
  let arr: (number | bigint)[]
  let sign: 1n | -1n = 1n
  if (typeof bigEndianArr === 'string') {
    if (bigEndianArr[0] === '+') {
      bigEndianArr = bigEndianArr.slice(1)
    } else if (bigEndianArr[0] === '-') {
      sign = -1n
      bigEndianArr = bigEndianArr.slice(1)
    }

    arr = bigEndianArr
      .toLowerCase()
      .split('')
      .map((c) => TABLE.indexOf(c))
    const invalidIdx = arr.indexOf(-1)
    if (invalidIdx !== -1) {
      throw Error(
        `다음 글자를 ${radix}진법 숫자로 해석할 수 없습니다: '${bigEndianArr[invalidIdx]}'`
      )
    }
  } else {
    arr = bigEndianArr
  }
  let result = 0n
  for (let i = 0; i < arr.length; i++) {
    result *= _radix
    result += BigInt(arr[i])
  }
  return result * sign
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
function isInteger(num: bigint | number) {
  return typeof num === 'bigint' || Number.isInteger(num)
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
  return isInteger(realValue) && bigIntValue === BigInt(realValue)
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

function complexAdd(a: Complex, b: Complex): Complex {
  return new Complex(a.re + b.re, a.im + b.im)
}
export function add(a: JSNumber, b: JSNumber) {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a + b
  }
  if (a instanceof Complex || b instanceof Complex) {
    return complexAdd(toComplex(a), toComplex(b))
  }
  return Number(a) + Number(b)
}
function sub(a: bigint, b: bigint): bigint
function sub(a: bigint | number, b: bigint | number): number
function sub(a: JSNumber, b: JSNumber): Complex
function sub(a: JSNumber, b: JSNumber): JSNumber {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a - b
  }
  if (a instanceof Complex || b instanceof Complex) {
    return toComplex(a).sub(toComplex(b))
  }
  return Number(a) - Number(b)
}
function complexMul(a: Complex, b: Complex): Complex {
  return new Complex(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re)
}
export function mul(a: JSNumber, b: JSNumber) {
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a * b
  }
  if (a instanceof Complex || b instanceof Complex) {
    return complexMul(toComplex(a), toComplex(b))
  }
  return Number(a) * Number(b)
}
export function div(a: number | bigint, b: number | bigint) {
  // integer division
  if (Number(b) === 0) throw Error('0으로 나눌 수 없습니다.')
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a / b
  }
  return Math.trunc(Number(a) / Number(b))
}
export function mod(a: number | bigint, b: number | bigint) {
  if (Number(b) === 0) throw Error('0으로 나눌 수 없습니다.')
  if (typeof a === 'bigint' && typeof b === 'bigint') {
    return a % b
  }
  return Number(a) % Number(b)
}

export function pow(a: JSNumber, b: JSNumber) {
  if (typeof a === 'bigint' && typeof b === 'bigint' && b >= 0) {
    return a ** b
  }

  const bReal = toRealIfPossible(b)
  if (!(bReal instanceof Complex) && bReal < 0 && eq(a, 0))
    throw Error('0의 역수를 구하려고 했습니다.')

  if (
    a instanceof Complex ||
    b instanceof Complex ||
    (a < 0 && !isInteger(b))
  ) {
    return toComplex(a).pow(toComplex(b))
  }

  return Number(a) === 1 ? 1 : Math.pow(Number(a), Number(b))
}
