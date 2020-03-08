/** Useful utilities **/
import * as AS from './abstractSyntax.js'

function isLiteralExpr(expr) {
  return expr instanceof AS.ExprV && expr.expr instanceof AS.Literal
}

function extractValue(arg) {
  return arg.value
}

function chooseConstructorLike(item, candidates) {
  return candidates.find(f => item instanceof f)
}

function recursiveMap(item, fn) {
  item = fn(item)
  if (item instanceof AS.ListV) {
    return new AS.ListV(item.value.map(v => recursiveMap(v, fn)))
  }
  if (item instanceof AS.DictV) {
    const d = item.value
    const result = {}
    Object.keys(d).forEach(function(k) {
      result[k] = recursiveMap(d[k], fn)
    })
    return new AS.DictV(result)
  }
  return item
}

function allEqual(arr) {
  if (arr.length === 0) return true
  return arr.every(function(a) {
    return a === arr[0]
  })
}

/* Argument constraint checkers */
function _forceArray(condition) {
  return Array.isArray(condition) ? condition : [condition]
}

function isType(argv, desiredTypes) {
  desiredTypes = _forceArray(desiredTypes)
  function _matches(arg) {
    return desiredTypes.some(function(desiredType) {
      return arg instanceof desiredType
    })
  }
  return _forceArray(argv).every(_matches)
}

function isSameType(argv) {
  argv = _forceArray(argv)
  return allEqual(argv.map(a => a.constructor))
}

function _formatArray(arr, conj = 'and') {
  if (arr.length < 2) return arr.toString()
  return arr
    .slice(0, -1)
    .join(', ')
    .concat(' ', conj, ' ', arr[arr.length - 1])
}

function checkType(argv, desiredTypes) {
  argv = _forceArray(argv)
  desiredTypes = _forceArray(desiredTypes)
  if (isType(argv, desiredTypes)) return
  const desiredTypeNames = desiredTypes.map(t => t.displayName)
  const argTypeNames = argv.map(a => a.constructor.displayName)
  throw TypeError(
    'Expected arguments of the same type among ' +
      _formatArray(desiredTypeNames) +
      ' but received ' +
      _formatArray(argTypeNames)
  )
}

function checkSameType(argv) {
  argv = _forceArray(argv)
  if (isSameType(argv)) return
  argTypeNames = argv.map(a => a.constructor.displayName)
  throw TypeError(
    'Expected arguments of the same type but received ' +
      _formatArray(argTypeNames)
  )
}

function checkArity(argv, desiredArities) {
  desiredArities = _forceArray(desiredArities)
  if (desiredArities.indexOf(argv.length) !== -1) return
  throw SyntaxError(
    'Expected ' +
      _formatArray(desiredArities, 'or') +
      ' arguments but received ' +
      argv.length
  )
}

function checkMinArity(argv, minimumArity) {
  if (argv.length >= minimumArity) return
  throw SyntaxError(
    'Expected at least ' +
      minimumArity +
      ' arguments expected but received ' +
      argv.length
  )
}

function checkMaxArity(argv, maximumArity) {
  if (argv.length <= maximumArity) return
  throw SyntaxError(
    'Expected at most ' +
      maximumArity +
      ' arguments expected but received ' +
      argv.length
  )
}

function matchDefaults(argv, arity, defaults) {
  if (defaults === undefined) {
    defaults = []
  }
  checkMaxArity(argv, arity)
  checkMinArity(argv, arity - defaults.length)
  if (argv.length < arity) {
    let deficiency = arity - argv.length
    argv = argv.concat(defaults.slice(-deficiency))
  }
  return argv
}

/* Converts the value into string for hashing */
function toString(value, strict, ioUtils, formatIO) {
  const _partial = v => toString(v, strict, ioUtils, formatIO)
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
    const pairs = keys.map(k => k + ': ' + _partial(value.value[k]))
    return '{' + pairs.join(', ') + '}'
  } else if (value instanceof AS.IOV) {
    const argvStr = value.argv.map(_partial).join(',')
    return '<IO ' + value.inst + ' (' + argvStr + ')>'
  } else if (value instanceof AS.NilV) {
    return 'Nil'
  }
  throw EvalError('Unexpected value: ' + value)
}

export {
  isLiteralExpr,
  extractValue,
  chooseConstructorLike,
  recursiveMap,
  allEqual,
  isType,
  isSameType,
  checkType,
  checkSameType,
  checkArity,
  checkMinArity,
  checkMaxArity,
  matchDefaults,
  toString
}
