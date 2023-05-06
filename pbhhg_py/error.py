from typing import Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import parse


class UnsuspectedHangeulCustomError(AS.UnsuspectedHangeulError):
    def __init__(self, argv: Sequence[AS.StrictValue]):
        message = f"사용자 예외: {','.join(str(arg) for arg in argv)}"
        super().__init__(message, argv)


class UnsuspectedHangeulBuiltinError(AS.UnsuspectedHangeulError):
    def __init__(self, message: str, codes: Sequence[int]):
        codes = [parse.parse_number("ㅂ"), *codes]
        super().__init__(message, [AS.Integer(code) for code in codes])


class UnsuspectedHangeulOSError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str, errno: int):
        code = parse.parse_number("ㅈㅈ")  # 체제
        super().__init__(message, [code, errno])


class UnsuspectedHangeulArithmeticError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㅅㅅ")  # 산술
        super().__init__(message, [code])


class UnsuspectedHangeulTypeError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㄱ")  # 꼴
        super().__init__(message, [code])


class UnsuspectedHangeulValueError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㅈㅁ")  # 잘못
        super().__init__(message, [code])


class UnsuspectedHangeulDivisionError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㄴㄴ")  # 나눔
        super().__init__(message, [code])


class UnsuspectedHangeulNotFoundError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㅁㅈ")  # 못찾
        super().__init__(message, [code])


class UnsuspectedHangeulImportError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㅂ")  # 불러오기
        super().__init__(message, [code])


class UnsuspectedHangeulOutOfRangeError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㅂㄱ")  # 바깥
        super().__init__(message, [code])


class UnsuspectedHangeulKeyboardInterruptError(UnsuspectedHangeulBuiltinError):
    def __init__(self, message: str):
        code = parse.parse_number("ㅈㄷ")  # 중단
        super().__init__(message, [code])
