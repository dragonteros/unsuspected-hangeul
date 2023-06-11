from typing import Generator, Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def _value_equals(
    argv: Sequence[AS.Value],
) -> Generator[AS.Value, AS.StrictValue, AS.Boolean]:
    key = None
    for arg in argv:
        arg = yield arg
        _key = yield from arg.as_key()
        if key is None:
            key = _key
        elif key != _key:
            return AS.Boolean(False)
    return AS.Boolean(True)


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    del proc_functional  # Unused

    def _equals(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        del metadata  # Unused
        return _value_equals(argv)

    def _negate(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        [arg] = yield from utils.match_arguments(metadata, argv, AS.Boolean, 1)
        return AS.Boolean(not arg.value)

    def _less_than(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(metadata, argv, AS.Real, 2)
        return AS.Boolean(argv[0].value < argv[1].value)

    def _true(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_arity(metadata, argv, 0)
        return AS.Boolean(True)
        yield

    def _false(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_arity(metadata, argv, 0)
        return AS.Boolean(False)
        yield

    return {
        "ㄴ": _equals,  # 같다 (<- 는)
        "ㅁ": _negate,  # 부정 (<- 못하다)
        "ㅈ": _less_than,  # 작다
        "ㅈㅈ": _true,  # 진짜
        "ㄱㅈ": _false,  # 가짜
    }
