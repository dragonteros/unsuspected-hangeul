"""
함수형 난해한 언어 '평범한 한글'의 구현체입니다.

Updates
* v0.7 (2020.03.08)
  * 복소수가 추가되고 정수가 실수에서 분리되었습니다.
  * 기본 제공 함수로 정수 나눗셈과 나머지 연산이 추가되었습니다. 거듭제곱 연산은 모듈로 거듭제곱을 지원하도록 확장되었습니다.
  * 인수 접근 및 목록, 문자열 등의 인덱싱 행동이 실수를 반올림하는 것에서 정수를 사용하는 것으로 일괄 변경되었습니다.
    - 주의: v0.6의 행동과 호환되지 않습니다.
  * 수학 모듈과 비트 연산 모듈이 추가되었습니다.
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
