from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    del proc_functional  # Unused

    def _split(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(argv, AS.String, [1, 2])
        src, delimiter = utils.match_defaults(argv, 2, [AS.String("")])
        if delimiter.value:
            pieces = src.value.split(delimiter.value)
        else:
            pieces = src.value
        return AS.List(tuple(AS.String(piece) for piece in pieces))

    def _join(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, [1, 2])
        argv = yield from utils.map_strict(argv)
        seq, delimiter = utils.match_defaults(argv, 2, [AS.String("")])
        [seq] = utils.check_type([seq], AS.List)
        [delimiter] = utils.check_type([delimiter], AS.String)

        pieces = yield from utils.map_strict(seq.value)
        pieces = utils.check_type(pieces, AS.String)
        return AS.String(delimiter.value.join(piece.value for piece in pieces))

    return {
        "ㅂㄹ": _split,  # 분리
        "ㄱㅁ": _join,  # 꿰매다
    }
