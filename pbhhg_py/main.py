'''
함수형 난해한 언어 '평범한 한글'의 구현체입니다.

Updates
v0.5 (2019.07.28)
  * 목록 및 문자열과 관련 기본 제공 함수가 추가되었습니다. 빈값도 추가되어,
    이제 객체는 실수, 논릿값, 목록, 문자열, 함수, 드나듦, 빈값의 일곱 종류입니다.
  * 기본 제공 함수 `ㄱ`과 `ㄷ`가 다른 자료형으로 확장되었습니다.
  * 기본 제공 함수 `ㅈㄹ`이 추가되고, 기본 제공 함수 `ㄱㄹ`의 행동이 변경되었습니다.
  * 기본 제공 함수 `ㄹ`의 행동이 변경되었습니다.
    - 주의: v0.4의 행동과 호환되지 않습니다.
'''
import sys

from pbhhg_py.abstract_syntax import *
from pbhhg_py.parse import parse
from pbhhg_py.interpret import strict, interpret
from pbhhg_py.check import check_type


def _do_single_IO(io_value):
    '''Receives an IO and produces non-Expr value.'''
    check_type(io_value, IO)
    inst, argv = io_value
    if inst == 'ㄹ':  # read string
        return String(input(''))
    if inst == 'ㅈㄹ':  # write
        print(argv[0].value, flush=True)
        return Nil()
    if inst == 'ㄱㅅ':  # return
        return strict(argv[0])
    if inst == 'ㄱㄹ':  # bind
        *argv, binder = [strict(arg) for arg in argv]
        check_type(argv, IO)
        check_type(binder, Closure)
        argv = [do_IO(arg) for arg in argv]
        body, canned_env = binder
        canned_funs, canned_args = canned_env
        new_env = Env(canned_funs, canned_args + [argv])
        result = strict(interpret(body, new_env))
        check_type(result, IO)
        return result


def do_IO(io_value):
    '''Receives an IO and produces non-IO non-Expr value.'''
    check_type(io_value, IO)
    while isinstance(io_value, IO):
        io_value = _do_single_IO(io_value)
    return io_value


def to_printable(value):
    '''Converts the value into a printable Python object'''
    value = strict(value)
    if isinstance(value, IO):
        value = do_IO(value)

    if isinstance(value, (Number, Boolean, String)):
        return value.value
    elif isinstance(value, List):
        return [to_printable(item) for item in value.value]
    elif isinstance(value, Closure):
        return '<Closure created at depth {}>'.format(
            len(value.env.args))
    elif isinstance(value, Nil):
        return None
    else:
        raise ValueError('Unexpected value: {}'.format(value))


def to_str(value):
    '''Converts the value into str.'''
    value = strict(value)
    if isinstance(value, IO):
        value = do_IO(value)
    if isinstance(value, String):
        return "'{}'".format(value.value)
    elif isinstance(value, Nil):
        return 'Nil'
    return str(to_printable(value))


def main(arg, formatter=to_printable):
    '''Main procedure. Parses, evaluates, and converts to str.
    Args:
        arg: Raw string that encodes a program
        formatter: A function that maps a pbhhg value to str.
    Returns:
        A list of strings representing the resulting values
    '''
    exprs = parse(arg)
    env = Env([], [])
    values = [interpret(expr, env) for expr in exprs]
    return [formatter(value) for value in values]


def print_main_with_warning(arg):
    values = main(arg, formatter=to_str)
    if len(values) >= 2:
        print('[!] Warning: Interpreted {} objects in 1 line.'.format(
            len(values)))
    print(' '.join(values), flush=True)


if __name__ == '__main__':
    if len(sys.argv) == 1:  # stdin (user or cat file)
        print('> ', end='', flush=True)
        for line in sys.stdin:
            print_main_with_warning(line)
            print('> ', end='', flush=True)
    elif len(sys.argv) == 2:  # inline
        print_main_with_warning(sys.argv[1])
