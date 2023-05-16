from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import parse


class UnsuspectedHangeulBuiltinError(AS.UnsuspectedHangeulError):
    def __init__(
        self, metadata: AS.Metadata, message: str, codes: Sequence[int]
    ):
        _codes = [parse.parse_number("ㅂ"), *codes]
        argv = [AS.Integer(code) for code in _codes]
        err = AS.ErrorValue((metadata,), message, tuple(argv))
        super().__init__(err)


class UnsuspectedHangeulOSError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str, errno: int):
        code = parse.parse_number("ㅈㅈ")  # 체제
        super().__init__(metadata, message, [code, errno])


class UnsuspectedHangeulArithmeticError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㅅㅅ")  # 산술
        super().__init__(metadata, message, [code])


class UnsuspectedHangeulTypeError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㄱ")  # 꼴
        super().__init__(metadata, message, [code])


class UnsuspectedHangeulValueError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㅈㅁ")  # 잘못
        super().__init__(metadata, message, [code])


class UnsuspectedHangeulDivisionError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㄴㄴ")  # 나누기
        super().__init__(metadata, message, [code])


class UnsuspectedHangeulNotFoundError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㅁㅈ")  # 못찾
        super().__init__(metadata, message, [code])


class UnsuspectedHangeulImportError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㅂ")  # 불러오기
        super().__init__(metadata, message, [code])


class UnsuspectedHangeulOutOfRangeError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㅂㄱ")  # 바깥
        super().__init__(metadata, message, [code])


class UnsuspectedHangeulKeyboardInterruptError(UnsuspectedHangeulBuiltinError):
    def __init__(self, metadata: AS.Metadata, message: str):
        code = parse.parse_number("ㅈㄷ")  # 중단
        super().__init__(metadata, message, [code])
