from typing import Generator, Iterable, Mapping, Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def _listed_equals(
    seqs: Iterable[Sequence[AS.Value]],
) -> Generator[AS.Value, AS.StrictValue, bool]:
    """Check equality for lists of pbhhg values."""
    seqs = list(seqs)
    if not utils.all_equal(len(seq) for seq in seqs):
        return False
    for tiers in zip(*seqs):
        equality = yield from _value_equals(tiers)
        if not equality.value:
            return False
    return True


def _dict_equals(
    dicts: Iterable[Mapping[AS.StrictValue, AS.Value]]
) -> Generator[AS.Value, AS.StrictValue, bool]:
    """Check equality for dicts of pbhhg values."""
    dicts = list(dicts)
    if not dicts:
        return True
    if not utils.all_equal(d.keys() for d in dicts):
        return False
    for k in dicts[0]:
        equality = yield from _value_equals([d[k] for d in dicts])
        if not equality.value:
            return False
    return True


def _value_equals(
    argv: Sequence[AS.Value],
) -> Generator[AS.Value, AS.StrictValue, AS.Boolean]:
    argv = yield from utils.map_strict(argv)
    if utils.is_type(argv, AS.Number):
        return AS.Boolean(utils.all_equal(argv))
    if utils.is_type(argv, AS.List | AS.ErrorValue):
        lists = [seq.value for seq in argv]
        return AS.Boolean((yield from _listed_equals(lists)))
    if utils.is_type(argv, AS.Dict):
        dicts = [d.value for d in argv]
        return AS.Boolean((yield from _dict_equals(dicts)))
    if utils.is_type(argv, AS.IO):
        return AS.Boolean(utils.all_equal(hash(a) for a in argv))
    return AS.Boolean(utils.is_same_type(argv) and utils.all_equal(argv))


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
