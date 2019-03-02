/** Normalizer **/

/* Normalizes each character into standard form */
function normalize_char(c) {
    function getidx(ref, divisor=1) {
        return Math.floor((c.charCodeAt(0) - ref.charCodeAt(0))/divisor)
    }
    // note all ㅇ and ㅎ has a preceding space in following tables
    var jamo = ['ㄱ', 'ㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴ ㅎ',
        'ㄷ', 'ㄷ', 'ㄹ', 'ㄹㄱ', 'ㄹㅁ', 'ㄹㅂ',
        'ㄹㅅ', 'ㄹㄷ', 'ㄹㅂ', 'ㄹ ㅎ', 'ㅁ', 'ㅂ',
        'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅅ', ' ㅇ', 'ㅈ', 'ㅈ',
        'ㅈ', 'ㄱ', 'ㄷ', 'ㅂ', ' ㅎ']
    var choseong = ['ㄱ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄷ', 'ㄹ', 'ㅁ',
        'ㅂ', 'ㅂ', 'ㅅ', 'ㅅ', ' ㅇ', 'ㅈ', 'ㅈ',
        'ㅈ', 'ㄱ', 'ㄷ', 'ㅂ', ' ㅎ']
    if (c.length != 1)
        throw '[normalize_char] Length of string should be 1, not ' + c.length + ': ' + c;
    if ('ㄱ' <= c && c <= 'ㅎ') {
        return jamo[getidx('ㄱ')]
    } else if ('가' <= c && c <= '힣') {
        return choseong[getidx('가', 588)]
    } else if ('\u1100' <= c && c <= '\u1112') {  // 첫가끝 초성
        return choseong[getidx('\u1100')]
    } else if ('\uFFA1' <= c && c <= '\uFFBE') {  // 반각
        return jamo[getidx('\uFFA1')]
    } else return ' ';
}

/* Parses jamo-encoded variable length integer into JS Number */
function parse_number(s) {
    var tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
    var varlen = s.split('').map(function (c) { return tbl.indexOf(c) })
    if (varlen.some(function (idx) { return idx == -1 }))
        throw '[parse_number] Argument ' + s + ' has an unsupported character';
    var num = parseInt(varlen.reverse().join(''), 8)
    if (s.length % 2 == 0)
        num = -num;
    return num
}


/** Parser **/

function Literal(value) {
    this.value = value;  // int
}
function FunRef(rel) {
    this.rel = rel;  // int
}
function ArgRef(relA, relF) {
    this.relA = relA;
    this.relF = relF;  // int
}
function FunDef(body) {
    this.body = body;
}
function BuiltinFun(id) {  // int
    this.id = id;
}
function FunCall(fun, argv) {
    this.fun = fun;
    this.argv = argv;
}

/* Parses concrete syntax to abstract syntax
Args:
    word: string. word to parse
    stack: list of parsed legal arguments so far that we will modify */
function parse_word(word, stack) {
    if (word.indexOf('ㅎ') != -1) {
        var arity = word.slice(1)
        if (arity) {  // FunCall
            arity = parse_number(arity)
            fun = stack.pop()
            if (fun instanceof Literal)
                fun = new BuiltinFun(fun.value)
            
            if (arity == 0) {
                stack.push(new FunCall(fun, []))
            } else if (arity < 0) {
                throw 'Function call with negative number of arguments: ' + arity;
            } else {
                argv = stack.splice(-arity, arity)
                stack.push(new FunCall(fun, argv))
            }
        } else {  // FunDef
            var body = stack.pop()
            stack.push(new FunDef(body))
        }
    } else if (word.indexOf('ㅇ') != -1) {
        var trailer = word.slice(1)
        if (trailer) {  // ArgRef
            var relF = parse_number(trailer)
            var relA = stack.pop()
            stack.push(new ArgRef(relA, relF))
        } else {  // FunRef
            var relF = stack.pop()
            if (relF instanceof Literal) {
                relF = relF.value;
            } else {
                throw ('Function reference admits integer literals only, ' +
                       'but received:' + relF)
            }
            stack.push(new FunRef(relF));
        }
    } else {
        stack.push(new Literal(parse_number(word)));
    }
}

/* Parses program into abstract syntax */
function parse(sentence) {
    sentence = sentence.split('').map(normalize_char).join('');
    var words = sentence.split(' ')
    var stack = []
    var len = words.length;
    for (var i=0; i<len; i++) {
        if (words[i]) parse_word(words[i], stack);
    }
    return stack;
}


// Interpreter

function Env(funs, args) {
    this.funs = funs
    this.args = args
}

function NumberV(value) {
    this.value = value;
}
function BooleanV(value) {
    this.value = value;
}
function ClosureV(body, env) {
    this.body = body;
    this.env = env;
}
function ExprV(expr, env, cache) {
    this.expr = expr;
    this.env = env;
    this.cache = cache;
}

/* Forces strict evaluation of the value */
function strict(value) {
    if (value instanceof ExprV) {
        if (value.cache) return value.cache;
        else {
            value.cache = strict(interpret(value.expr, value.env))
            return value.cache;
        }
    } else return value;
}

function arity_check(argv, desired_arity) {
    if (argv.length == desired_arity) return;
    throw desired_arity + 'arguments expected but received ' + argv.length;
}

function type_check(argv, desired_type) {
    if (argv.every(function (a) {return a instanceof desired_type})) return;
    throw 'Arguments of type ' + desired_type + ' expected but received: ' + argv;
}

/* Execute the built-in function with given arguments and environement
Args:
    i: Built-in Function ID
    argv: Argument Values for the built-in function
    env: Current environment
Returns:
    Return value of the built-in function */
function proc_builtin(i, argv, env) {
    switch (i) {
        // 산술 연산
        case parse_number('ㄱ'):
            argv = argv.map(strict)
            type_check(argv, NumberV)
            var product = argv.reduce(function (a, b) {
                return a.value * b.value;
            })
            return new NumberV(product);
        case parse_number('ㄷ'):
            argv = argv.map(strict)
            type_check(argv, NumberV)
            var sum = argv.reduce(function (a, b) {
                return a.value + b.value;
            })
            return new NumberV(sum);
        case parse_number('ㅅ'):
            arity_check(argv, 2)
            argv = argv.map(strict)
            type_check(argv, NumberV)
            var power = Math.pow(argv[0].value, argv[1].value)
            return new NumberV(power)
        
        //논리 연산
        case parse_number('ㄴ'):
            arity_check(argv, 2)
            argv = argv.map(strict)
            if (argv[0].constructor != argv[1].constructor)
                throw 'Argument type mismatch' + argv
            return new BooleanV(argv[0].value == argv[1].value)
        case parse_number('ㅁ'):
            arity_check(argv, 1)
            argv = argv.map(strict)
            type_check(argv, BooleanV)
            return new BooleanV(!argv[0].value)
        case parse_number('ㅈ'):
            arity_check(argv, 2)
            argv = argv.map(strict)
            type_check(argv, NumberV)
            return new BooleanV(argv[0].value < argv[1].value)
        case parse_number('ㅈㅈ'):
            arity_check(argv, 0)
            return new BooleanV(True)
        case parse_number('ㄱㅈ'):
            arity_check(argv, 0)
            return new BooleanV(False)
        
        // 입력
        case parse_number('ㄹ'):
            arity_check(argv, 0)
            value = Number(prompt())
            return new NumberV(value)
    }
}

/* Evaluates the expression in given environment and
 * returns a value */
function interpret(expr, env) {
    if (expr instanceof Literal) {
        return new NumberV(expr.value)
    } else if (expr instanceof FunRef) {
        return env.funs[env.funs.length-expr.rel-1]
    } else if (expr instanceof ArgRef) {
        if (env.funs.length != env.args.length)
            throw ('Assertion Error: Environment has ' +
                   env.funs.length + ' funs and ' + env.args.length + ' args.')
        var args = env.args[env.args.length-expr.relF-1]
        var relA = strict(interpret(expr.relA, env))
        type_check([relA], NumberV)
        relA = Math.round(relA.value)
        if (relA < 0) {
            throw 'Tried to reference argument with negative index: ' + relA
        } else if (relA >= args.length) {
            throw ('Out of Range: ' + args.length +' arguments received ' +
            'but ' + relA + '-th argument requested')
        } else return args[relA]
    } else if (expr instanceof FunDef) {
        var new_funs = env.funs.slice()
        var new_env = new Env(new_funs, env.args)
        var closure = new ClosureV(expr.body, new_env)
        new_env.funs.push(closure)
        return closure
    } else if (expr instanceof FunCall) {
        var argv = expr.argv.map(function (arg) {
            return new ExprV(arg, env, null)
        })
        if (expr.fun instanceof BuiltinFun) {
            return proc_builtin(expr.fun.id, argv, env)
        }

        var fun_value = strict(interpret(expr.fun, env))
        if (fun_value instanceof NumberV) {
            throw 'Number is not callable.'
        } else if (fun_value instanceof BooleanV) {
            arity_check(argv, 2)
            return argv[fun_value.value? 0: 1]
        } else if (fun_value instanceof ClosureV) {
            var canned_env = fun_value.env
            var new_argv = canned_env.args.concat([argv])
            var new_env = new Env(canned_env.funs, new_argv)
            return interpret(fun_value.body, new_env)
        }
    }
    throw 'Unexpected expression: ' + expr
}

/* Converts the value into a printable JS object */
function to_printable(value) {
    value = strict(value)
    if (value instanceof NumberV) {
        return value.value
    } else if (value instanceof BooleanV) {
        return value.value
    } else if (value instanceof ClosureV) {
        return '&lt;Closure created at depth ' + (value.env.args.length-1) + '&gt;'
    } else {
        throw 'Unexpected value: ' + value
    }
}

/* Main procedure. Parses, evaluates, and converts to str.
    Args:
        arg: raw string that encodes a program
    Returns:
        A string representing the resulting value */
function main(arg) {
    var stack = parse(arg)
    var env = new Env([null], [[]])
    var values = stack.map(function (expr) {
        return interpret(expr, env)
    })
    return values.map(to_printable).join(' ')
}