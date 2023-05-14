"""함수형 난해한 언어 '평범한 한글'의 명령행 인터페이스입니다."""
import argparse
import os
import sys

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import debugger
from pbhhg_py import interpret
from pbhhg_py import main
from pbhhg_py import parse
from pbhhg_py import utils


def run(
    filename: str, program: str, argv: list[str], debug: bool = False
) -> int:
    """Runs the outermost function with command-line arguments.

    If the program is not a function, just returns the value.
    In either case, the value is interpreted as the return code.

    Args:
        filename: File name of the program.
        program: Raw string that encodes the program.
        argv: Command-line arguments.

    Returns:
        An integer representing the return code.
        IO value is treated with its underlying value.
        Nil value is treated as return code of 0.
        No other types of return values are allowed.
    """
    cli_metadata = AS.Metadata("<main>", 0, 0, 0, "")
    arguments = [AS.String(arg) for arg in argv]
    _debugger = debugger.Debugger() if debug else None

    exprs = parse.parse(filename, program)
    if not exprs:
        return 0
    if len(exprs) > 1:
        err = AS.ErrorValue(
            tuple(expr.metadata for expr in exprs),
            f"모듈에는 하나의 표현식만 있어야 하는데 {len(exprs)}개의 표현식이 있습니다.",
            (),
        )
        raise AS.UnsuspectedHangeulError(err)
    env = AS.Env([], [])
    value = AS.Expr(exprs[0], env)
    strict = interpret.evaluate(
        interpret.strict(value), debugger=_debugger
    )  # No builtin function

    if isinstance(strict, AS.Function):
        value = interpret.evaluate(
            interpret.proc_functional(cli_metadata, strict)(
                cli_metadata, arguments
            ),
            debugger=_debugger,
        )
        strict = interpret.evaluate(
            interpret.strict(value), debugger=_debugger
        )

    if isinstance(strict, AS.IO):
        strict = interpret.evaluate(main.do_IO(strict), debugger=_debugger)

    [strict] = utils.check_type(cli_metadata, [strict], AS.Integer | AS.Nil)
    if isinstance(strict, AS.Nil):
        return 0
    return strict.value


def _print_main(filename: str, arg: str, warn_multiple: bool = True):
    values = main.main(filename, arg)
    if warn_multiple and len(values) >= 2:
        print(
            "[!] 주의: 한 줄에 {}개의 객체를 해석했습니다.".format(len(values)),
            file=sys.stderr,
        )
    print(" ".join(values), flush=True)


def _get_quit_instruction() -> str:
    if os.name == "nt":
        return "Ctrl-Z를 누른 다음 Enter"
    elif os.name == "posix":
        return "Ctrl-D"
    else:
        return "Ctrl-C"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="난해한 프로그래밍 언어 '평범한 한글'의 해석기입니다.",
    )
    parser.add_argument(
        "-d", "--debug", help="디버그 모드 켜기.", action="store_true"
    )
    parser.add_argument(
        "-c", "--command", nargs="?", help="실행하고자 하는 '평범한 한글' 프로그램 본문."
    )

    parser.add_argument(
        "rest",
        nargs=argparse.REMAINDER,
        help="meow.",
    )

    args = parser.parse_args()

    filepath: str = ""
    arguments: list[str] = []
    if args.command:
        arguments = args.rest
    elif args.rest:
        filepath, *arguments = args.rest

    if filepath:
        fd: str | int = filepath
        if filepath == "-":
            fd = 0
        with open(fd, "r", encoding="utf-8") as file:
            exit_code = run(filepath, file.read(), arguments, debug=args.debug)
            sys.exit(exit_code)

    elif args.command:
        exit_code = run("<command>", args.command, arguments, debug=args.debug)
        sys.exit(exit_code)

    else:  # interactive
        quit_key = _get_quit_instruction()
        print(f"[평범한 한글 해석기. 종료하려면 {quit_key}를 누르세요.]")
        print("> ", end="", flush=True)
        for line in sys.stdin:
            _print_main("<stdin>", line)
            print("> ", end="", flush=True)
