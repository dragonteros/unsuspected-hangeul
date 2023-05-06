from typing import Callable, Generator, Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils

DoIO = Callable[
    [AS.IO], Generator[AS.Value, AS.StrictValue, AS.NonIOStrictValue]
]


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _input(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, 0)
        argv = yield from utils.map_strict(argv)

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            try:
                return AS.String(input(""))
            except EOFError:
                return AS.Nil()
            yield

        return AS.IO("ㄹ", tuple(argv), _fn)
        yield

    def _print(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, 1)
        argv = yield from utils.map_strict(argv)
        [content] = utils.check_type([argv[0]], AS.String)

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            print(content.value, flush=True)
            return AS.Nil()
            yield

        return AS.IO("ㅈㄹ", tuple(argv), _fn)

    def _return(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, 1)
        argv = yield from utils.map_strict(argv)

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            return argv[0]
            yield

        return AS.IO("ㄱㅅ", tuple(argv), _fn)
        yield

    def _bind(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, [2, 3])
        [io_to_bind] = yield from utils.match_arguments([argv[0]], AS.IO)
        resolve = yield from utils.strict_functional(argv[1])
        reject = AS.Nil()
        if len(argv) == 3:
            reject = yield from utils.strict_functional(argv[2])

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            try:
                result = yield from do_IO(io_to_bind)
            except AS.UnsuspectedHangeulError as e:
                if isinstance(reject, AS.Nil):
                    raise e
                return (yield from proc_functional(reject)(e.argv))

            return (yield from proc_functional(resolve)([result]))

        return AS.IO("ㄱㄹ", (io_to_bind, resolve, reject), _fn)
        yield

    # def _file(argv: Sequence[AS.Value]) -> AS.EvalContext:
    #     utils.check_min_arity(argv, 1)
    #     # fd or path, [mode=rb, []] => File_obj  # meow TODO
    #     yield

    return {
        "ㄹ": _input,  # 입력
        "ㅈㄹ": _print,  # 출력
        "ㄱㅅ": _return,  # 감싸다
        "ㄱㄹ": _bind,  # ~기로 하다
        # "ㄱㄴ": _file,  # 꺼내다
    }
