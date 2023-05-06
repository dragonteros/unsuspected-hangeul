"""Bitwise operations."""
from typing import Callable, Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils

Op = Callable[[int], int] | Callable[[int, int], int]


def _shift_left(operand: int, num_bits: int):
    if num_bits < 0:
        return operand >> (-num_bits)
    return operand << num_bits


def build_tbl(
    proc_functional: utils.ProcFunctional,
):
    del proc_functional  # Unused

    def _wrap(op: Op, arity: int):
        def _proc(argv: Sequence[AS.Value]) -> AS.EvalContext:
            argv = yield from utils.match_arguments(argv, AS.Integer, arity)
            return AS.Integer(op(*(arg.value for arg in argv)))

        return _proc

    return {
        "ㅂㄷ": {
            "ㄱ": _wrap(lambda x, y: x & y, 2),  # 비트별 논리곱
            "ㄷ": _wrap(lambda x, y: x | y, 2),  # 비트별 논리합
            "ㅁ": _wrap(lambda x: ~x, 1),  # 비트별 논리부정
            "ㅂ": _wrap(lambda x, y: x ^ y, 2),  # 비트별 배타적 논리합
            "ㅈ": _wrap(_shift_left, 2),  # 비트 자리 옮김
        }
    }
