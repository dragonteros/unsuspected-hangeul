from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    del proc_functional  # Unused

    def _split(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            metadata, argv, AS.String | AS.Bytes, [1, 2]
        )
        if isinstance(argv[0], AS.String):
            argv = utils.check_type(metadata, argv, AS.String)
            _argv = [arg.value for arg in argv]
            src, delimiter = utils.match_defaults(metadata, _argv, 2, [""])
            pieces = src.split(delimiter) if delimiter else src
            return AS.List(tuple(AS.String(piece) for piece in pieces))
        else:
            argv = utils.check_type(metadata, argv, AS.Bytes)
            _argv = [arg.value for arg in argv]
            src, delimiter = utils.match_defaults(metadata, _argv, 2, [b""])
            pieces = (
                src.split(delimiter)
                if delimiter
                else [src[i : i + 1] for i in range(len(src))]
            )
            return AS.List(tuple(AS.Bytes(piece) for piece in pieces))

    def _join(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_arity(metadata, argv, [1, 2])
        argv = yield from utils.map_strict(argv)

        [seq] = utils.check_type(metadata, [argv[0]], AS.List)
        pieces = yield from utils.map_strict(seq.value)
        pieces = utils.check_type(metadata, pieces, AS.String | AS.Bytes)

        if isinstance(pieces[0], AS.String):
            pieces = utils.check_type(metadata, pieces, AS.String)
            delimiter = AS.String("")
            if len(argv) > 1:
                [delimiter] = utils.check_type(metadata, [argv[1]], AS.String)
            return AS.String(
                delimiter.value.join(piece.value for piece in pieces)
            )
        else:
            pieces = utils.check_type(metadata, pieces, AS.Bytes)
            delimiter = AS.Bytes(b"")
            if len(argv) > 1:
                [delimiter] = utils.check_type(metadata, [argv[1]], AS.Bytes)
            return AS.Bytes(
                delimiter.value.join(piece.value for piece in pieces)
            )

    return {
        "ㅂㄹ": _split,  # 분리
        "ㄱㅁ": _join,  # 꿰매다
    }
