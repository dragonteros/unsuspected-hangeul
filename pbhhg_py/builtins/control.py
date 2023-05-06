"""Control-flow operations."""
from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error
from pbhhg_py import utils


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _throw(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.map_strict(argv)
        raise error.UnsuspectedHangeulCustomError(argv)
        yield

    def _try(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, 2)
        try:
            return (yield argv[0])
        except AS.UnsuspectedHangeulError as e:
            fun = yield from utils.strict_functional(argv[1])
            return (yield from proc_functional(fun)(e.argv))

    return {
        "ㄷㅈ": _throw,  # 던지다
        "ㅅㄷ": _try,  # 시도하다
    }
