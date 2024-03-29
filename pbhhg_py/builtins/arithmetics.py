import functools
import math
import operator
from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error
from pbhhg_py import utils


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    del proc_functional  # Unused

    def _all(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        # short-circuiting
        for arg in argv:
            [arg] = yield from utils.match_arguments(
                metadata, [arg], AS.Boolean
            )
            if not arg.value:
                return AS.Boolean(False)
        return AS.Boolean(True)

    def _multiply(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_min_arity(metadata, argv, 1)
        first = yield argv[0]
        [first] = utils.check_type(metadata, [first], AS.Number | AS.Boolean)
        if isinstance(first, AS.Boolean):
            return (yield from _all(metadata, argv))

        rest = yield from utils.match_arguments(metadata, argv[1:], AS.Number)
        values = (arg.value for arg in [first, *rest])
        return utils.guessed_wrap(
            functools.reduce(operator.mul, values)
        )  # No init value

    def _any(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        # short-circuiting
        for arg in argv:
            [arg] = yield from utils.match_arguments(
                metadata, [arg], AS.Boolean
            )
            if arg.value:
                return AS.Boolean(True)
        return AS.Boolean(False)

    def _add(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_min_arity(metadata, argv, 1)
        first = yield argv[0]
        [first] = utils.check_type(
            metadata, [first], AS.Number | AS.Boolean | AS.Sequence | AS.Dict
        )
        if isinstance(first, AS.Boolean):
            return (yield from _any(metadata, argv))

        argv = yield from utils.map_strict(argv)
        if isinstance(first, AS.List):
            argv = utils.check_type(metadata, argv, AS.List)
            return AS.List(tuple(item for seq in argv for item in seq.value))
        if isinstance(first, AS.String):
            argv = utils.check_type(metadata, argv, AS.String)
            return AS.String("".join(a.value for a in argv))
        if isinstance(first, AS.Bytes):
            argv = utils.check_type(metadata, argv, AS.Bytes)
            return AS.Bytes(b"".join(a.value for a in argv))
        if isinstance(first, AS.Dict):
            argv = utils.check_type(metadata, argv, AS.Dict)
            merged = {h: (k, v) for a in argv for k, h, v in a.table}
            table = [(k, h, v) for h, (k, v) in merged.items()]
            return AS.Dict(table)
        argv = utils.check_type(metadata, argv, AS.Number)
        return utils.guessed_wrap(sum(a.value for a in argv))

    def _exponentiate(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            metadata, argv, AS.Number, [2, 3]
        )
        if len(argv) == 2:
            base, exponent = argv
            try:
                return utils.guessed_wrap(base.value**exponent.value)
            except ZeroDivisionError:
                raise error.UnsuspectedHangeulDivisionError(
                    metadata, "0의 역수를 구하려고 했습니다."
                ) from None

        argv = utils.check_type(metadata, argv, AS.Integer)
        base, exponent, modulo = [a.value for a in argv]
        try:
            return utils.guessed_wrap(pow(base, exponent, abs(modulo)))
        except ValueError:
            raise error.UnsuspectedHangeulArithmeticError(
                metadata, f"법 {modulo}에 대한 {base}의 {exponent}제곱을 구할 수 없습니다."
            ) from None

    def _integer_division(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(metadata, argv, AS.Real, 2)
        dividend, divider = [arg.value for arg in argv]
        try:
            value = dividend // divider
            if value < 0:
                value = -(-dividend // divider)
        except ZeroDivisionError:
            raise error.UnsuspectedHangeulDivisionError(
                metadata, "0으로 나누려고 했습니다."
            ) from None
        return utils.guessed_wrap(value)

    def _remainder(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(metadata, argv, AS.Real, 2)
        if utils.is_type(argv, AS.Integer):
            dividend, divider = [arg.value for arg in argv]
            try:
                if dividend // divider >= 0:
                    return AS.Integer(dividend % divider)
                else:
                    return AS.Integer(-(-dividend % divider))
            except ZeroDivisionError:
                raise error.UnsuspectedHangeulDivisionError(
                    metadata, "0으로 나누려고 했습니다."
                ) from None
        dividend, divider = [arg.value for arg in argv]
        return AS.Float(math.fmod(dividend, divider))

    return {
        "ㄱ": _multiply,  # 곱셈
        "ㄷ": _add,  # 덧셈
        "ㅅ": _exponentiate,  # 거듭제곱
        "ㄴㄴ": _integer_division,  # 몫
        "ㄴㅁ": _remainder,  # 나머지
    }
