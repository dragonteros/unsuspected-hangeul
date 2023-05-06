from typing import Generator, Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


class Pipe(AS.Function):
    def __init__(self, evaluations: Sequence[AS.Evaluation]):
        super().__init__("Piped ")
        self._evaluations = evaluations

    def __call__(self, argv: Sequence[AS.Value]) -> AS.EvalContext:
        for evaluation in self._evaluations:
            arg = yield from evaluation(argv)
            argv = [arg]
        return argv[0]


class Collect(AS.Function):
    def __init__(self, evaluation: AS.Evaluation):
        super().__init__("Collectedly-Receiving ")
        self._evaluation = evaluation

    def __call__(self, argv: Sequence[AS.Value]) -> AS.EvalContext:
        [seq] = yield from utils.match_arguments(argv, AS.List, 1)
        return (yield from self._evaluation(seq.value))


class Spread(AS.Function):
    def __init__(self, evaluation: AS.Evaluation):
        super().__init__("Spreadly-Receiving ")
        self._evaluation = evaluation

    def __call__(self, argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = [AS.List(tuple(argv))]
        return (yield from self._evaluation(argv))


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _proc(
        fun: AS.Value,
    ) -> Generator[AS.Value, AS.StrictValue, AS.Evaluation]:
        _fun = yield from utils.strict_functional(fun)
        return proc_functional(_fun, general_callable=True)

    def _pipe(funs: Sequence[AS.Value]) -> AS.EvalContext:
        evaluations = yield from utils.map_strict_with_hook(funs, _proc)
        return Pipe(evaluations)

    def _collect(funs: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(funs, 1)
        return Collect((yield from _proc(funs[0])))

    def _spread(funs: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(funs, 1)
        return Spread((yield from _proc(funs[0])))

    return {
        "ㄴㄱ": _pipe,  # 연결
        "ㅁㅂ": _collect,  # 모아받기
        "ㅂㅂ": _spread,  # 펴받기
    }
