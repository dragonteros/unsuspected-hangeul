from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _len(argv: Sequence[AS.Value]) -> AS.EvalContext:
        [seq] = yield from utils.match_arguments(argv, AS.Sequence, 1)
        return AS.Integer(len(seq.value))

    def _slice(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, [2, 3, 4])
        argv = yield from utils.map_strict(argv)
        [seq] = utils.check_type(argv[:1], AS.Sequence)
        rest = utils.check_type(argv[1:], AS.Integer)

        _rest = [arg.value for arg in rest]
        start, end, step = utils.match_defaults(_rest, 3, [len(seq.value), 1])
        result = seq.value[start:end:step]
        if isinstance(result, str):
            return AS.String(result)
        elif isinstance(result, bytes):
            return AS.Bytes(result)
        else:
            return AS.List(result)

    def _map(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, 2)
        seq = yield argv[0]
        [seq] = utils.check_type([seq], AS.List)
        fun = yield from utils.strict_functional(argv[1])
        _fn = proc_functional(fun)
        value = yield from utils.map_strict_with_hook(
            seq.value, lambda x: _fn([x])
        )
        return AS.List(tuple(value))

    def _filter(argv: Sequence[AS.Value]) -> AS.EvalContext:
        # maybe lazy later?
        utils.check_arity(argv, 2)
        seq = yield argv[0]
        [seq] = utils.check_type([seq], AS.List)
        fun = yield from utils.strict_functional(argv[1])
        _fn = proc_functional(fun)
        fit_check = yield from utils.map_strict_with_hook(
            seq.value, lambda x: _fn([x])
        )
        fit_check = yield from utils.map_strict(fit_check)
        fit_check = utils.check_type(fit_check, AS.Boolean)
        zipped = zip(seq.value, fit_check)
        return AS.List(tuple(arg for arg, fits in zipped if fits.value))

    def _fold(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, [2, 3])
        init = None
        if len(argv) == 3:
            x, init, y = argv
            argv = [x, y]

        first_arg = yield argv[0]
        from_right = utils.is_type([first_arg], AS.List)
        step = -1 if from_right else 1

        fun, seq = argv[::step]
        fun = yield from utils.strict_functional(fun)
        _fn = proc_functional(fun)
        [seq] = utils.check_type([(yield seq)], AS.List)

        acc = init
        feed = seq.value[::step]
        if acc is None:
            acc = feed[0]
            feed = feed[1:]

        for item in feed:
            args = [acc, item][::step]
            acc = yield from _fn(args)
        return acc

    return {
        "ㅈㄷ": _len,  # 장단
        "ㅂㅈ": _slice,  # 발췌
        "ㅁㄷ": _map,  # ~마다
        "ㅅㅂ": _filter,  # 선별
        "ㅅㄹ": _fold,  # 수렴
    }
