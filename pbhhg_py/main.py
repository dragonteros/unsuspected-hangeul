"""
함수형 난해한 언어 '평범한 한글'의 구현체입니다.

Updates
-------
v0.8 (2023.07.16)
- 예외가 추가되었습니다. 이제 객체는 정수, 실수, 복소수, 논릿값, 문자열, 바이트열, 목록, 사전, 함수, 드나듦, 빈값, 예외의 열두 종류입니다.
- 예외 처리용 기본 제공 함수 `ㄷㅈ`과 `ㅅㄷ`이 추가되었습니다.
- 기본 제공 함수 `ㄱㄹ`가 예외 처리 함수를 인수로 받도록 변경되었습니다.
  - 주의: v0.7의 행동과 호환되지 않습니다.
- 오류 발생 시 출력 형식을 개선했습니다. 이제 오류 내용에 더해 오류가 발생한 지점도 함께 알립니다.
- 파일 접근 기본 제공 함수 `ㄱㄴ`이 추가되었습니다.
- 기본 제공 함수 `ㄹ`이 파일 끝을 마주하면 빈값을 내놓도록 변경되었습니다.
- 기본 제공 함수 `ㄱ`과 `ㄷ`이 논릿값 인수를 받은 경우 첫번째 인수부터 차례로 단락 평가(short-circuit evaluation)를 하도록 변경되었습니다.
- 기본 제공 함수 `ㅁㅂ`, `ㅈㄷ`에 예외 지원을 추가했습니다.
- 기본 제공 모듈 `ㅂ ㅂ`에 UTF-32 지원이 추가되었습니다.
- 기본 제공 함수 `ㅂㄹ`과 `ㄱㅁ`에 바이트열 지원을 추가하였습니다.
- 알려진 문제: 일부 구문에서 느긋한 평가로 인해 예외 처리가 안되는 현상이 있습니다.
  - 예: `(ㄱ ㄴㄱ ㅅㅎㄷ) [ㄱㅇㄴㅎ] ㅎㅎㄴ [ㄱㅎ] ㅅㄷㅎㄷ`
"""
import functools
from typing import Generator

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import interpret
from pbhhg_py import parse
from pbhhg_py import utils


def do_IO(
    value: AS.StrictValue,
) -> Generator[AS.Value, AS.StrictValue, AS.NonIOStrictValue]:
    """Receives an IO and produces non-IO non-Expr value."""
    while isinstance(value, AS.IO):
        expr = yield from value.continuation(do_IO)
        value = yield expr
    return value


def formatter(
    value: AS.Value, format_io: bool = True
) -> Generator[AS.Value, AS.StrictValue, str]:
    """Converts the value into Python number, bool and str for writing tests"""
    value = yield value
    if isinstance(value, AS.IO):
        _format = "IO({})" if format_io else "{}"
        arg = yield from do_IO(value)
        arg = yield from formatter(arg)
        return _format.format(arg)
    _formatter = functools.partial(formatter, format_io=format_io)

    if isinstance(value, AS.List):
        arg = yield from utils.map_strict_with_hook(value.value, _formatter)
        return f"[{', '.join(arg)}]"

    if isinstance(value, AS.Dict):
        keys = [k for k, _, _ in value.table]
        keys = yield from utils.map_strict_with_hook(keys, _formatter)
        values = [v for _, _, v in value.table]
        values = yield from utils.map_strict_with_hook(values, _formatter)
        pairs = list(zip(keys, values))
        pairs.sort(key=lambda pair: pair[0])
        formatted = ", ".join(f"{k}: {v}" for k, v in pairs)
        return "{" + formatted + "}"

    if isinstance(value, AS.ErrorValue):
        arg = yield from utils.map_strict_with_hook(value.value, _formatter)
        return f"<예외: [{(', '.join(arg))}]>"

    return (yield from value.format())


def main(filename: str, program: str, format_io: bool = True) -> list[str]:
    """Main procedure. Parses, evaluates, and converts to str.

    Args:
        filename: File name of the program.
        arg: Raw string that encodes the program.
        format_io: Whether to format IOs in the form `IO(.)`

    Returns:
        A list of strings representing the resulting values
    """
    exprs = parse.parse(filename, program)
    env = AS.Env([], [])
    values = [AS.Expr(expr, env) for expr in exprs]
    formatters = [formatter(value, format_io) for value in values]
    return [interpret.evaluate(f) for f in formatters]
