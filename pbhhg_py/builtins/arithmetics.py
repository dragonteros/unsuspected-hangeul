from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def build_tbl(proc_functional, _strict):
    def _multiply(argv):
        check_min_arity(argv, 1)
        argv = _strict(argv)
        check_type(argv, (Number, Boolean))
        if is_type(argv, Boolean):
            return Boolean(all(a.value for a in argv))
        elif is_type(argv, Number):
            product = 1
            for a in argv:
                product *= a.value
            return Number(product)

    def _add(argv):
        check_min_arity(argv, 1)
        argv = _strict(argv)
        check_type(argv, [Number, Boolean, List, String, Bytes, Dict])
        if is_type(argv, Number):
            return Number(sum(a.value for a in argv))
        elif is_type(argv, Boolean):
            return Boolean(any(a.value for a in argv))
        elif is_type(argv, List):
            return List(tuple(item for seq in argv for item in seq.value))
        elif is_type(argv, String):
            return String(''.join(a.value for a in argv))
        elif is_type(argv, Bytes):
            return Bytes(b''.join(a.value for a in argv))
        elif is_type(argv, Dict):
            return Dict({k: a.value[k] for a in argv for k in a.value})

    def _exponentiate(argv):
        check_arity(argv, 2)
        argv = _strict(argv)
        check_type(argv, Number)
        base, exponent = argv
        return Number(base.value ** exponent.value)

    return {
        'ㄱ': _multiply,  # 곱셈
        'ㄷ': _add,  # 덧셈
        'ㅅ': _exponentiate,  # 거듭제곱
    }
