'''
함수형 난해한 언어 '평범한 한글'의 구현체입니다.

Updates
v0.2
* ㅇ의 행동을 변경했습니다.
  - 인수 위치를 정수 리터럴로만 지정 가능 -> 동적으로 평가해 그 값으로 지정 가능
  - 주의: v0.1의 행동과 호환이 되지 않습니다.
* 기본 함수 ㄹ, ㅁ을 추가했습니다.
    - ㄹ: 표준 입력
      * 알려진 문제: 현재 구현체는 게으른(lazy) 평가를 사용하기 때문에
          `ㄹㅎㄱ ㄱㅇㄱ ㄱㅇㄱ ㄷㅎㄷ ㅎ ㅎㄴ`를 실행하면
          입력을 따로 두 번 받는 문제가 있습니다.
    - ㅁ: 논리 부정
'''
from collections import namedtuple
import sys


def normalize_char(c):
    '''Normalizes each character into standard form'''
    # note all ㅇ and ㅎ has a preceding space in following tables
    jamo = ['ㄱ', 'ㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴ ㅎ',
            'ㄷ', 'ㄷ', 'ㄹ', 'ㄹㄱ', 'ㄹㅁ', 'ㄹㅂ',
            'ㄹㅅ', 'ㄹㄷ', 'ㄹㅂ', 'ㄹ ㅎ', 'ㅁ', 'ㅂ',
            'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅅ', ' ㅇ', 'ㅈ', 'ㅈ',
            'ㅈ', 'ㄱ', 'ㄷ', 'ㅂ', ' ㅎ']
    choseong = ['ㄱ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄷ', 'ㄹ', 'ㅁ',
                'ㅂ', 'ㅂ', 'ㅅ', 'ㅅ', ' ㅇ', 'ㅈ', 'ㅈ',
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
ArgRef = namedtuple('ArgRef', 'relA relF')  # relF nonnegative integer
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

            argv = stack[-arity:] if arity else []
            rest = stack[:-arity] if arity else stack
            return rest + [FunCall(fun, argv)]

        else:  # FunDef
            body = stack.pop()
            return stack + [FunDef(body)]
        
    elif 'ㅇ' in word:
        _, trailer = word.split('ㅇ')  # Assume space before every ㅇ

        if trailer:  # ArgRef
            relF = parse_number(trailer)
            relA = stack.pop()
            return stack + [ArgRef(relA, relF)]

        else:  # FunRef
            relF = stack.pop()
            if not isinstance(relF, Literal):
                raise ValueError(
                    'Function reference admits integer literals only, ' +
                    'but received: {}'.format(relF))
            else:
                relF = relF.value
            return stack + [FunRef(relF)]

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


def encode_bool(pred, env):
    '''Encodes a boolean into Church boolean
    Args:
        pred: boolean to encode.
        env: current environment.
    Returns:
        A closure which includes the church-encoded boolean value
    '''
    idx = Literal(0 if pred else 1)
    fundef = FunDef(ArgRef(idx, 0))
    return interpret(fundef, env)


def decode_bool(value):
    '''Decodes Church boolean into Python bool
    Args:
        value: Closure value encoding church boolean
    Returns:
        Corresponding Python bool
    '''
    value = strict(value)
    err_msg = 'Expected boolean, received: {}'.format(value)
    if not isinstance(value, Closure):
        raise ValueError(err_msg)
    if not isinstance(value.body, ArgRef):
        raise ValueError(err_msg)
    a, f = value.body
    if f == 0 and a.value == 0:
        return True
    elif f == 0 and a.value == 1:
        return False
    else:
        raise ValueError(err_msg)


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
    # 산술 연산
    if i == parse_number('ㄱ'):  # 곱셈
        argv = [strict(a) for a in argv]
        product = 1.0
        for a in argv:
            product *= a.value
        return Number(product)
    if i == parse_number('ㄷ'):  # 덧셈
        argv = [strict(a) for a in argv]
        return Number(sum([a.value for a in argv]))
    if i == parse_number('ㅅ'):  # 거듭제곱
        argv = [strict(a) for a in argv]
        return Number(argv[0].value ** argv[1].value)

    # 논리 연산
    if i == parse_number('ㄴ'):  # 같다 (<-는)
        argv = [strict(a) for a in argv]
        return encode_bool(argv[0].value == argv[1].value, env)
    if i == parse_number('ㅁ'):  # 부정 (<-못하다)
        argv = [strict(a) for a in argv]
        value = decode_bool(argv[0])
        return encode_bool(not value, env)
    if i == parse_number('ㅈ'):  # 작다
        argv = [strict(a) for a in argv]
        return encode_bool(argv[0].value < argv[1].value, env)

    # 입력
    if i == parse_number('ㄹ'):  # 읽기
        value = input('')
        return Number(float(value) if value else 0)


def interpret(expr, env):
    '''Evaluates the expression in given environment and returns a value'''
    if isinstance(expr, Literal):
        return Number(expr.value)

    elif isinstance(expr, FunRef):
        return env.funs[-expr.rel-1]

    elif isinstance(expr, ArgRef):
        assert len(env.funs) == len(env.args)
        relA, relF = expr
        args = env.args[-relF-1]

        relA = strict(interpret(relA, env))
        relA = int(round(abs(relA.value)))

        if relA >= len(args):
            raise ValueError(
                'Out of Range: {} arguments received ' +
                'but {}-th argument requested'.format(len(args), relA))
        else:
            return args[relA]

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
        arguments = [Expr(arg, env) for arg in argv]  # lazy eval
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
        try:
            return decode_bool(value)
        except ValueError:
            return '<Closure created at depth {}>'.format(
                len(value.env.args)-1)
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
