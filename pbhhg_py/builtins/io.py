import io
import sys
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

    def __call__(
        self, metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> EvalIOContext:
        utils.check_min_arity(metadata, argv, 1)
        command = yield argv[-1]
        [command] = utils.check_type(metadata, [command], AS.Integer)
        command_str = parse.encode_number(command.value)
        try:
            _fn = {
                "ㄷ": self._close,  # 닫다
                "ㄹ": self._read,
                "ㅈㄹ": self._write,  # 출력
                "ㅈ": self._seek_or_tell,  # 찾다
                "ㄱ": self._truncate,  # 끊다
            }[command_str]
            return (yield from _fn(metadata, argv))
        except KeyError:
            raise error.UnsuspectedHangeulValueError(
                metadata, f"{command_str}은 파일 객체가 인식하지 못하는 명령입니다."
            ) from None
        except OSError as err:
            raise error.UnsuspectedHangeulOSError(
                metadata, f"운영체제 오류 errno={err.errno}", err.errno
            ) from None

    def _close(
        self, metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> EvalIOContext:
        utils.check_arity(metadata, argv, 1)

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            self._file.close()
            return AS.Nil()
            yield

        return AS.IO("File::_close", (self,), _fn)
        yield

    def _read(
        self, metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> EvalIOContext:
        utils.check_arity(metadata, argv, 2)
        [count] = yield from utils.match_arguments(
            metadata, [argv[0]], AS.Integer
        )

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            content = self._file.read(count.value)  # -1 for all
            return AS.Bytes(content)
            yield

        return AS.IO("File::_read", (self, count), _fn)

    def _write(
        self, metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> EvalIOContext:
        utils.check_arity(metadata, argv, 2)
        [content] = yield from utils.match_arguments(
            metadata, [argv[0]], AS.Bytes
        )

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            count = self._file.write(content.value)
            return AS.Integer(count)
            yield

        return AS.IO("File::_write", (self, content), _fn)

    def _seek_or_tell(
        self, metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> EvalIOContext:
        utils.check_max_arity(metadata, argv, 3)
        if len(argv) == 1:

            def _fn(do_IO: DoIO) -> AS.EvalContext:
                del do_IO  # Unused
                pos = self._file.tell()
                return AS.Integer(pos)
                yield

            return AS.IO("File::_seek_or_tell", (self,), _fn)

        argv = yield from utils.map_strict(argv)
        [offset] = yield from utils.match_arguments(
            metadata, [argv[-2]], AS.Integer
        )
        whence = io.SEEK_SET
        if len(argv) > 2:
            [_whence] = yield from utils.match_arguments(
                metadata, [argv[-3]], AS.Integer
            )
            try:
                whence = {
                    "ㅅㅈㅂㄷ": io.SEEK_SET,  # 시작부터
                    "ㅈㄱㅂㄷ": io.SEEK_CUR,  # 지금부터
                }[parse.encode_number(_whence.value)]
            except KeyError:
                raise error.UnsuspectedHangeulValueError(
                    metadata,
                    f"파일 객체의 ㅈ 명령에 주는 위치 인수로 {_whence.value}은 " "적절하지 않습니다.",
                ) from None

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            pos = self._file.seek(offset.value, whence)
            return AS.Integer(pos)
            yield

        return AS.IO("File::_seek_or_tell", (self, *argv[:-1]), _fn)

    def _truncate(
        self, metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> EvalIOContext:
        _argv = yield from utils.match_arguments(
            metadata, argv, AS.Integer, max_arity=2
        )

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            del do_IO  # Unused
            new_size = self._file.truncate(*[arg.value for arg in _argv[:-1]])
            return AS.Integer(new_size)
            yield

        return AS.IO("File::_truncate", (self, *_argv[:-1]), _fn)


def _input(metadata: AS.Metadata, argv: Sequence[AS.Value]) -> EvalIOContext:
    utils.check_arity(metadata, argv, 0)
    argv = yield from utils.map_strict(argv)

    def _fn(do_IO: DoIO) -> AS.EvalContext:
        del do_IO  # Unused
        try:
            return AS.String(input(""))
        except EOFError:
            return AS.Nil()
        except OSError as err:
            raise error.UnsuspectedHangeulOSError(
                metadata, f"운영체제 오류 errno={err.errno}", err.errno
            ) from None
        yield

    return AS.IO("ㄹ", tuple(argv), _fn)


def _print(metadata: AS.Metadata, argv: Sequence[AS.Value]) -> EvalIOContext:
    utils.check_arity(metadata, argv, 1)
    argv = yield from utils.map_strict(argv)
    [content] = utils.check_type(metadata, [argv[0]], AS.String)

    def _fn(do_IO: DoIO) -> AS.EvalContext:
        del do_IO  # Unused
        try:
            print(content.value, flush=True)
        except OSError as err:
            raise error.UnsuspectedHangeulOSError(
                metadata, f"운영체제 오류 errno={err.errno}", err.errno
            ) from None
        return AS.Nil()
        yield

    return AS.IO("ㅈㄹ", tuple(argv), _fn)


def _return(metadata: AS.Metadata, argv: Sequence[AS.Value]) -> EvalIOContext:
    utils.check_arity(metadata, argv, 1)
    # NOTE(dragonteros): Evaluate everything before moving to IO phase
    argv = yield from utils.map_strict_with_hook(argv, utils.recursive_strict)

    def _fn(do_IO: DoIO) -> AS.EvalContext:
        del do_IO  # Unused
        return argv[0]
        yield

    return AS.IO("ㄱㅅ", tuple(argv), _fn)


def _file(metadata: AS.Metadata, argv: Sequence[AS.Value]) -> EvalIOContext:
    utils.check_arity(metadata, argv, 2)
    argv = yield from utils.map_strict(argv)
    [path_or_fd] = utils.check_type(
        metadata, [argv[0]], AS.Integer | AS.String
    )
    [mode] = utils.check_type(metadata, [argv[1]], AS.Integer)

    mode_str = parse.encode_number(mode.value)
    try:
        _mode = _MODE_TABLE[mode_str]
    except KeyError:
        raise error.UnsuspectedHangeulValueError(
            metadata, f"{mode_str}은 기본 제공 함수 ㄱㄴ이 이해하는 파일 열기 방식이 아닙니다."
        ) from None

    def _fn(do_IO: DoIO) -> AS.EvalContext:
        del do_IO  # Unused
        try:
            if (path_or_fd.value, _mode) == (0, "rb"):
                return File(sys.stdin.buffer)
            if (path_or_fd.value, _mode) == (1, "wb"):
                return File(sys.stdout.buffer)
            if (path_or_fd.value, _mode) == (2, "wb"):
                return File(sys.stderr.buffer)
            return File(open(path_or_fd.value, _mode))
        except OSError as err:
            raise error.UnsuspectedHangeulOSError(
                metadata, f"운영체제 오류 errno={err.errno}", err.errno
            ) from err
        yield

    return AS.IO("ㄱㄴ", (path_or_fd, mode), _fn)


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _bind(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> EvalIOContext:
        utils.check_arity(metadata, argv, [2, 3])
        [io_to_bind] = yield from utils.match_arguments(
            metadata, [argv[0]], AS.IO
        )
        resolve = yield from utils.strict_functional(metadata, argv[1])
        reject = AS.Nil()
        if len(argv) == 3:
            reject = yield from utils.strict_functional(metadata, argv[2])

        def _fn(do_IO: DoIO) -> AS.EvalContext:
            try:
                arg = yield from do_IO(io_to_bind)
            except AS.UnsuspectedHangeulError as err:
                if isinstance(reject, AS.Nil):
                    raise err
                result = yield from proc_functional(metadata, reject)(
                    metadata, [err.err]
                )
                result = yield result
                utils.check_type(metadata, [result], AS.IO)
                return result

            result = yield from proc_functional(metadata, resolve)(
                metadata, [arg]
            )
            result = yield result
            utils.check_type(metadata, [result], AS.IO)
            return result

        return AS.IO("ㄱㄹ", tuple(argv), _fn)

    return {
        "ㄹ": _input,  # 입력
        "ㅈㄹ": _print,  # 출력
        "ㄱㅅ": _return,  # 감싸다
        "ㄱㄹ": _bind,  # ~기로 하다
        "ㄱㄴ": _file,  # 꺼내다
    }
