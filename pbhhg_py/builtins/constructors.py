from pbhhg_py.abstract_syntax import *
from pbhhg_py.utils import *


def _parse_str_to_number(argv):
    match_defaults(argv, 2, [Integer(10)])
    string, base = argv
    check_type(string, String)
    check_type(base, Integer)
    return string.value, base.value


def build_tbl(proc_functional):
    def _dict(argv):
        if len(argv) % 2 == 1:
            raise ValueError('Dict requires even number of arguments '
                             'but received: {}'.format(len(argv)))
        keys, values = argv[0::2], argv[1::2]
        keys = yield from map_strict(keys, recursive_strict)
        return Dict({k: v for k, v in zip(keys, values)})

    def _list(argv):
        return List(tuple(argv))
        yield

    def _string(argv):
        check_arity(argv, [0, 1])
        if len(argv) == 0:
            return String('')
        arg = yield argv[0]
        check_type(arg, (Number, String))
        if is_type(arg, Real):
            return String(str(arg.value))
        elif is_type(arg, Complex):
            return String(str(arg))
        else:
            return arg

    def _integer(argv):
        argv = yield from match_arguments(argv, (Real, String), [1, 2])
        if is_type(argv[0], Real):
            check_arity(argv, 1)
            return Integer(int(argv[0].value))

        string, base = _parse_str_to_number(argv)
        return Integer(int(string, base))

    def _float(argv):
        argv = yield from match_arguments(argv, (Real, String), [1, 2])
        if is_type(argv[0], Real):
            check_arity(argv, 1)
            return Float(float(argv[0].value))

        string, base = _parse_str_to_number(argv)
        if base == 10:
            return Float(float(string))
        integer, frac = (string.strip().split('.') + [''])[:2]
        significant = int(integer + frac, base=base)
        return Float(significant / base ** len(frac))

    def _complex(argv):
        argv = yield from match_arguments(argv, (Number, String), [1, 2])
        if is_type(argv, Number):
            real, imag = (argv + [Float(0.0)])[:2]
            return Complex(complex(real.value, imag.value))

        check_arity(argv, 1)
        arg = argv[0].value.replace('i', 'j')
        return Complex(complex(arg))

    def _nil(argv):
        check_arity(argv, 0)
        return Nil()
        yield

    return {
        'ㅅㅈ': _dict,  # 사전
        'ㅁㄹ': _list,  # 목록
        'ㅁㅈ': _string,  # 문자열
        'ㅈㅅ': _integer,  # 정수
        'ㅅㅅ': _float,  # 실수
        'ㅂㅅ': _complex,  # 복소수
        'ㅂㄱ': _nil,  # 빈값
    }
