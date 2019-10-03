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
from pbhhg_py.interpret import strict, proc_functional
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
        *arguments, binder = argv
        arguments = [strict(arg) for arg in arguments]
        check_type(arguments, IO)
        arguments = [do_IO(arg) for arg in arguments]
        result = strict(proc_functional(binder)(arguments))
        check_type(result, IO)
        return result


def do_IO(io_value):
    '''Receives an IO and produces non-IO non-Expr value.'''
    check_type(io_value, IO)
    while isinstance(io_value, IO):
        io_value = _do_single_IO(io_value)
    return io_value


def formatter(value, format_io=True):
    '''Converts the value into Python number, bool and str for writing tests'''
    value = strict(value)
    if isinstance(value, IO):
        _format = 'IO({})' if format_io else '{}'
        return _format.format(formatter(do_IO(value)))

    if isinstance(value, Number):
        arg = value.value
        return str(int(arg) if int(arg) == arg else arg)
    if isinstance(value, Boolean):
        return str(value.value)
    if isinstance(value, String):
        return "'{}'".format(value.value)
    if isinstance(value, Bytes):
        arg = ''.join(r'\x{:02X}'.format(b) for b in value.value)
        return "b'{}'".format(arg)
    if isinstance(value, List):
        arg = [formatter(item, format_io) for item in value.value]
        return '[{}]'.format(', '.join(arg))
    if isinstance(value, Dict):
        d = value.value
        d = [(formatter(k, format_io), formatter(d[k], format_io)) for k in d]
        d = sorted(d, key=lambda pair: pair[0])
        d = ', '.join("{}: {}".format(k, v) for k, v in d)
        return '{' + d + '}'
    if isinstance(value, Function):
        return str(value)
    if isinstance(value, Nil):
        return 'Nil'
    raise ValueError('Unexpected value: {}'.format(value))


def main(arg, format_io=True):
    '''Main procedure. Parses, evaluates, and converts to str.
    Args:
        arg: Raw string that encodes a program
        formatter: A function that maps a pbhhg value to str.
    Returns:
        A list of strings representing the resulting values
    '''
    exprs = parse(arg)
    env = Env([], [])
    values = [Expr(expr, env, []) for expr in exprs]
    return [formatter(value, format_io) for value in values]


def print_main_with_warning(arg):
    values = main(arg)
    if len(values) >= 2:
        print('[!] Warning: Interpreted {} objects in 1 line.'.format(
            len(values)))
    print(' '.join(values), flush=True)


if __name__ == '__main__':
    if len(sys.argv) == 1:  # stdin (user or cat file)
        print('[Unsuspected Hangeul Interpreter shell. Quit with Ctrl-D.]')
        print('> ', end='', flush=True)
        for line in sys.stdin:
            print_main_with_warning(line)
            print('> ', end='', flush=True)
    elif len(sys.argv) == 2:  # inline
        print_main_with_warning(sys.argv[1])
