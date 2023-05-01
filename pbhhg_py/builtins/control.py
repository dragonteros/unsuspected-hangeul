
"""Control-flow operations."""
from pbhhg_py import utils
from pbhhg_py import error

def build_tbl(proc_functional) -> dict[str, utils.Coroutine]:
    def _throw(argv) -> utils.Coroutine:
        raise error.UnsuspectedHangeulError(argv)
        yield

    def _try(argv) -> utils.Coroutine:
        utils.check_arity(argv, 2)
        try:
            return (yield argv[0])
        except error.UnsuspectedHangeulError as e:
            _fn = yield from proc_functional(argv[1])
            return (yield from _fn(e.argv))

    return {
        'ㄷㅈ': _throw,  # 던지다
        'ㅅㄷ': _try,  # 시도하다
    }
