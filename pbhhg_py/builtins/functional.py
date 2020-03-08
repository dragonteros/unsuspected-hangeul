from pbhhg_py.abstract_syntax import *
from pbhhg_py.utils import *


class Pipe(Function):
    def __init__(self, funs):
        super().__init__('Piped ')
        self.funs = funs

    def __call__(self, args):
        for fun in self.funs:
            arg = yield from fun(args)
            args = [arg]
        return args[0]


class Collect(Function):
    def __init__(self, _fn):
        super().__init__('Collectedly-Receiving ')
        self._fn = _fn

    def __call__(self, args):
        check_arity(args, 1)
        seq = yield args[0]
        check_type(seq, List)
        return (yield from self._fn(seq.value))


class Spread(Function):
    def __init__(self, _fn):
        super().__init__('Spreadly-Receiving ')
        self._fn = _fn

    def __call__(self, args):
        args = [List(tuple(args))]
        return (yield from self._fn(args))


def build_tbl(proc_functional):
    def _proc(fun):
        return proc_functional(fun, allow=Callable)

    def _pipe(funs):
        funs = yield from [(yield from _proc(fun)) for fun in funs]
        return Pipe(funs)

    def _collect(funs):
        check_arity(funs, 1)
        [fun] = funs
        return Collect((yield from _proc(fun)))

    def _spread(funs):
        check_arity(funs, 1)
        [fun] = funs
        return Spread((yield from _proc(fun)))

    return {
        'ㄴㄱ': _pipe,  # 연결
        'ㅁㅂ': _collect,  # 모아받기
        'ㅂㅂ': _spread,  # 펴받기
    }
