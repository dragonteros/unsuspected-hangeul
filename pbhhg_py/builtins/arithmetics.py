import math
import operator
from functools import reduce

from pbhhg_py.abstract_syntax import *
from pbhhg_py.utils import *


def _extended_gcd(a, b):
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x, x_old, y, y_old = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y, y_old = y_old, y - q * y_old
        x, x_old = x_old, x - q * x_old
    return b, x, y


def _modular_inverse(a, mod):
    a = a % mod
    try:
        return pow(a, -1, mod)
    except ValueError:
        g, inverse, _ = _extended_gcd(a, mod)
        if g == 1:
            return inverse % mod
    raise ValueError(
        'Modular inverse of {} mod {} does not exist.'.format(a, mod))


def build_tbl(proc_functional) -> dict[str, Coroutine]:
    def _multiply(argv):
        check_min_arity(argv, 1)
        argv = yield from map_strict(argv)
        check_type(argv, (Number, Boolean))
        if is_type(argv, Number):
            argv = (arg.value for arg in argv)
            return guessed_wrap(reduce(operator.mul, argv))  # No init

        check_same_type(argv)
        return Boolean(all(a.value for a in argv))

    def _add(argv):
        check_min_arity(argv, 1)
        argv = yield from map_strict(argv)
        check_type(argv, (Number, Boolean, Sequence, Dict))
        if is_type(argv, Number):
            return guessed_wrap(sum(a.value for a in argv))

        check_same_type(argv)
        if is_type(argv, Boolean):
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
        argv = yield from match_arguments(argv, Number, [2, 3])
        if len(argv) == 2:
            base, exponent = argv
            return guessed_wrap(base.value ** exponent.value)

        check_type(argv, Integer)
        base, exponent, modulo = [a.value for a in argv]
        if exponent < 0:
            base = _modular_inverse(base, modulo)
            exponent = -exponent
        return guessed_wrap(pow(base, exponent, modulo))

    def _integer_division(argv):
        argv = yield from match_arguments(argv, Real, 2)
        dividend, divider = [arg.value for arg in argv]
        value = dividend // divider
        if value < 0:
            value = -(-dividend // divider)
        return guessed_wrap(value)

    def _remainder(argv):
        argv = yield from match_arguments(argv, Real, 2)
        dividend, divider = [arg.value for arg in argv]
        if is_type(argv, Integer):
            if dividend // divider >= 0:
                return Integer(dividend % divider)
            else:
                return Integer(-(-dividend % divider))
        return Float(math.fmod(dividend, divider))

    return {
        'ㄱ': _multiply,  # 곱셈
        'ㄷ': _add,  # 덧셈
        'ㅅ': _exponentiate,  # 거듭제곱
        'ㄴㄴ': _integer_division,  # 몫
        'ㄴㅁ': _remainder,  # 나머지
    }
