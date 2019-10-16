from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def build_tbl(proc_functional):
    def _dict(argv):
        if len(argv) % 2 == 1:
            raise ValueError('Dict requires even number of arguments '
                             'but received: {}'.format(len(argv)))
        keys, values = argv[0::2], argv[1::2]
        keys = yield from [(yield from recursive_strict(k)) for k in keys]
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
        if is_type(arg, String):
            return arg
        elif arg.value == int(arg.value):
            return String(str(int(arg.value)))
        else:
            return String(str(arg.value))

    def _nil(argv):
        check_arity(argv, 0)
        return Nil()
        yield

    return {
        'ㅅㅈ': _dict,  # 사전
        'ㅁㄹ': _list,  # 목록
        'ㅁㅈ': _string,  # 문자열
        'ㅂㄱ': _nil,  # 빈값
    }
