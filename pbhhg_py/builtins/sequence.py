from pbhhg_py.abstract_syntax import *
from pbhhg_py.utils import *


def build_tbl(proc_functional):
    def _len(argv):
        [seq] = yield from match_arguments(argv, Sequence, 1)
        return Integer(len(seq.value))

    def _slice(argv):
        check_arity(argv, [2, 3, 4])
        argv = yield from [(yield arg) for arg in argv]
        check_type(argv[0], Sequence)
        check_type(argv[1:], Integer)

        seq, *rest = [arg.value for arg in argv]
        start, end, step = match_defaults(rest, 3, [len(seq), 1])
        result = seq[start:end:step]
        if isinstance(argv[0], List):
            return List(result)
        elif isinstance(argv[0], String):
            return String(result)
        elif isinstance(argv[0], Bytes):
            return Bytes(result)

    def _map(argv):
        check_arity(argv, 2)
        seq = yield argv[0]
        check_type(seq, List)  # ?
        _fn = yield from proc_functional(argv[1])
        value = yield from [(yield from _fn([arg])) for arg in seq.value]
        return List(value)

    def _filter(argv):  # maybe lazy later?
        check_arity(argv, 2)
        seq = yield argv[0]
        check_type(seq, List)  # ?
        _fn = yield from proc_functional(argv[1])
        fit_check = yield from [(yield (yield from _fn([arg]))) for arg in seq.value]
        check_type(fit_check, Boolean)
        zipped = zip(seq.value, fit_check)
        return List(tuple(arg for arg, fits in zipped if fits.value))

    def _fold(argv):
        check_arity(argv, [2, 3])
        init = None
        if len(argv) == 3:
            x, init, y = argv
            argv = [x, y]

        preserved_argv = argv
        argv = yield from [(yield arg) for arg in argv]
        from_right = is_type(argv[0], List)
        maybe_reversed = reversed if from_right else lambda x: x

        fun, seq = maybe_reversed(argv)
        _fn, _ = maybe_reversed(preserved_argv)
        _fn = yield from proc_functional(_fn, stricted=fun)
        check_type(seq, List)

        acc = init
        feed = list(maybe_reversed(seq.value))
        if init is None:
            acc = feed[0]
            feed = feed[1:]

        for item in feed:
            args = list(maybe_reversed([acc, item]))
            acc = yield from _fn(args)
        return acc

    return {
        'ㅈㄷ': _len,  # 장단
        'ㅂㅈ': _slice,  # 발췌
        'ㅁㄷ': _map,  # ~마다
        'ㅅㅂ': _filter,  # 선별
        'ㅅㄹ': _fold,  # 수렴
    }
