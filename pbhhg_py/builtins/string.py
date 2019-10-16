from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def build_tbl(proc_functional, _strict):
    def _str_to_number(argv):
        check_arity(argv, [1, 2])
        argv = _strict(argv)
        string = argv[0]
        check_type(string, String)
        base = argv[1] if len(argv) > 1 else Number(10)
        check_type(base, Number)
        string, base = string.value, base.value
        try:
            return Number(int(string, base))
        except ValueError:
            if base == 10:
                return Number(float(string))
            integer, frac = string.strip().split('.')
            significant = int(integer + frac, base=base)
            return Number(significant / base ** len(frac))

    def _split(argv):
        check_arity(argv, [1, 2])
        argv = _strict(argv)
        check_type(argv, String)
        src, delimiter = (argv + [String('')])[:2]
        if delimiter.value:
            pieces = src.value.split(delimiter.value)
        else:
            pieces = src.value
        return List(tuple(String(piece) for piece in pieces))

    def _join(argv):
        check_arity(argv, [1, 2])
        argv = _strict(argv)
        seq, delimiter = (argv + [String('')])[:2]
        check_type(seq, List)
        check_type(delimiter, String)
        pieces = _strict(seq.value)
        check_type(pieces, String)
        return String(delimiter.value.join(piece.value for piece in pieces))

    return {
        'ㅅㅅ': _str_to_number,  # 실수
        'ㅂㄹ': _split,  # 분리
        'ㄱㅁ': _join,  # 꿰매다
    }
