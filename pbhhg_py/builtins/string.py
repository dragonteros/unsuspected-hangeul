from pbhhg_py.abstract_syntax import *
from pbhhg_py.utils import *


def build_tbl(proc_functional):
    def _split(argv):
        check_arity(argv, [1, 2])
        argv = yield from [(yield arg) for arg in argv]
        check_type(argv, String)
        src, delimiter = (argv + [String('')])[:2]
        if delimiter.value:
            pieces = src.value.split(delimiter.value)
        else:
            pieces = src.value
        return List(tuple(String(piece) for piece in pieces))

    def _join(argv):
        check_arity(argv, [1, 2])
        argv = yield from [(yield arg) for arg in argv]
        seq, delimiter = (argv + [String('')])[:2]
        check_type(seq, List)
        check_type(delimiter, String)
        pieces = yield from [(yield arg) for arg in seq.value]
        check_type(pieces, String)
        return String(delimiter.value.join(piece.value for piece in pieces))

    return {
        'ㅂㄹ': _split,  # 분리
        'ㄱㅁ': _join,  # 꿰매다
    }
