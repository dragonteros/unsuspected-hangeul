"""Control-flow operations."""
from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _throw(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_arity(metadata, argv, 1)
        argv = yield from utils.map_strict(argv)
        argv = utils.check_type(metadata, argv, AS.ErrorValue)
        raise AS.UnsuspectedHangeulError(argv[0])

    def _try(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_arity(metadata, argv, 2)
        try:
            return (yield from utils.recursive_strict(argv[0]))
        except AS.UnsuspectedHangeulError as err:
            fun = yield from utils.strict_functional(metadata, argv[1])
            return (
                yield from proc_functional(metadata, fun)(metadata, [err.err])
            )

    return {
        "ㄷㅈ": _throw,  # 던지다
        "ㅅㄷ": _try,  # 시도하다
    }
