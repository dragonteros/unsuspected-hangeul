'''
함수형 난해한 언어 '평범한 한글'의 구현체입니다.

Updates
* v0.7 (2020.03.08)
  * 복소수가 추가되고 정수가 실수에서 분리되었습니다.
  * 기본 제공 함수로 정수 나눗셈과 나머지 연산이 추가되었습니다. 거듭제곱 연산은 모듈로 거듭제곱을 지원하도록 확장되었습니다.
  * 인수 접근 및 목록, 문자열 등의 인덱싱 행동이 실수를 반올림하는 것에서 정수를 사용하는 것으로 일괄 변경되었습니다.
    - 주의: v0.6의 행동과 호환되지 않습니다.
  * 수학 모듈과 비트 연산 모듈이 추가되었습니다.
'''
import sys

from pbhhg_py.abstract_syntax import *
from pbhhg_py.parse import parse
from pbhhg_py.interpret import proc_functional, evaluate
from pbhhg_py.utils import check_type, map_strict


def _do_single_IO(io_value):
    '''Receives an IO and produces non-Expr value.'''
    check_type(io_value, IO)
    inst, argv = io_value
    if inst == 'ㄹ':  # read string
        try:
            return String(input(''))
        except EOFError:
            return Nil()
    if inst == 'ㅈㄹ':  # write
        print(argv[0].value, flush=True)
        return Nil()
    if inst == 'ㄱㅅ':  # return
        return (yield argv[0])
    if inst == 'ㄱㄹ':  # bind
        *arguments, binder = argv
        arguments = yield from map_strict(arguments)
        check_type(arguments, IO)
        arguments = yield from map_strict(arguments, do_IO)
        _fn = yield from proc_functional(binder)
        result = yield (yield from _fn(arguments))
        check_type(result, IO)
        return result


def do_IO(io_value):
    '''Receives an IO and produces non-IO non-Expr value.'''
    check_type(io_value, IO)
    while isinstance(io_value, IO):
        io_value = yield from _do_single_IO(io_value)
    return io_value


def formatter(value, format_io=True):
    '''Converts the value into Python number, bool and str for writing tests'''
    value = yield value
    if isinstance(value, IO):
        _format = 'IO({})' if format_io else '{}'
        arg = yield from do_IO(value)
        arg = yield from formatter(arg)
        return _format.format(arg)

    _formatter = lambda x: formatter(x, format_io)
    if isinstance(value, Real):
        return str(value.value)
    if isinstance(value, Complex):
        return str(value)
    if isinstance(value, Boolean):
        return str(value.value)
    if isinstance(value, String):
        return "'{}'".format(value.value)
    if isinstance(value, Bytes):
        arg = ''.join(r'\x{:02X}'.format(b) for b in value.value)
        return "b'{}'".format(arg)
    if isinstance(value, List):
        arg = yield from map_strict(value.value, _formatter)
        return '[{}]'.format(', '.join(arg))
    if isinstance(value, Dict):
        if not value.value:
            return '{}'
        keys, values = zip(*value.value.items())
        keys = yield from map_strict(keys, _formatter)
        values = yield from map_strict(values, _formatter)
        d = list(zip(keys, values))
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
        format_io: Whether to format IOs in the form `IO(.)`
    Returns:
        A list of strings representing the resulting values
    '''
    exprs = parse(arg)
    env = Env([], [])
    values = [Expr(expr, env, []) for expr in exprs]
    formatters = [formatter(value, format_io) for value in values]
    return [evaluate(f) for f in formatters]


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
