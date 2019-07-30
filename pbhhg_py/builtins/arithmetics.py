from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def _multiply(argv, _strict):
    check_min_arity(argv, 1)
    argv = _strict(argv)
    check_type(argv, (Number, Boolean))
    if is_type(argv, Boolean):
        return Boolean(all(a.value for a in argv))
    elif is_type(argv, Number):
        product = 1.0
        for a in argv:
            product *= a.value
        return Number(product)


def _add(argv, _strict):
    check_min_arity(argv, 1)
    argv = _strict(argv)
    check_type(argv, [Number, Boolean, List, String])
    if is_type(argv, Number):
        return Number(sum(a.value for a in argv))
    elif is_type(argv, Boolean):
        return Boolean(any(a.value for a in argv))
    elif is_type(argv, List):
        return List([element for seq in argv for element in seq.value])
    elif is_type(argv, String):
        return String(''.join(a.value for a in argv))


def _exponentiate(argv, _strict):
    check_arity(argv, 2)
    argv = _strict(argv)
    check_type(argv, Number)
    base, exponent = argv
    return Number(base.value ** exponent.value)


tbl = {
    'ㄱ': _multiply,  # 곱셈
    'ㄷ': _add,  # 덧셈
    'ㅅ': _exponentiate,  # 거듭제곱
}
