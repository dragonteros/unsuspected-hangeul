/** Useful utilities **/
import * as AS from './abstractSyntax.js'

function isLiteralExpr(expr) {
  return (expr instanceof AS.ExprV) && (expr.expr instanceof AS.Literal)
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
    Object.keys(d).forEach(function (k) {
      result[k] = recursiveMap(d[k], fn)
    })
    return new AS.DictV(result)
  }
  return item
}

/* Argument constraint checkers */
function _forceArray(condition) {
  return Array.isArray(condition) ? condition : [condition]
}

function isType(argv, desiredTypes) {
  function matches(desiredType) {
    return _forceArray(argv).every(function (arg) {
      return arg instanceof desiredType
    })
  }
  return _forceArray(desiredTypes).some(matches)
}

function checkType(argv, desiredTypes) {
  if (isType(argv, desiredTypes)) return
  throw TypeError(
    'args of type ' + desiredTypes + ' expected but received: ' + argv.map(a => a.constructor)
  )
}

function checkArity(argv, desiredArities) {
  desiredArities = _forceArray(desiredArities)
  if (desiredArities.indexOf(argv.length) !== -1) return
  throw SyntaxError(
    desiredArities + 'args expected but received ' + argv.length
  )
}

function checkMinArity(argv, minimumArity) {
  if (argv.length >= minimumArity) return
  throw SyntaxError('At least ' + minimumArity + 'args expected but received ' + argv.length)
}

/* Converts the value into string for hashing */
function toString(value, strict, ioUtils, formatIO) {
  const _partial = v => toString(v, strict, ioUtils, formatIO)
  value = strict(value)
  if (ioUtils && value instanceof AS.IOV) {
    value = ioUtils.doIO(value, ioUtils)
    value = _partial(value)
    return formatIO? 'IO(' + value + ')': value
  }

  if (value instanceof AS.NumberV) {
    return value.value.toString()
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
  isType,
  checkType,
  checkArity,
  checkMinArity,
  toString
}
