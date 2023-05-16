/**
 * Number operations made generic of argument types
 */

import BigInteger from 'big-integer'
import Complex from 'complex.js'

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

Complex.prototype.add = function (a, b) {
  var z = new Complex(a, b)
  return new Complex(this['re'] + z['re'], this['im'] + z['im'])
}
Complex.prototype.mul = function (a, b) {
  var z = new Complex(a, b)
  return new Complex(
    this['re'] * z['re'] - this['im'] * z['im'],
    this['re'] * z['im'] + this['im'] * z['re']
  )
}

function _isBothIntegers(a, b) {
  return a instanceof BigInteger && b instanceof BigInteger
}

function _isBothReal(a, b) {
  return !(a instanceof Complex || b instanceof Complex)
}

function _toReal(x) {
  return x instanceof Complex ? x.valueOf() : x
}

export function toComplex(x) {
  if (x instanceof BigInteger) x = x.valueOf()
  return Complex(x)
}

/* Logic */
export function isinf(num) {
  if (num instanceof BigInteger) return false
  if (num instanceof Complex) return isinf(num.re) || isinf(num.im)
  return !(isFinite(num) || isNaN(num))
}
export function isnan(num) {
  if (num instanceof BigInteger) return false
  if (num instanceof Complex) return num.isNaN()
  return isNaN(num)
}

export function eq(a, b) {
  try {
    // error if any of them are not a whole number in value
    return BigInteger(_toReal(a)).eq(_toReal(b))
  } catch (e) {
    if (a instanceof Complex && b instanceof Complex) {
      return (a.re === b.re && a.im === b.re) || a.equals(b)
    }
    return a == b
  }
}

export function isclose(a, b, rel_tol = 1e-9, abs_tol = 1e-16) {
  // assume a & b Complex
  if (rel_tol < 0 || abs_tol < 0) {
    throw RangeError('Tolerances must be non-negative.')
  }
  if (eq(a, b)) {
    return true
  }
  if (isinf(a) || isinf(b)) {
    return false
  }
  const diff = abs(sub(a, b))
  return diff <= rel_tol * abs(b) || diff <= rel_tol * abs(a) || diff <= abs_tol
}

/* Arithmetics */
export function abs(num) {
  if (num instanceof BigInteger) {
    return num.abs()
  } else if (num instanceof Complex) {
    return num.abs()
  }
  return Math.abs(num)
}

export function add(a, b) {
  if (_isBothIntegers(a, b)) {
    return a.plus(b)
  } else if (a instanceof Complex) {
    return a.add(toComplex(b))
  } else if (b instanceof Complex) {
    return b.add(toComplex(a))
  }
  return a + b
}
export function sub(a, b) {
  if (_isBothIntegers(a, b)) {
    return a.minus(b)
  } else if (a instanceof Complex) {
    return a.sub(toComplex(b))
  } else if (b instanceof Complex) {
    return b.sub(toComplex(a))
  }
  return a - b
}
export function mul(a, b) {
  if (_isBothIntegers(a, b)) {
    return a.times(b)
  } else if (a instanceof Complex) {
    return a.mul(toComplex(b))
  } else if (b instanceof Complex) {
    return b.mul(toComplex(a))
  }
  return a * b
}
export function div(a, b) {
  // integer division
  if (_isBothIntegers(a, b)) {
    return a.divide(b)
  }
  return Math.trunc(a / b)
}
export function mod(a, b) {
  if (_isBothIntegers(a, b)) {
    return a.mod(b)
  }
  return a % b
}

export function pow(a, b) {
  if (_isBothIntegers(a, b) && b.isPositive()) {
    return a.pow(b)
  } else if (_isBothReal(a, b)) {
    let value = Math.pow(a, b)
    if (!isNaN(value)) return value
  }
  return toComplex(a).pow(toComplex(b))
}
