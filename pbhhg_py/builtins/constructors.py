from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error
from pbhhg_py import utils


def _parse_str_to_number(argv: Sequence[AS.StrictValue]):
    argv = utils.match_defaults(argv, 2, [AS.Integer(10)])
    string, base = argv
    [string] = utils.check_type([string], AS.String)
    [base] = utils.check_type([base], AS.Integer)
    return string.value, base.value


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    del proc_functional  # Unused

    def _dict(argv: Sequence[AS.Value]) -> AS.EvalContext:
        if len(argv) % 2 == 1:
            raise error.UnsuspectedHangeulValueError(
                f"ㅅㅈ 함수는 짝수 개의 인수를 받지만 {len(argv)}개의 인수가 들어왔습니다."
            )
        keys, values = argv[0::2], argv[1::2]
        keys = yield from utils.map_strict_with_hook(
            keys, utils.recursive_strict
        )
        return AS.Dict({k: v for k, v in zip(keys, values)})

    def _list(argv: Sequence[AS.Value]) -> AS.EvalContext:
        return AS.List(tuple(argv))
        yield

    def _string(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            argv, AS.Number | AS.String, [0, 1]
        )
        if len(argv) == 0:
            return AS.String("")
        if utils.is_type(argv, AS.Real):
            return AS.String(str(argv[0].value))
        elif utils.is_type(argv, AS.Complex):
            return AS.String(str(argv[0]))
        return argv[0]

    def _integer(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            argv, AS.Real | AS.String, [1, 2]
        )
        if utils.is_type([argv[0]], AS.Real):
            utils.check_arity(argv, 1)
            return AS.Integer(int(argv[0].value))

        string, base = _parse_str_to_number(argv)
        return AS.Integer(int(string, base))

    def _float(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            argv, AS.Real | AS.String, [1, 2]
        )
        if utils.is_type([argv[0]], AS.Real):
            utils.check_arity(argv, 1)
            return AS.Float(float(argv[0].value))

        string, base = _parse_str_to_number(argv)
        if base == 10:
            return AS.Float(float(string))
        integer, frac = (string.strip().split(".") + [""])[:2]
        significant = int(integer + frac, base=base)
        return AS.Float(significant / base ** len(frac))

    def _complex(argv: Sequence[AS.Value]) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            argv, AS.Number | AS.String, [1, 2]
        )
        if utils.is_type(argv, AS.Number):
            real, imag = utils.match_defaults(argv, 2, [AS.Float(0.0)])
            return AS.Complex(complex(real.value, imag.value))

        argv = utils.check_type(argv, AS.String)
        utils.check_arity(argv, 1)
        arg = argv[0].value.replace("i", "j")
        return AS.Complex(complex(arg))

    def _nil(argv: Sequence[AS.Value]) -> AS.EvalContext:
        utils.check_arity(argv, 0)
        return AS.Nil()
        yield

    return {
        "ㅅㅈ": _dict,  # 사전
        "ㅁㄹ": _list,  # 목록
        "ㅁㅈ": _string,  # 문자열
        "ㅈㅅ": _integer,  # 정수
        "ㅅㅅ": _float,  # 실수
        "ㅂㅅ": _complex,  # 복소수
        "ㅂㄱ": _nil,  # 빈값
    }
