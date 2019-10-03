from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *

Sequence = (List, String, Bytes)


def build_tbl(proc_functional, _strict):
    def _len(argv):
        check_arity(argv, 1)
        [seq] = _strict(argv)
        check_type(seq, Sequence)
        return Number(len(seq.value))

    def _slice(argv):
        check_arity(argv, [2, 3, 4])
        argv = _strict(argv)
        check_type(argv[0], Sequence)
        check_type(argv[1:], Number)

        seq = argv[0].value
        start = int(round(argv[1].value))
        end = int(round(argv[2].value)) if len(argv) > 2 else len(seq)
        step = int(round(argv[3].value)) if len(argv) > 3 else 1
        result = seq[start:end:step]
        if isinstance(argv[0], List):
            return List(result)
        elif isinstance(argv[0], String):
            return String(result)
        elif isinstance(argv[0], Bytes):
            return Bytes(result)

    def _map(argv):
        check_arity(argv, 2)
        _fn = proc_functional(argv[1])
        [seq] = _strict(argv[:1])
        check_type(seq, List)  # ?
        return List(tuple(_fn([arg]) for arg in seq.value))

    def _filter(argv):  # maybe lazy later?
        check_arity(argv, 2)
        _fn = proc_functional(argv[1])
        [seq] = _strict(argv[:1])
        check_type(seq, List)  # ?
        fit_check = [_fn([arg]) for arg in seq.value]
        fit_check = _strict(fit_check)
        check_type(fit_check, Boolean)
        return List(tuple(arg for arg, fits in zip(seq.value, fit_check) if fits.value))

    def _fold(argv):
        check_arity(argv, [2, 3])
        init = None
        if len(argv) == 3:
            x, init, y = argv
            argv = [x, y]

        preserved_argv = argv
        argv = _strict(argv)
        from_right = is_type(argv[0], List)
        maybe_reversed = reversed if from_right else lambda x: x

        fun, seq = maybe_reversed(argv)
        _fn, _ = maybe_reversed(preserved_argv)
        _fn = proc_functional(_fn, stricted=fun)
        check_type(seq, List)

        acc = init
        feed = list(maybe_reversed(seq.value))
        if init is None:
            acc = feed[0]
            feed = feed[1:]

        for item in feed:
            args = list(maybe_reversed([acc, item]))
            acc = _fn(args)
        return acc

    return {
        'ㅈㄷ': _len,  # 장단
        'ㅂㅈ': _slice,  # 발췌
        'ㅁㄷ': _map,  # ~마다
        'ㅅㅂ': _filter,  # 선별
        'ㅅㄹ': _fold,  # 수렴
    }
