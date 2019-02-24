'''
함수형 난해한 언어 '평범한 한글'의 구현체입니다.

현재 지원 안되는 단어:
* ㅇ 두 개 이상
* ㅇ 단독
* ㅎ 다음에 오는 ㅇ
'''
from collections import namedtuple
import sys


def normalize_char(c):
    '''Normalizes each character into standard form'''
    # note all ㅎ has a preceding space in following tables
    jamo = ['ㄱ', 'ㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴ ㅎ',
            'ㄷ', 'ㄷ', 'ㄹ', 'ㄹㄱ', 'ㄹㅁ', 'ㄹㅂ',
            'ㄹㅅ', 'ㄹㄷ', 'ㄹㅂ', 'ㄹ ㅎ', 'ㅁ', 'ㅂ',
            'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅈ',
            'ㅈ', 'ㄱ', 'ㄷ', 'ㅂ', ' ㅎ']
    choseong = ['ㄱ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄷ', 'ㄹ', 'ㅁ',
                'ㅂ', 'ㅂ', 'ㅅ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅈ',
                'ㅈ', 'ㄱ', 'ㄷ', 'ㅂ', ' ㅎ']
    if len(c) != 1:
        raise ValueError(
            'Length of string should be 1, not {}: {}'.format(len(c), c))

    if 'ㄱ' <= c <= 'ㅎ':
        idx = ord(c) - ord('ㄱ')
        return jamo[idx]
    elif '가' <= c <= '힣':
        idx = (ord(c) - ord('가')) // 588
        return choseong[idx]
    elif '\u1100' <= c <= '\u1112':  # 첫가끝 초성
        idx = ord(c) - ord('\u1100')
        return choseong[idx]
    elif '\uFFA1' <= c <= '\uFFBE':  # 반각
        idx = ord(c) - ord('\uFFA1')
        return jamo[idx]
    else:
        return ' '


def parse_number(s):
    '''Parses jamo-encoded variable length integer into python int'''
    tbl = 'ㄱㄴㄷㄹㅁㅂㅅㅈ'
    varlen = [tbl.index(c) for c in s]  # LSB first
    octal = ''.join([str(d) for d in reversed(varlen)])  # MSB first
    num = int(octal, base=8)
    if len(s) % 2 == 0:
        num = -num
    return num


Literal = namedtuple('Literal', 'value')  # integer
FunRef = namedtuple('FunRef', 'rel')  # nonnegative integer
ArgRef = namedtuple('ArgRef', 'relF relA')  # both nonnegative integer
FunDef = namedtuple('FunDef', 'body')
BuiltinFun = namedtuple('BuiltinFun', 'id')  # integer
FunCall = namedtuple('FunCall', 'fun argv')


def parse_word(word, stack):
    '''Parses concrete syntax to abstract syntax
    Args:
        word: str. word to parse
        stack: list of parsed legal arguments so far

    Returns:
        new stack with newly parsed argument appended
    '''
    if 'ㅎ' in word:
        _, arity = word.split('ㅎ')  # Assume space before every ㅎ

        if arity:  # FunCall
            arity = parse_number(arity)
            fun = stack.pop()
            if isinstance(fun, Literal):
                fun = BuiltinFun(fun.value)

            argv = stack[-arity:]
            return stack[:-arity] + [FunCall(fun, argv)]

        else:  # FunDef
            body = stack.pop()
            return stack + [FunDef(body)]
        
    elif 'ㅇ' in word:
        relF, relA = word.split('ㅇ')
        relF = abs(parse_number(relF)) if relF else 0
        if not relA:  # FunRef
            return stack + [FunRef(relF)]
        else:  # ArgRef
            relA = abs(parse_number(relA))
            return stack + [ArgRef(relF, relA)]
    else:
        return stack + [Literal(parse_number(word))]


def parse(sentence):
    '''Parses program into abstract syntax'''
    sentence = ''.join([normalize_char(c) for c in sentence])
    
    words = sentence.strip().split(' ')
    stack = []
    for word in words:
        if word:
            stack = parse_word(word, stack)
    return stack


def print_parse_tree(arg, indent=0):
    '''Prints the parse tree
    Args:
        arg: Parsed argument whose parse tree is to be printed
        indent: Current indentation status
    Returns:
        None
    '''
    tab = ' ' * 2
    indenter = tab * indent
    if isinstance(arg, int) or isinstance(arg, list):
        print(indenter + str(arg))
        return

    typename = type(arg).__name__
    print(indenter + typename)
    for field in arg._fields:
        print(indenter + tab + field)
        print_parse_tree(getattr(arg, field), indent + 2)


Env = namedtuple('Env', 'funs args')

Number = namedtuple('Number', 'value')
Closure = namedtuple('Closure', 'body env')
Expr = namedtuple('Expr', 'expr env')


def make_bool(pred, env):
    '''Encodes a boolean into Church boolean
    Args:
        pred: boolean to encode.
        env: current environment.
    Returns:
        A closure which includes the church-encoded boolean value
    '''
    idx = 0 if pred else 1
    fundef = FunDef(ArgRef(0, idx))
    return interpret(fundef, env)


def strict(value):
    '''Forces strict evaluation of the value'''
    if isinstance(value, Expr):
        expr, env = value
        return strict(interpret(expr, env))
    else:
        return value


def proc_builtin(i, argv, env):  # ㄱㄴㄷ[ㄹㅁㅂ]ㅅㅈ
    '''Execute the built-in function with given arguments and environement
    Args:
        i: Built-in Function ID
        argv: Argument Values for the built-in function
        env: Current environment
    Returns:
        Return value of the built-in function
    '''
    if i == 2:  # ㄷ: 덧셈
        argv = [strict(a) for a in argv]
        return Number(sum([a.value for a in argv]))
    if i == 0:  # ㄱ: 곱셈
        argv = [strict(a) for a in argv]
        product = 1.0
        for a in argv:
            product *= a.value
        return Number(product)
    if i == 6:  # ㅅ: 거듭제곱
        argv = [strict(a) for a in argv]
        return Number(argv[0].value ** argv[1].value)
    if i == 7:  # ㅈ: 작다
        argv = [strict(a) for a in argv]
        return make_bool(argv[0].value < argv[1].value, env)
    if i == 1:  # ㄴ: 같다
        argv = [strict(a) for a in argv]
        return make_bool(argv[0].value == argv[1].value, env)


def interpret(expr, env):
    '''Evaluates the expression in given environment and returns a value'''
    if isinstance(expr, Literal):
        return Number(expr.value)

    elif isinstance(expr, FunRef):
        return env.funs[-expr.rel-1]

    elif isinstance(expr, ArgRef):
        assert len(env.funs) == len(env.args)
        relF, relA = expr
        return env.args[-relF-1][relA]

    elif isinstance(expr, FunDef):
        body = expr.body
        funs, args = env
        new_funs = funs[:]
        new_env = Env(new_funs, args)
        closure = Closure(body, new_env)
        new_env.funs.append(closure)
        return closure

    elif isinstance(expr, FunCall):
        fun, argv = expr
        arguments = [Expr(arg, env) for arg in argv]
        if isinstance(fun, BuiltinFun):
            return proc_builtin(fun.id, arguments, env)

        body, canned_env = strict(interpret(fun, env))

        canned_funs, canned_args = canned_env
        new_env = Env(canned_funs, canned_args + [arguments])

        return interpret(body, new_env)
    else:
        raise ValueError('Unexpected expression: {}'.format(expr))


def to_printable(value):
    '''Converts the value into a printable Python object'''
    if isinstance(value, Number):
        return value.value
    elif isinstance(value, Closure):
        if isinstance(value.body, ArgRef):
            f, a = value.body
            if f == 0 and a == 0:
                return True
            elif f == 0 and a == 1:
                return False
        return '<Closure created at depth {}>'.format(len(value.env.args)-1)
    elif isinstance(value, Expr):
        return to_printable(strict(value))
    else:
        raise ValueError('Unexpected value: {}'.format(value))


def main(arg):
    '''Main procedure. Parses, evaluates, and converts to str.
    Args:
        arg: raw string that encodes a program
    Returns:
        A string representing the resulting value
    '''
    stack = parse(arg)
    env = Env([None], [[]])
    values = [interpret(expr, env) for expr in stack]

    if len(values) == 1:
        return str(to_printable(values[0]))
    else:
        if any([isinstance(v, Closure) for v in values]):
            return ' '.join([str(to_printable(v)) for v in values])
        else:
            numbers = [to_printable(v) for v in values]
            string = [chr(int(round(n))) for n in numbers]
            return ''.join(string)


if __name__ == '__main__':
    if len(sys.argv) == 1:  # stdin (user or cat file)
        print('> ', end='')
        for line in sys.stdin:
            print(main(line))
            print('> ', end='')
    elif len(sys.argv) == 2:  # inline
        print(main(sys.argv[1]))
