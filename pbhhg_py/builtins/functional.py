from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


class Pipe(Function):
    def __init__(self, funs):
        self.funs = funs

    def __str__(self):
        return '<Piped Function>'

    def __call__(self, args):
        for _fn in self.funs:
            args = [_fn(args)]
        return args[0]


class Collect(Function):
    def __init__(self, _fn, _str, _strict):
        self._fn = _fn
        self._str = _str
        self._strict = _strict

    def __str__(self):
        return self._str

    def __call__(self, args):
        check_arity(args, 1)
        [seq] = self._strict(args)
        check_type(seq, List)
        return self._fn(seq.value)


class Spread(Function):
    def __init__(self, _fn, _str):
        self._fn = _fn
        self._str = _str

    def __str__(self):
        return self._str

    def __call__(self, args):
        return self._fn([List(tuple(args))])


def build_tbl(proc_functional, _strict):
    def _proc(fun):
        return proc_functional(fun, allow=Callable)

    def _pipe(funs):
        funs = [_proc(fun) for fun in funs]
        return Pipe(funs)

    def _collect(funs):
        check_arity(funs, 1)
        [fun] = funs
        return Collect(_proc(fun), str(fun), _strict)

    def _spread(funs):
        check_arity(funs, 1)
        [fun] = funs
        return Spread(_proc(fun), str(fun))

    return {
        'ㄴㄱ': _pipe,  # 연결
        'ㅁㅂ': _collect,  # 모아받기
        'ㅂㅂ': _spread,  # 펴받기
    }
