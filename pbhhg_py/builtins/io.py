from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def _input(argv, _strict):
    check_arity(argv, 0)
    return IO('ㄹ', argv)


def _print(argv, _strict):
    check_arity(argv, 1)
    argv = _strict(argv)
    check_type(argv, String)
    return IO('ㅈㄹ', argv)


def _return(argv, _strict):
    check_arity(argv, 1)
    return IO('ㄱㅅ', argv)


def _bind(argv, _strict):
    check_min_arity(argv, 1)
    return IO('ㄱㄹ', argv)


tbl = {
    'ㄹ': _input,  # 입력
    'ㅈㄹ': _print,  # 출력
    'ㄱㅅ': _return,  # 감싸다
    'ㄱㄹ': _bind,  # ~기로 하다
}
