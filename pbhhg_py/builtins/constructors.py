from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error
from pbhhg_py import utils


def _parse_str_to_number(
    metadata: AS.Metadata, argv: Sequence[AS.StrictValue]
):
    argv = utils.match_defaults(metadata, argv, 2, [AS.Integer(10)])
    string, base = argv
    [string] = utils.check_type(metadata, [string], AS.String)
    [base] = utils.check_type(metadata, [base], AS.Integer)
    return string.value, base.value


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    del proc_functional  # Unused

    def _dict(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        if len(argv) % 2 == 1:
            raise error.UnsuspectedHangeulValueError(
                metadata, f"ㅅㅈ 함수에는 인수를 짝수 개로 주어야 하는데 {len(argv)}개를 주었습니다."
            )
        keys, values = argv[0::2], argv[1::2]
        keys = yield from utils.map_strict_with_hook(
            keys, utils.recursive_strict
        )
        return AS.Dict({k: v for k, v in zip(keys, values)})

    def _list(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        del metadata  # Unused
        return AS.List(tuple(argv))
        yield

    def _string(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            metadata, argv, AS.Number | AS.String, [0, 1]
        )
        if len(argv) == 0:
            return AS.String("")
        if utils.is_type(argv, AS.Real):
            return AS.String(str(argv[0].value))
        elif utils.is_type(argv, AS.Complex):
            return AS.String(str(argv[0]))
        return argv[0]

    def _integer(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            metadata, argv, AS.Real | AS.String, [1, 2]
        )
        if utils.is_type([argv[0]], AS.Real):
            utils.check_arity(metadata, argv, 1)
            return AS.Integer(int(argv[0].value))

        string, base = _parse_str_to_number(metadata, argv)
        try:
            return AS.Integer(int(string, base))
        except ValueError:
            raise error.UnsuspectedHangeulValueError(
                metadata, f"다음 문자열을 정수값으로 변환할 수 없습니다.: '{string}'"
            ) from None

    def _float(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            metadata, argv, AS.Real | AS.String, [1, 2]
        )
        if utils.is_type([argv[0]], AS.Real):
            utils.check_arity(metadata, argv, 1)
            return AS.Float(float(argv[0].value))

        string, base = _parse_str_to_number(metadata, argv)
        if base == 10:
            try:
                return AS.Float(float(string))
            except ValueError:
                raise error.UnsuspectedHangeulValueError(
                    metadata, f"다음 문자열을 실수값으로 변환할 수 없습니다: '{string}'"
                ) from None
        integer, frac = utils.match_defaults(
            metadata, string.strip().split("."), 2, [""]
        )
        try:
            significant = int(integer + frac, base=base)
        except ValueError:
            raise error.UnsuspectedHangeulValueError(
                metadata, f"다음 문자열을 실수값으로 변환할 수 없습니다: '{string}'"
            ) from None
        return AS.Float(significant / base ** len(frac))

    def _complex(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.match_arguments(
            metadata, argv, AS.Number | AS.String, [1, 2]
        )
        if utils.is_type(argv, AS.Number):
            real, imag = utils.match_defaults(
                metadata, argv, 2, [AS.Float(0.0)]
            )
            return AS.Complex(complex(real.value, imag.value))

        argv = utils.check_type(metadata, argv, AS.String)
        utils.check_arity(metadata, argv, 1)
        arg = argv[0].value.replace("i", "j")
        try:
            return AS.Complex(complex(arg))
        except ValueError:
            raise error.UnsuspectedHangeulValueError(
                metadata, f"다음 문자열을 복소수값으로 변환할 수 없습니다: '{arg}'"
            ) from None

    def _nil(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_arity(metadata, argv, 0)
        return AS.Nil()
        yield

    def _exception(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        argv = yield from utils.map_strict(argv)
        message = f'사용자 예외: {", ".join(map(str, argv))}'
        return AS.ErrorValue((metadata,), message, tuple(argv))
        yield

    return {
        "ㄷㅂ": _exception,  # 뜻밖
        "ㅁㄹ": _list,  # 목록
        "ㅁㅈ": _string,  # 문자열
        "ㅂㄱ": _nil,  # 빈값
        "ㅂㅅ": _complex,  # 복소수
        "ㅅㅅ": _float,  # 실수
        "ㅅㅈ": _dict,  # 사전
        "ㅈㅅ": _integer,  # 정수
    }
