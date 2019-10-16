from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def build_tbl(proc_functional):
    def _input(argv):
        check_arity(argv, 0)
        return IO('ㄹ', tuple(argv))
        yield

    def _print(argv):
        check_arity(argv, 1)
        arg = yield argv[0]
        argv = [arg]
        check_type(argv, String)
        return IO('ㅈㄹ', tuple(argv))

    def _return(argv):
        check_arity(argv, 1)
        return IO('ㄱㅅ', tuple(argv))
        yield

    def _bind(argv):
        check_min_arity(argv, 1)
        return IO('ㄱㄹ', tuple(argv))
        yield

    return {
        'ㄹ': _input,  # 입력
        'ㅈㄹ': _print,  # 출력
        'ㄱㅅ': _return,  # 감싸다
        'ㄱㄹ': _bind,  # ~기로 하다
    }
