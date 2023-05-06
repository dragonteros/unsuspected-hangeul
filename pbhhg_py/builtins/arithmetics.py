import functools
import math
import operator
from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error
from pbhhg_py import utils


def _extended_gcd(a: int, b: int):
    """Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x, x_old, y, y_old = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y, y_old = y_old, y - q * y_old
        x, x_old = x_old, x - q * x_old
    return b, x, y


def _modular_inverse(a: int, mod: int):
    a = a % mod
    try:
        return pow(a, -1, mod)
    except ValueError:
        g, inverse, _ = _extended_gcd(a, mod)
        if g == 1:
            return inverse % mod
    raise error.UnsuspectedHangeulArithmeticError(
        f"{mod}를 법으로 한 {a}의 역원이 존재하지 않습니다."
    )


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    del proc_functional  # Unused

    def _multiply(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_min_arity(argv, 1)
        argv = yield from utils.map_strict(argv)
        argv = utils.check_type(argv, AS.Number | AS.Boolean)
        if utils.is_type(argv, AS.Number):
            values = (arg.value for arg in argv)
            return utils.guessed_wrap(
                functools.reduce(operator.mul, values)
            )  # No init

        utils.check_same_type(argv)
        return AS.Boolean(all(a.value for a in argv))

    def _add(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_min_arity(argv, 1)
        argv = yield from utils.map_strict(argv)
        utils.check_type(argv, AS.Number | AS.Boolean | AS.Sequence | AS.Dict)
        if utils.is_type(argv, AS.Number):
            return utils.guessed_wrap(sum(a.value for a in argv))

        utils.check_same_type(argv)
        if utils.is_type(argv, AS.Boolean):
            return AS.Boolean(any(a.value for a in argv))
        elif utils.is_type(argv, AS.List):
            return AS.List(tuple(item for seq in argv for item in seq.value))
        elif utils.is_type(argv, AS.String):
            return AS.String("".join(a.value for a in argv))
        elif utils.is_type(argv, AS.Bytes):
            return AS.Bytes(b"".join(a.value for a in argv))
        elif utils.is_type(argv, AS.Dict):
            return AS.Dict({k: a.value[k] for a in argv for k in a.value})
        assert False

    def _exponentiate(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(argv, AS.Number, [2, 3])
        if len(argv) == 2:
            base, exponent = argv
            try:
                return utils.guessed_wrap(base.value**exponent.value)
            except ZeroDivisionError:
                raise error.UnsuspectedHangeulDivisionError(
                    "0의 역수를 구하려고 했습니다."
                )

        argv = utils.check_type(argv, AS.Integer)
        base, exponent, modulo = [a.value for a in argv]
        if exponent < 0:
            base = _modular_inverse(base, modulo)
            exponent = -exponent
        return utils.guessed_wrap(pow(base, exponent, modulo))

    def _integer_division(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(argv, AS.Real, 2)
        dividend, divider = [arg.value for arg in argv]
        try:
            value = dividend // divider
            if value < 0:
                value = -(-dividend // divider)
        except ZeroDivisionError:
            raise error.UnsuspectedHangeulDivisionError("0으로 나누려고 했습니다.")
        return utils.guessed_wrap(value)

    def _remainder(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(argv, AS.Real, 2)
        if utils.is_type(argv, AS.Integer):
            dividend, divider = [arg.value for arg in argv]
            try:
                if dividend // divider >= 0:
                    return AS.Integer(dividend % divider)
                else:
                    return AS.Integer(-(-dividend % divider))
            except ZeroDivisionError:
                raise error.UnsuspectedHangeulDivisionError("0으로 나누려고 했습니다.")
        dividend, divider = [arg.value for arg in argv]
        return AS.Float(math.fmod(dividend, divider))

    return {
        "ㄱ": _multiply,  # 곱셈
        "ㄷ": _add,  # 덧셈
        "ㅅ": _exponentiate,  # 거듭제곱
        "ㄴㄴ": _integer_division,  # 몫
        "ㄴㅁ": _remainder,  # 나머지
    }
