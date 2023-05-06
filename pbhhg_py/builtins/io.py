import io
from typing import BinaryIO, Callable, Generator, Literal, Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error
from pbhhg_py import parse
from pbhhg_py import utils

DoIO = Callable[
    [AS.IO], Generator[AS.Value, AS.StrictValue, AS.NonIOStrictValue]
]
EvalIOContext = Generator[AS.Value, AS.StrictValue, AS.IO]

_MODE_TABLE: dict[str, Literal["rb", "wb", "ab", "r+b", "w+b", "a+b"]] = {
    "ㄹ": "rb",
    "ㅈㄹ": "wb",
    "ㅈㄱ": "ab",
    "ㄹㅈㄹ": "r+b",  # open R/W without resetting file content
    "ㅈㄹㄹ": "w+b",  # open R/W after resetting file content
    "ㅈㄱㄹ": "a+b",
}


class File(AS.Function):
    def __init__(self, file: BinaryIO):
        super().__init__("File-accessing ")
        self._file = file

    def __call__(self, argv: Sequence[AS.Value]) -> EvalIOContext:
        utils.check_min_arity(argv, 1)
        command = yield argv[-1]
        [command] = utils.check_type([command], AS.Integer)
        command_str = parse.encode_number(command.value)
        try:
            _fn = {
                "ㄹ": self._read,
                "ㅈㄹ": self._write,  # 출력
                "ㅈ": self._seek_or_tell,  # 찾다
                "ㄱ": self._truncate,  # 끊다
            }[command_str]
            return (yield from _fn(argv))
        except KeyError:
            raise error.UnsuspectedHangeulValueError(
                f"{command_str}은 파일 객체가 인식하지 못하는 명령입니다."
            )
        except OSError as e:
            raise error.UnsuspectedHangeulOSError(
                f"운영체제 오류 errno={e.errno}", e.errno
            )

    def _read(self, argv: Sequence[AS.Value]) -> EvalIOContext:
        utils.check_arity(argv, 2)
        [count] = yield from utils.match_arguments([argv[0]], AS.Integer)
        content = self._file.read(count.value or -1)
        return (yield from _return([AS.Bytes(content)]))

    def _write(self, argv: Sequence[AS.Value]) -> EvalIOContext:
        utils.check_arity(argv, 2)
        [content] = yield from utils.match_arguments([argv[0]], AS.Bytes)
        count = self._file.write(content.value)
        return (yield from _return([AS.Integer(count)]))

    def _seek_or_tell(self, argv: Sequence[AS.Value]) -> EvalIOContext:
        utils.check_max_arity(argv, 3)
        if len(argv) == 1:
            pos = self._file.tell()
        else:
            [offset] = yield from utils.match_arguments([argv[-2]], AS.Integer)
            whence = io.SEEK_SET
            if len(argv) > 2:
                [_whence] = yield from utils.match_arguments(
                    [argv[-3]], AS.Integer
                )
                whence = {
                    "ㅅㅈㅂㄷ": io.SEEK_SET,  # 시작부터
                    "ㅈㄱㅂㄷ": io.SEEK_CUR,  # 지금부터
                    "ㄱㅂㄷ": io.SEEK_END,  # 끝부터
                }[parse.encode_number(_whence.value)]
            pos = self._file.seek(offset.value, whence)
        return (yield from _return([AS.Integer(pos)]))

    def _truncate(self, argv: Sequence[AS.Value]) -> EvalIOContext:
        argv = yield from utils.match_arguments(argv, AS.Integer, max_arity=2)
        new_size = self._file.truncate(*[arg.value for arg in argv[:-1]])
        return (yield from _return([AS.Integer(new_size)]))


def _input(argv: Sequence[AS.Value]) -> EvalIOContext:
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


def _print(argv: Sequence[AS.Value]) -> EvalIOContext:
    utils.check_arity(argv, 1)
    argv = yield from utils.map_strict(argv)
    [content] = utils.check_type([argv[0]], AS.String)

    def _fn(do_IO: DoIO) -> AS.EvalContext:
        del do_IO  # Unused
        print(content.value, flush=True)
        return AS.Nil()
        yield

    return AS.IO("ㅈㄹ", tuple(argv), _fn)


def _return(argv: Sequence[AS.Value]) -> EvalIOContext:
    utils.check_arity(argv, 1)
    argv = yield from utils.map_strict(argv)

    def _fn(do_IO: DoIO) -> AS.EvalContext:
        del do_IO  # Unused
        return argv[0]
        yield

    return AS.IO("ㄱㅅ", tuple(argv), _fn)


def _file(argv: Sequence[AS.Value]) -> EvalIOContext:
    utils.check_arity(argv, 2)
    argv = yield from utils.map_strict(argv)
    [path_or_fd] = utils.check_type([argv[0]], AS.Integer | AS.String)
    [mode] = utils.check_type([argv[1]], AS.Integer)

    mode_str = parse.encode_number(mode.value)
    try:
        _mode = _MODE_TABLE[mode_str]
    except KeyError:
        raise error.UnsuspectedHangeulValueError(
            f"{mode_str}은 기본 제공 함수 ㄱㄴ이 이해하는 파일 열기 방식이 아닙니다."
        )

    def _fn(do_IO: DoIO) -> AS.EvalContext:
        del do_IO  # Unused
        return File(open(path_or_fd.value, _mode))
        yield

    return AS.IO("ㄱㄴ", (path_or_fd, mode), _fn)


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _bind(argv: Sequence[AS.Value]) -> EvalIOContext:
        utils.check_arity(argv, [2, 3])
        [io_to_bind] = yield from utils.match_arguments([argv[0]], AS.IO)
        resolve = yield from utils.strict_functional(argv[1])
        reject = AS.Nil()
        if len(argv) == 3:
            reject = yield from utils.strict_functional(argv[2])

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            try:
                arg = yield from do_IO(io_to_bind)
            except AS.UnsuspectedHangeulError as e:
                if isinstance(reject, AS.Nil):
                    raise e
                result = yield from proc_functional(reject)(e.argv)
                result = yield result
                utils.check_type([result], AS.IO)
                return result

            result = yield from proc_functional(resolve)([arg])
            result = yield result
            utils.check_type([result], AS.IO)
            return result

        return AS.IO("ㄱㄹ", (io_to_bind, resolve, reject), _fn)

    return {
        "ㄹ": _input,  # 입력
        "ㅈㄹ": _print,  # 출력
        "ㄱㅅ": _return,  # 감싸다
        "ㄱㄹ": _bind,  # ~기로 하다
        "ㄱㄴ": _file,  # 꺼내다
    }
