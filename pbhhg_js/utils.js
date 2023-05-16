/** Useful utilities **/
import * as AS from './abstractSyntax.js'
import * as E from './error.js'

export function isLiteralExpr(expr) {
  return expr instanceof AS.ExprV && expr.expr instanceof AS.Literal
}

export function extractValue(arg) {
  return arg.value
}

export function chooseConstructorLike(item, candidates) {
  return candidates.find((f) => item instanceof f)
}

export function recursiveMap(item, fn) {
  item = fn(item)
  if (item instanceof AS.ListV) {
    return new AS.ListV(item.value.map((v) => recursiveMap(v, fn)))
  }
  if (item instanceof AS.DictV) {
    const d = item.value
    const result = {}
    Object.keys(d).forEach(function (k) {
      result[k] = recursiveMap(d[k], fn)
    })
    return new AS.DictV(result)
  }
  if (item instanceof AS.ErrorV) {
    return new AS.ErrorV(
      item.metadatas,
      item.message,
      item.value.map((v) => recursiveMap(v, fn))
    )
  }
  return item
}

export function allEqual(arr) {
  if (arr.length === 0) return true
  return arr.every(function (a) {
    return a === arr[0]
  })
}

/* Argument constraint checkers */
function _forceArray(condition) {
  return Array.isArray(condition) ? condition : [condition]
}

export function isType(argv, desiredTypes) {
  desiredTypes = _forceArray(desiredTypes)
  function _matches(arg) {
    return desiredTypes.some(function (desiredType) {
      return arg instanceof desiredType
    })
  }
  return _forceArray(argv).every(_matches)
}

export function isSameType(argv) {
  argv = _forceArray(argv)
  return allEqual(argv.map((a) => a.constructor))
}

function _formatArray(arr, conj = ', ') {
  return arr.join(conj)
}

export function checkType(metadata, argv, desiredTypes) {
  argv = _forceArray(argv)
  desiredTypes = _forceArray(desiredTypes)
  if (isType(argv, desiredTypes)) return
  const desiredTypeNames = desiredTypes.map((t) => t.displayName)
  const argTypeNames = argv.map((a) => a.constructor.displayName)
  throw new E.UnsuspectedHangeulTypeError(
    metadata,
    `인수를 ${_formatArray(desiredTypeNames)} 중에서 주어야 하는데 ` +
      `${_formatArray(argTypeNames)}를 주었습니다.`
  )
}

export function checkSameType(metadata, argv) {
  argv = _forceArray(argv)
  if (isSameType(argv)) return
  argTypeNames = argv.map((a) => a.constructor.displayName)
  throw new E.UnsuspectedHangeulTypeError(
    metadata,
    'Expected arguments of the same type but received ' +
      _formatArray(argTypeNames)
  )
}

export function checkArity(metadata, argv, desiredArities) {
  desiredArities = _forceArray(desiredArities)
  if (desiredArities.indexOf(argv.length) !== -1) return
  throw new E.UnsuspectedHangeulValueError(
    metadata,
    `인수를 ${_formatArray(desiredArities, '개나 ')}개를 주어야 하는데 ` +
      `${argv.length}개의 인수를 주었습니다.`
  )
}

export function checkMinArity(metadata, argv, minimumArity) {
  if (argv.length >= minimumArity) return
  throw new E.UnsuspectedHangeulValueError(
    metadata,
    `인수를 ${minimumArity}개 이상 주어야 하는데` +
      `${argv.length}개 주었습니다.`
  )
}

export function checkMaxArity(metadata, argv, maximumArity) {
  if (argv.length <= maximumArity) return
  throw new E.UnsuspectedHangeulValueError(
    metadata,
    `인수를 ${maximumArity}개 이하 주어야 하는데` +
      `${argv.length}개 주었습니다.`
  )
}

export function matchDefaults(metadata, argv, arity, defaults) {
  if (defaults === undefined) {
    defaults = []
  }
  checkMaxArity(metadata, argv, arity)
  checkMinArity(metadata, argv, arity - defaults.length)
  if (argv.length < arity) {
    let deficiency = arity - argv.length
    argv = argv.concat(defaults.slice(-deficiency))
  }
  return argv
}

/* Converts the value into string for display */
export function toString(value, strict, ioUtils, formatIO) {
  const _partial = (v) => toString(v, strict, ioUtils, formatIO)
  value = strict(value)
  if (ioUtils && value instanceof AS.IOV) {
    value = ioUtils.doIO(value, ioUtils)
    value = _partial(value)
    return formatIO ? 'IO(' + value + ')' : value
  }

  if (value instanceof AS.IntegerV) {
    return value.value.toString()
  } else if (isType(value, AS.NumberV)) {
    return value.toString()
  } else if (value instanceof AS.BooleanV) {
    return value.value ? 'True' : 'False'
  } else if (value instanceof AS.StringV) {
    return "'" + value.value + "'"
  } else if (isType(value, [AS.BytesV, AS.FunctionV])) {
    return value.toString()
  } else if (value instanceof AS.ListV) {
    return '[' + value.value.map(_partial).join(', ') + ']'
  } else if (value instanceof AS.DictV) {
    const keys = value.keys()
    const pairs = keys.map((k) => k + ': ' + _partial(value.value[k]))
    return '{' + pairs.join(', ') + '}'
  } else if (value instanceof AS.IOV) {
    const argvStr = value.argv.map(_partial).join(',')
    return '<IO ' + value.inst + ' (' + argvStr + ')>'
  } else if (value instanceof AS.NilV) {
    return 'Nil'
  }
  throw EvalError('Unexpected value: ' + value)
}
