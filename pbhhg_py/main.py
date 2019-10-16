'''
함수형 난해한 언어 '평범한 한글'의 구현체입니다.

Updates
* v0.6 (2019.10.03)
  * 옛한글 지원이 추가되었습니다. 이제 모음을 공백으로 취급하지 않습니다.
    - 주의: v0.5의 행동과 호환되지 않습니다.
  * 사전과 바이트열이 추가되었습니다. 이제 객체는 실수, 논릿값, 문자열, 바이트열, 목록, 사전, 함수, 드나듦, 빈값의 아홉 종류입니다.
  * 모듈 불러오기가 추가되었습니다.
    * 실수 및 문자열과 바이트열 사이를 변환하는 모듈 `ㅂ ㅂ`이 기본 제공 모듈로 지원됩니다.
  * 기본 제공 함수 `ㄴ`, `ㄷ`, `ㅈㄷ`, `ㅂㅈ`에 사전과 바이트열 지원을 추가했습니다.
  * 기본 제공 함수 `ㅅㄹ`과 `ㄴㄱ`, `ㅁㅂ`, `ㅂㅂ`이 추가되었습니다.
  * 기본 제공 함수 `ㅁㄷ`, `ㅅㅂ`, `ㅅㄹ`, `ㄱㄹ`가 함수 대신 정수 리터럴, 논릿값 등을 받을 수 있게 변경되었습니다.
'''
import sys

from pbhhg_py.abstract_syntax import *
from pbhhg_py.parse import parse
from pbhhg_py.interpret import proc_functional, evaluate
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
        return (yield argv[0])
    if inst == 'ㄱㄹ':  # bind
        *arguments, binder = argv
        arguments = yield from [(yield arg) for arg in arguments]
        check_type(arguments, IO)
        arguments = yield from [(yield from do_IO(arg)) for arg in arguments]
        _fn = yield from proc_functional(binder)
        result = yield from _fn(arguments)
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
        arg = yield from [(yield from formatter(item, format_io)) for item in value.value]
        return '[{}]'.format(', '.join(arg))
    if isinstance(value, Dict):
        d = value.value
        d = yield from [((yield from formatter(k, format_io)),
                         (yield from formatter(d[k], format_io))) for k in d]
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
