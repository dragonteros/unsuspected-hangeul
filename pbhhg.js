/** Normalizer **/

/* Normalizes each character into standard form */
function normalizeChar (c) {
  function getidx (ref, divisor = 1) {
    return Math.floor((c.charCodeAt(0) - ref.charCodeAt(0)) / divisor)
  }
  // note all ㅇ and ㅎ has a preceding space in following tables
  var jamo = [
    'ㄱ',
    'ㄱ',
    'ㄱㅅ',
    'ㄴ',
    'ㄴㅈ',
    'ㄴ ㅎ',
    'ㄷ',
    'ㄷ',
    'ㄹ',
    'ㄹㄱ',
    'ㄹㅁ',
    'ㄹㅂ',
    'ㄹㅅ',
    'ㄹㄷ',
    'ㄹㅂ',
    'ㄹ ㅎ',
    'ㅁ',
    'ㅂ',
    'ㅂ',
    'ㅂㅅ',
    'ㅅ',
    'ㅅ',
    ' ㅇ',
    'ㅈ',
    'ㅈ',
    'ㅈ',
    'ㄱ',
    'ㄷ',
    'ㅂ',
    ' ㅎ'
  ]
  var choseong = [
    'ㄱ',
    'ㄱ',
    'ㄴ',
    'ㄷ',
    'ㄷ',
    'ㄹ',
    'ㅁ',
    'ㅂ',
    'ㅂ',
    'ㅅ',
    'ㅅ',
    ' ㅇ',
    'ㅈ',
    'ㅈ',
    'ㅈ',
    'ㄱ',
    'ㄷ',
    'ㅂ',
    ' ㅎ'
  ]
  if (c.length !== 1) {
    throw Error(
      '[normalizeChar] Length of string should be 1, not ' + c.length + ': ' + c
    )
  }
  if (c >= 'ㄱ' && c <= 'ㅎ') {
    return jamo[getidx('ㄱ')]
  } else if (c >= '가' && c <= '힣') {
    return choseong[getidx('가', 588)]
  } else if (c >= '\u1100' && c <= '\u1112') {
    // 첫가끝 초성
    return choseong[getidx('\u1100')]
  } else if (c >= '\uFFA1' && c <= '\uFFBE') {
    // 반각
    return jamo[getidx('\uFFA1')]
  } else return ' '
}

/* Parses jamo-encoded variable length integer into JS Number */
function parseNumber (s) {
  var tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
  var varlen = s.split('').map(function (c) {
    return tbl.indexOf(c)
  })
  if (varlen.indexOf(-1) !== -1) {
    throw SyntaxError('Argument ' + s + ' has an unsupported character')
  }
  var num = parseInt(varlen.reverse().join(''), 8)
  if (s.length % 2 === 0) {
    num = -num
  }
  return num
}

/** Parser **/

/* AST */
function Literal (value) {
  this.value = value // int
}
function FunRef (rel) {
  this.rel = rel // int
}
function ArgRef (relA, relF) {
  this.relA = relA
  this.relF = relF // int
}
function FunDef (body) {
  this.body = body
}
function BuiltinFun (id) {
  // int
  this.id = id
}
function FunCall (fun, argv) {
  this.fun = fun
  this.argv = argv
}

/* Parses concrete syntax to abstract syntax
Args:
    word: string. word to parse
    stack: list of parsed legal arguments so far that we will modify
*/
function parseWord (word, stack) {
  if (word.indexOf('ㅎ') !== -1) {
    var arity = word.slice(1)

    if (arity) {
      // FunCall
      arity = parseNumber(arity)
      if (arity < 0) {
        throw SyntaxError(
          'Function call with negative number of arguments: ' + arity
        )
      }

      var fun = stack.pop()
      if (fun instanceof Literal) {
        fun = new BuiltinFun(fun.value)
      }

      if (arity === 0) {
        stack.push(new FunCall(fun, []))
      } else {
        var argv = stack.splice(-arity, arity)
        if (argv.length < arity) {
          throw SyntaxError(
            'Function call required ' +
              arity +
              ' arguments but there are only ' +
              argv.length
          )
        }
        stack.push(new FunCall(fun, argv))
      }
    } else {
      // FunDef
      var body = stack.pop()
      stack.push(new FunDef(body))
    }
  } else if (word.indexOf('ㅇ') !== -1) {
    var trailer = word.slice(1)
    var relF
    if (trailer) {
      // ArgRef
      var relA = stack.pop()
      relF = parseNumber(trailer)
      stack.push(new ArgRef(relA, relF))
    } else {
      // FunRef
      relF = stack.pop()
      if (relF instanceof Literal) {
        relF = relF.value
      } else {
        throw SyntaxError(
          'Function reference admits integer literals only, ' +
            'but received:' + relF
        )
      }
      stack.push(new FunRef(relF))
    }
  } else {
    stack.push(new Literal(parseNumber(word)))
  }
}

/* Parses program into abstract syntax */
function parse (sentence) {
  sentence = sentence
    .split('')
    .map(normalizeChar)
    .join('')
  var words = sentence.split(' ')
  var stack = []
  var len = words.length
  for (var i = 0; i < len; i++) {
    if (words[i]) parseWord(words[i], stack)
  }
  return stack
}

/** Interpreter **/

/* Values */
function Env (funs, args) {
  this.funs = funs
  this.args = args
}

function NumberV (value) {
  this.value = value
}
function BooleanV (value) {
  this.value = value
}
function ListV (value) {
  this.value = value
}
function StringV (value) {
  this.value = value
}
function ClosureV (body, env) {
  this.body = body
  this.env = env
}
function IOV (inst, argv) {
  this.inst = inst
  this.argv = argv
}
function NilV () {
}
function ExprV (expr, env, cache) {
  this.expr = expr
  this.env = env
  this.cache = cache
}
var AnyV = [NumberV, BooleanV, ClosureV, ListV, StringV, IOV, NilV]

/* Argument constraint checkers */
function _forceArray (condition) {
  return Array.isArray(condition) ? condition : [condition]
}

function isType (argv, desiredTypes) {
  function matches (desiredType) {
    return _forceArray(argv).every(function (arg) {
      return arg instanceof desiredType
    })
  }
  return _forceArray(desiredTypes).some(matches)
}

function checkType (argv, desiredTypes) {
  if (isType(argv, desiredTypes)) return
  throw TypeError(
    'Arguments of type ' + desiredTypes + ' expected but received: ' + argv
  )
}

function checkArity (argv, desiredArities) {
  desiredArities = _forceArray(desiredArities)
  if (desiredArities.indexOf(argv.length) !== -1) return
  throw SyntaxError(
    desiredArities + 'arguments expected but received ' + argv.length
  )
}

function checkMinArity (argv, minimumArity) {
  if (argv.length >= minimumArity) return
  throw SyntaxError('At least ' + minimumArity + 'arguments expected but received ' + argv.length)
}

/* Builtin functions */
function _extractValue (arg) {
  return arg.value
}

function _allEqual (arr) {
  if (arr.length === 0) return true
  return arr.every(function (a) {
    return a === arr[0]
  })
}

function _listedEquals (arrs) {
  if (arrs.length === 0) return true
  if (!_allEqual(arrs.map(function (arr) { return arr.length }))) { return false }
  var len = arrs[0].length
  for (var i = 0; i < len; i++) { // compare among tiers
    if (!_equals(arrs.map(function (arr) { return arr[i] }))) { return false }
  }
  return true
}

function _equals (argv) {
  argv = argv.map(strict)
  if (!isType(argv, AnyV)) return new BooleanV(false)
  else if (isType(argv, NilV)) return new BooleanV(true)
  else if (isType(argv, ClosureV)) {
    return new BooleanV(_allEqual(argv))
  } else if (isType(argv, ListV)) {
    return new BooleanV(_listedEquals(argv.map(_extractValue)))
  } else if (isType(argv, IOV)) {
    if (!_allEqual(argv.map(function (arg) { return arg.inst }))) {
      return new BooleanV(false)
    }
    return new BooleanV(_listedEquals(argv.map(function (arg) { return arg.argv })))
  } else {
    return new BooleanV(_allEqual(argv.map(_extractValue)))
  }
}

function _exprApply (fun) {
  return function (argv) {
    var cannedEnv = fun.env
    var newEnv = new Env(cannedEnv.funs, cannedEnv.args.concat([argv]))
    return new ExprV(fun.body, newEnv, null)
  }
}

/* Execute the built-in function with given arguments and environement
Args:
    i: Built-in Function ID
    argv: Argument Values for the built-in function
Returns:
    Return value of the built-in function */
function procBuiltin (i, argv) {
  var inst = encodeNumber(i)
  switch (inst) {
    // 산술 연산
    case 'ㄱ':
      checkMinArity(argv, 1)
      argv = argv.map(strict)
      checkType(argv, [NumberV, BooleanV])
      if (isType(argv, BooleanV)) {
        return new BooleanV(argv.every(_extractValue))
      } else {
        return new NumberV(argv.map(_extractValue).reduce(
          function (a, b) { return a * b }, 1))
      }
    case 'ㄷ':
      checkMinArity(argv, 1)
      argv = argv.map(strict)
      checkType(argv, [NumberV, BooleanV, ListV, StringV])
      if (isType(argv, BooleanV)) {
        return new BooleanV(argv.some(_extractValue))
      } else if (isType(argv, StringV)) {
        return new StringV(argv.map(_extractValue).join(''))
      } else if (isType(argv, ListV)) {
        return new ListV(argv.map(_extractValue).reduce(
          function (a, b) { return a.concat(b) }, []))
      } else {
        return new NumberV(argv.map(_extractValue).reduce(
          function (a, b) { return a + b }, 0))
      }
    case 'ㅅ':
      checkArity(argv, 2)
      argv = argv.map(strict)
      checkType(argv, NumberV)
      var power = Math.pow(argv[0].value, argv[1].value)
      return new NumberV(power)

    // 논리 연산
    case 'ㄴ':
      return _equals(argv)
    case 'ㅁ':
      checkArity(argv, 1)
      argv = argv.map(strict)
      checkType(argv, BooleanV)
      return new BooleanV(!argv[0].value)
    case 'ㅈ':
      checkArity(argv, 2)
      argv = argv.map(strict)
      checkType(argv, NumberV)
      return new BooleanV(argv[0].value < argv[1].value)
    case 'ㅈㅈ':
      checkArity(argv, 0)
      return new BooleanV(true)
    case 'ㄱㅈ':
      checkArity(argv, 0)
      return new BooleanV(false)

    // 입력
    case 'ㄹ':
      checkArity(argv, 0)
      return new IOV(inst, argv)
    case 'ㅈㄹ':
      checkArity(argv, 1)
      argv = argv.map(strict)
      checkType(argv, StringV)
      return new IOV(inst, argv)
    case 'ㄱㅅ':
      checkArity(argv, 1)
      return new IOV(inst, argv)
    case 'ㄱㄹ':
      checkMinArity(argv, 1)
      return new IOV(inst, argv)

    // 문자열
    case 'ㅅㅅ':
      checkArity(argv, [1, 2])
      argv = argv.map(strict)
      var string = argv[0]
      checkType(string, StringV)
      string = string.value
      if (argv.length === 1) {
        if (isNaN(+string)) {
          throw EvalError('Cannot convert "' + string + '" to Number.')
        }
        return new NumberV(+string)
      }
      var base = argv[1]
      checkType(base, NumberV)
      base = base.value
      if (base === 10) {
        if (isNaN(+string)) {
          throw EvalError('Cannot convert "' + string + '" to Number.')
        }
        return new NumberV(+string)
      } else {
        var parts = string.trim().split('.').concat([''])
        var vocab = '0123456789abcdefghijklmnopqrstuvwxyz'.slice(0, base)
        var significant = parts.join('')
        if (significant.search('^[+-]?[' + vocab + ']+$') === -1) {
          throw EvalError('Cannot convert "' + string + '" to Number.')
        }
        significant = parseInt(significant, base)
        return new NumberV(significant / Math.pow(base, parts[1].length))
      }

    case 'ㅂㄹ':
      checkArity(argv, [1, 2])
      argv = argv.map(strict)
      checkType(argv, StringV)
      var src = argv[0].value
      var delimiter = argv.length > 1 ? argv[1].value : ''
      var pieces = src.split(delimiter)
      return new ListV(pieces.map(function (piece) { return new StringV(piece) }))
    case 'ㄱㅁ':
      checkArity(argv, [1, 2])
      argv = argv.map(strict)
      var seq = argv[0]
      var delimiter = (argv.length > 1) ? argv[1] : new StringV('')
      checkType(seq, ListV)
      checkType(delimiter, StringV)
      var pieces = seq.value.map(strict)
      checkType(pieces, StringV)
      return new StringV(pieces.map(_extractValue).join(delimiter.value))

    // 목록
    case 'ㅈㄷ':
      checkArity(argv, 1)
      argv = argv.map(strict)
      checkType(argv, [ListV, StringV])
      return new NumberV(argv[0].value.length)
    case 'ㅂㅈ':
      checkArity(argv, [2, 3, 4])
      argv = argv.map(strict)
      checkType(argv[0], [ListV, StringV])
      checkType(argv.slice(1), NumberV)
      var seq = argv[0].value
      var start = Math.round(argv[1].value)
      var end = argv.length > 2 ? Math.round(argv[2].value) : seq.length
      seq = seq.slice(start, end)
      var step = argv.length > 3 ? Math.round(argv[3].value) : 1
      var cond = function (element, idx) { return idx % step === 0 }
      if (argv[0] instanceof ListV) {
        return new ListV(seq.filter(cond))
      } else if (argv[0] instanceof StringV) {
        return new StringV(seq.split('').filter(cond).join(''))
      }
      break
    case 'ㅁㄷ':
      checkArity(argv, 2)
      argv = argv.map(strict)
      checkType(argv[0], ListV)
      checkType(argv[1], ClosureV)
      return new ListV(argv[0].value.map(function (a) { return [a] }).map(_exprApply(argv[1])))
    case 'ㅅㅂ':
      checkArity(argv, 2)
      argv = argv.map(strict)
      checkType(argv[0], ListV)
      checkType(argv[1], ClosureV)

      var seq = argv[0].value
      var fitCheck = seq.map(function (a) { return [a] }).map(_exprApply(argv[1])).map(strict)
      checkType(fitCheck, BooleanV)
      fitCheck = fitCheck.map(_extractValue)
      return new ListV(seq.filter(function (_, idx) {
        return fitCheck[idx]
      }))

    // 기타
    case 'ㅁㄹ': // 목록
      return new ListV(argv)
    case 'ㅁㅈ': // 문자열
      checkArity(argv, [0, 1])
      if (argv.length === 0) return new StringV('')
      var arg = strict(argv[0])
      checkType(arg, [NumberV, StringV])
      if (arg instanceof StringV) return arg
      else if (arg.value === (arg.value | 0)) {
        return new StringV(String(arg.value | 0))
      } else {
        return new StringV(String(arg.value))
      }
    case 'ㅂㄱ': // 빈값
      checkArity(argv, 0)
      return new NilV()
  }
}

/* Forces strict evaluation of the value */
function strict (value) {
  if (value instanceof ExprV) {
    if (value.cache) return value.cache
    else {
      value.cache = strict(interpret(value.expr, value.env))
      return value.cache
    }
  } else return value
}

function _accessWithRelativeIndex (arr, rel) {
  if (rel >= 0) return arr[rel]
  else return arr[arr.length + rel]
}

/* Evaluates the expression in given environment and
 * returns a value */
function interpret (expr, env) {
  if (expr instanceof Literal) {
    return new NumberV(expr.value)
  } else if (expr instanceof FunRef) {
    return _accessWithRelativeIndex(env.funs, -expr.rel - 1)
  } else if (expr instanceof ArgRef) {
    if (env.funs.length !== env.args.length) {
      throw EvalError(
        'Assertion Error: Environment has ' +
          env.funs.length +
          ' funs and ' +
          env.args.length +
          ' args.'
      )
    }
    var args = _accessWithRelativeIndex(env.args, -expr.relF - 1)
    var relA = strict(interpret(expr.relA, env))
    checkType(relA, NumberV)
    relA = Math.round(relA.value)
    if (relA < 0 || relA >= args.length) {
      throw EvalError(
        'Out of Range: ' +
          args.length +
          ' arguments received ' +
          'but ' +
          relA +
          '-th argument requested'
      )
    } else return args[relA]
  } else if (expr instanceof FunDef) {
    var newFuns = env.funs.slice()
    var newEnv = new Env(newFuns, env.args)
    var closure = new ClosureV(expr.body, newEnv)
    newEnv.funs.push(closure)
    return closure
  } else if (expr instanceof FunCall) {
    var argv = expr.argv.map(function (arg) {
      return new ExprV(arg, env, null)
    })
    if (expr.fun instanceof BuiltinFun) {
      return procBuiltin(expr.fun.id, argv)
    }

    var funValue = strict(interpret(expr.fun, env))
    checkType(funValue, [BooleanV, ListV, StringV, ClosureV])
    if (funValue instanceof BooleanV) {
      checkArity(argv, 2)
      return argv[funValue.value ? 0 : 1]
    } else if (funValue instanceof ClosureV) {
      return _exprApply(funValue)(argv)
    } else {
      checkArity(argv, 1)
      argv = argv.map(strict)
      checkType(argv, NumberV)
      var seq = funValue.value
      var idx = Math.round(argv[0].value)
      var item = _accessWithRelativeIndex(seq, idx)
      if (funValue instanceof ListV) return item
      else return new StringV(item)
    }
  }
  throw EvalError('Unexpected expression: ' + expr)
}

/* Receives an IOV and produces non-ExprV value. */
function _doSingleIO (ioValue) {
  checkType(ioValue, IOV)
  var inst = ioValue.inst
  var argv = ioValue.argv
  switch (inst) {
    case 'ㄹ':
      return new StringV(prompt())
    case 'ㅈㄹ':
      alert(argv[0].value)
      return new NilV()
    case 'ㄱㅅ':
      return strict(argv[0])
    case 'ㄱㄹ':
      argv = argv.map(strict)
      var binder = argv.pop()
      checkType(argv, IOV)
      checkType(binder, ClosureV)
      argv = argv.map(doIO)
      var result = strict(_exprApply(binder)(argv))
      checkType(result, IOV)
      return result
  }
}

/* Receives an IOV and produces non-IOV non-ExprV value. */
function doIO (ioValue) {
  checkType(ioValue, IOV)
  while (ioValue instanceof IOV) {
    ioValue = _doSingleIO(ioValue)
  }
  return ioValue
}

/* Converts the value into a JS object */
function toJS (value) {
  value = strict(value)
  if (value instanceof IOV) value = doIO(value)

  if (isType(value, [NumberV, BooleanV, StringV])) {
    return value.value
  } else if (value instanceof ListV) {
    return value.value.map(toJS)
  } else if (value instanceof ClosureV) {
    return '&lt;Closure created at depth ' + value.env.args.length + '&gt;'
  } else if (value instanceof NilV) {
    return null
  }
  throw EvalError('Unexpected value: ' + value)
}

/* Main procedure. Parses, evaluates, and converts to str.
    Args:
        arg: raw string that encodes a program
    Returns:
        A string representing the resulting value */
function main (arg, formatter = toJS) {
  var exprs = parse(arg)
  var env = new Env([], [])
  var values = exprs.map(function (expr) {
    return interpret(expr, env)
  })
  return values.map(formatter)
}

/* Used to revert AST to codes */
function encodeNumber (number) {
  var isNegative = number < 0
  if (isNegative) number = -number
  // nonnegative integer
  var oct = number
    .toString(8)
    .split('')
    .reverse()
  var tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
  var encoded = oct.map(s => tbl[s]).join('')
  if ((encoded.length % 2 === 0) !== isNegative) {
    encoded += 'ㄱ'
  }
  return encoded
}
function astToCode (parsed) {
  if (parsed instanceof Literal) {
    return encodeNumber(parsed.value)
  } else if (parsed instanceof FunRef) {
    return encodeNumber(parsed.rel) + ' ㅇ'
  } else if (parsed instanceof ArgRef) {
    return encodeNumber(parsed.relA) + ' ㅇ' + encodeNumber(parsed.relF)
  } else if (parsed instanceof FunDef) {
    return astToCode(parsed.body) + ' ㅎ'
  } else if (parsed instanceof BuiltinFun) {
    return encodeNumber(parsed.id)
  } else if (parsed instanceof FunCall) {
    var argv = parsed.argv.map(astToCode).join(' ')
    var fun = astToCode(parsed.fun)
    if (argv) argv += ' '
    return argv + fun + ' ㅎ' + encodeNumber(parsed.argv.length)
  }
  throw Error('[astToCode] Invalid argument', parsed)
}
