"""평범한 한글 디버그 도구."""
import dataclasses
import sys
from typing import Callable, Literal

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import interpret
from pbhhg_py import main
from pbhhg_py import parse

_HELP = """평범한 한글 디버그 도구 사용법 안내

이 도구는 평범한 한글 프로그램의 실행 흐름을 따라가며 동작을 점검할 수 있는 상호작용형 디버그 도구입니다.

디버그 도구 명령
    계속(ㄱ): 다음 멈춤점에 도달하거나 오류 발생 또는 종료 때까지 실행을 계속합니다.

    넘어가기(ㄴ): 현재 객체의 평가 흐름으로 들어가는 대신 다른 객체의 평가로 넘어갑니다.

    들어가기(ㄷ): 현재 객체의 평가 흐름으로 들어갑니다.

    [줄 번호(숫자)] 멈추기(ㅁ): 지정한 줄 번호에 멈춤점을 둡니다. 줄 번호를 지정하지 않는 경우 현재 줄에 멈춤점을 둡니다.

    반환(ㅂ): 현재 객체의 결과값을 반환합니다.

    상승(ㅅ): 상위 객체로 돌아갑니다.

    안내(ㅇ): 본 안내문을 출력합니다.

    종료(ㅈ): 디버그 도구를 종료합니다.

    [줄 번호(숫자)] 치우기(ㅊ): 지정한 줄 번호에 둔 멈춤점을 치웁니다. 줄 번호를 지정하지 않는 경우 모든 멈춤점을 치웁니다.

    [평범한 한글 표현식, ...] 평가(ㅍ): 현재 문맥에서 지정한 표현식들을 평가합니다.
"""

_CommandType = Literal[
    "break",
    "clear",
    "continue",
    # "down",
    "help",
    "next",
    "print",
    "quit",
    "return",
    "step",
    "up",
]
_DEBUG_COMMANDS_KO: dict[str, _CommandType] = {
    "ㄱ": "continue",
    "계속": "continue",
    "ㄴ": "next",
    "넘어가기": "next",
    "ㄷ": "step",
    "들어가기": "step",
    "ㅁ": "break",
    "멈추기": "break",
    "ㅂ": "return",
    "반환": "return",
    "ㅅ": "up",
    "상승": "up",
    "ㅇ": "help",
    "안내": "help",
    "ㅈ": "quit",
    "종료": "quit",
    "ㅊ": "clear",
    "치우기": "clear",
    "ㅍ": "print",
    "평가": "print",
    # "ㅎ": "down",
    # "하강": "down",
}
_DEBUG_COMMANDS_EN: dict[str, _CommandType] = {
    "b": "break",
    "cl": "clear",
    "c": "continue",
    "cont": "continue",
    # "d": "down",
    "h": "help",
    "n": "next",
    "p": "print",
    "q": "quit",
    "r": "return",
    "s": "step",
    "u": "up",
}


def _parse_debug_command(
    command: str,
) -> tuple[_CommandType, list[str]] | None:
    args = command.strip().split(" ")
    if not args:
        return ("print", [])
    if args[-1] in _DEBUG_COMMANDS_KO.keys():
        return (_DEBUG_COMMANDS_KO[args[-1]], args[:-1])
    if args[0] in _DEBUG_COMMANDS_EN.keys():
        return (_DEBUG_COMMANDS_EN[args[0]], args[1:])
    if args[0] in _DEBUG_COMMANDS_EN.values():
        return (args[0], args[1:])
    return ("print", args)


@dataclasses.dataclass
class _DebugState:
    breakpoints: set[int] = dataclasses.field(default_factory=set)
    last_command: tuple[_CommandType, list[str]] | None = None


_StopCondition = Callable[[Literal["before", "after"], int], bool]


def _stop_always(
    when: Literal["before", "after"],
    depth_now: int,
) -> bool:
    del when, depth_now  # Unused
    return True


def _stop_never(
    when: Literal["before", "after"],
    depth_now: int,
) -> bool:
    del when, depth_now  # Unused
    return False


def _interact(
    state: _DebugState,
    depth: int,
    expr: AS.Expr,
) -> _StopCondition:
    while True:
        print(
            f"# {expr.expr.metadata.filename}:{expr.expr.metadata.line_no+1}"
            f":{expr.expr.metadata.start_col+1}~{expr.expr.metadata.end_col+1}"
        )
        print(str(expr.expr.metadata))

        line = input("> ")
        parsed_command = _parse_debug_command(line)
        if parsed_command is None:
            if state.last_command is None:
                continue
            cmd, args = state.last_command
        else:
            cmd, args = parsed_command

        if cmd == "break":
            if len(args) > 1:
                print("'멈추기'의 인수가 너무 많습니다.")
                continue
            point = int(args[0]) - 1 if args else expr.expr.metadata.line_no
            state.breakpoints.add(point)
            continue

        if cmd == "clear":
            if len(args) > 1:
                print("'치우기'의 인수가 너무 많습니다.")
                continue
            if not args:
                answer = input("멈춤점을 모두 치울까요? (예/아니오):")
                if answer == "예":
                    state.breakpoints = set()
            else:
                point = int(args[0]) - 1
                state.breakpoints.remove(point)
            continue

        if cmd == "continue":
            if len(args) > 0:
                print("'계속'의 인수가 너무 많습니다.")
                continue
            return _stop_never

        if cmd == "help":
            if len(args) > 0:
                print("'안내'의 인수가 너무 많습니다.")
                continue
            print(_HELP)
            continue

        if cmd == "next":
            if len(args) > 0:
                print("'넘어가기'의 인수가 너무 많습니다.")
                continue

            def _condition(
                when: Literal["before", "after"],
                depth_now: int,
            ) -> bool:
                return when == "before" and (depth_now <= depth)

            return _condition

        if cmd == "print":
            try:
                exprs = parse.parse("<debug>", " ".join(args))
                values = [AS.Expr(e, expr.env) for e in exprs]
                formatted = [
                    interpret.evaluate(main.formatter(value))
                    for value in values
                ]
                print(*formatted)
            except Exception as err:
                print("Error:", err)
            continue

        if cmd == "quit":
            if len(args) > 0:
                print("'종료'의 인수가 너무 많습니다.")
                continue
            sys.exit(0)

        if cmd == "return":
            if len(args) > 0:
                print("'반환'의 인수가 너무 많습니다.")
                continue

            def _condition(
                when: Literal["before", "after"],
                depth_now: int,
            ) -> bool:
                return when == "after" and (depth_now <= depth)

            return _condition

        if cmd == "step":
            if len(args) > 0:
                print("'다음'의 인수가 너무 많습니다.")
                continue

            def _condition(
                when: Literal["before", "after"],
                depth_now: int,
            ) -> bool:
                del depth_now  # unused
                return when == "before"

            return _condition

        if cmd == "up":
            if len(args) > 0:
                print("'상승'의 인수가 너무 많습니다.")
                continue

            def _condition(
                when: Literal["before", "after"],
                depth_now: int,
            ) -> bool:
                return when == "before" and (depth_now < depth)

            return _condition


class Debugger(interpret.DebuggerBase):
    def __init__(self):
        print(f"[평범한 한글 디버거. 사용법을 보려면 '안내'라고 입력하세요.]")
        self._state = _DebugState()
        self._stop_condition: _StopCondition = _stop_always

    def before_eval(self, depth: int, expr: AS.Expr) -> None:
        if expr.expr.metadata.line_no in self._state.breakpoints:
            self._stop_condition = _interact(self._state, depth, expr)
        elif self._stop_condition("before", depth):
            self._stop_condition = _interact(self._state, depth, expr)

    def after_eval(
        self,
        depth: int,
        expr: AS.Expr,
        result: AS.StrictValue | AS.UnsuspectedHangeulError,
    ) -> None:
        if isinstance(result, AS.UnsuspectedHangeulError):
            print(str(result), file=sys.stderr)
            self._stop_condition = _interact(self._state, depth, expr)
        elif self._stop_condition("after", depth):
            formatted = interpret.evaluate(main.formatter(result))
            print(f"Returned with value {formatted}")
            self._stop_condition = _interact(self._state, depth, expr)
