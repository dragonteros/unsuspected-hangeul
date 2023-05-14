"""Does math stuff."""
import cmath
import math
from typing import Any, Callable, Sequence, TypeVar

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def _isclose(a: complex, b: complex):
    return cmath.isclose(a, b, abs_tol=1e-16)


def _round_to_inf(x: float):
    return math.ceil(x) if x > 0 else math.floor(x)


_ValueT = TypeVar("_ValueT", bound=AS.Number | AS.Boolean)


def build_tbl(proc_functional: utils.ProcFunctional):
    del proc_functional  # Unused

    def _wrap(
        _fn: Any,
        arity: int,
        arg_type: type[_ValueT],
        ret_type: Callable[..., AS.StrictValue],
    ) -> AS.Evaluation:
        def _proc(
            metadata: AS.Metadata, argv: Sequence[AS.Value]
        ) -> AS.EvalContext:
            argv = yield from utils.match_arguments(
                metadata, argv, arg_type, arity
            )
            return ret_type(_fn(*(arg.value for arg in argv)))

        return _proc

    def _wrap2(
        _fn_real: Callable[[float], float],
        _fn_complex: Callable[[complex], complex],
    ) -> AS.Evaluation:
        def _proc(
            metadata: AS.Metadata, argv: Sequence[AS.Value]
        ) -> AS.EvalContext:
            [arg] = yield from utils.match_arguments(
                metadata, argv, AS.Number, 1
            )
            try:
                assert isinstance(arg.value, int | float)
                return AS.Float(_fn_real(arg.value))
            except (TypeError, ValueError, AssertionError):
                return AS.Complex(_fn_complex(arg.value))

        return _proc

    _atan1 = _wrap2(math.atan, cmath.atan)
    _atan2 = _wrap(math.atan2, 2, AS.Real, AS.Float)

    def _atan(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        _fn = _atan2 if len(argv) == 2 else _atan1
        return (yield from _fn(metadata, argv))

    return {
        "ㅅ": {
            "ㅂ": math.pi,  # 파이
            "ㅈ": math.e,  # 자연상수
            "ㅁ": math.inf,  # 무한대
            "ㄴ": math.nan,  # NaN
            "ㄱ": _wrap(_isclose, 2, AS.Number, AS.Boolean),  # 가깝다
            "ㄴㄴ": _wrap(cmath.isnan, 1, AS.Number, AS.Boolean),  # ~ ㄴ ㄴㅎㄷ
            "ㅁㄴ": _wrap(cmath.isinf, 1, AS.Number, AS.Boolean),  # ~ ㅁ ㄴㅎㄷ
            "ㅈㄷ": _wrap(abs, 1, AS.Number, utils.guessed_wrap),  # 절댓값
            "ㄹㄱ": _wrap2(math.log, cmath.log),  # log
            "ㅅㄴ": _wrap2(math.sin, cmath.sin),  # sin
            "ㄴㅅ": _wrap2(math.asin, cmath.asin),
            "ㄱㅅ": _wrap2(math.cos, cmath.cos),  # cos
            "ㅅㄱ": _wrap2(math.acos, cmath.acos),
            "ㄷㄴ": _wrap2(math.tan, cmath.tan),  # tan
            "ㄴㄷ": _atan,
            "ㅂㄹ": {  # 자르기
                "ㄱ": _wrap(math.trunc, 1, AS.Real, AS.Integer),
                "ㄴ": _wrap(math.floor, 1, AS.Real, AS.Integer),
                "ㄷ": _wrap(round, 1, AS.Real, AS.Integer),
                "ㄹ": _wrap(math.ceil, 1, AS.Real, AS.Integer),
                "ㅁ": _wrap(_round_to_inf, 1, AS.Real, AS.Integer),
            },
        }
    }
