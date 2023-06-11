from __future__ import annotations

import abc
import dataclasses
import math
import typing
from typing import NamedTuple
import unicodedata


def _get_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "FW" else 1 for c in s)


class Metadata(NamedTuple):
    filename: str
    line_no: int
    start_col: int
    end_col: int
    line: str  # whole line

    def __str__(self) -> str:
        return (
            self.line
            + "\n"
            + " " * _get_width(self.line[: self.start_col])
            + "^" * _get_width(self.line[self.start_col : self.end_col])
        )


# AST
class Literal(NamedTuple):
    value: int
    metadata: Metadata


class FunRef(NamedTuple):
    rel: int
    metadata: Metadata


class ArgRef(NamedTuple):
    relA: AST
    relF: int
    metadata: Metadata


class FunDef(NamedTuple):
    body: AST
    metadata: Metadata


class FunCall(NamedTuple):
    fun: AST
    argv: tuple[AST, ...]
    metadata: Metadata


AST = Literal | FunRef | ArgRef | FunDef | FunCall


# Env
class Env(NamedTuple):
    funs: list[Closure]
    args: list[tuple[Value, ...]]


# Exception
class UnsuspectedHangeulError(Exception):
    def __init__(
        self,
        err: ErrorValue,
    ):
        message = ""
        for metadata in err.metadatas:
            message += (
                f"{metadata.filename} {metadata.line_no+1}번줄 "
                f"{metadata.start_col + 1}~{metadata.end_col+1}번째 글자:\n"
                f"{str(metadata)}\n"
            )
        super().__init__(f"{message}\n{err.message}")
        self.err = err  # Exposed to user code


# Values
@dataclasses.dataclass
class Integer:
    value: int

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Number) and self.value == other.value

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(self.value)
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return str(self.value)
        yield


@dataclasses.dataclass
class Float:
    value: float

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Number) and self.value == other.value

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(self.value)
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return str(self.value)
        yield


@dataclasses.dataclass
class Boolean:
    value: bool

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(("평범한 한글/참거짓", self.value))
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return str(self.value)
        yield


@dataclasses.dataclass
class List:
    value: tuple[Value, ...]
    _key: int | None = dataclasses.field(
        default=None, init=False, compare=False
    )
    _format: str | None = dataclasses.field(
        default=None, init=False, compare=False
    )

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        if self._key is None:
            keys: list[int] = []
            for item in self.value:
                item = yield item
                keys.append((yield from item.as_key()))
            self._key = hash(("평범한 한글/목록", tuple(keys)))
        return self._key

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        if self._format is None:
            formatted: list[str] = []
            for item in self.value:
                item = yield item
                formatted.append((yield from item.format()))
            self._format = "[" + ", ".join(formatted) + "]"
        return self._format


@dataclasses.dataclass
class String:
    value: str

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(("평범한 한글/문자열", self.value))
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return f"'{self.value}'"
        yield


@dataclasses.dataclass
class Bytes:
    value: bytes
    _format: str | None = dataclasses.field(
        default=None, init=False, compare=False
    )

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(("평범한 한글/바이트열", self.value))
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        if self._format is None:
            arg = "".join(rf"\x{b:02X}" for b in self.value)
            self._format = f"b'{arg}'"
        return self._format
        yield


@dataclasses.dataclass
class ErrorValue:
    metadatas: tuple[Metadata, ...]
    message: str
    value: tuple[StrictValue, ...]
    _key: int | None = dataclasses.field(
        default=None, init=False, compare=False
    )
    _format: str | None = dataclasses.field(
        default=None, init=False, compare=False
    )

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        if self._key is None:
            keys: list[int] = []
            for item in self.value:
                item = yield item
                keys.append((yield from item.as_key()))
            self._key = hash(("평범한 한글/예외", tuple(keys)))
        return self._key

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        if self._format is None:
            formatted: list[str] = []
            for item in self.value:
                item = yield item
                formatted.append((yield from item.format()))
            self._format = "<예외: [" + ", ".join(formatted) + "]>"
        return self._format


@dataclasses.dataclass
class Nil:
    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(("평범한 한글/빈값", None))
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return "Nil"
        yield


def _to_int_if_possible(num: float) -> int | float:
    if math.isfinite(num) and math.isclose(num, int(num), abs_tol=1e-16):
        return int(num)
    return num


@dataclasses.dataclass
class Complex:
    value: complex

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Number) and self.value == other.value

    def __str__(self):
        re = _to_int_if_possible(self.value.real)
        im = _to_int_if_possible(self.value.imag)
        re_str = str(re) + ("" if im < 0 else "+")
        minus_str = "-" if im < 0 else ""
        im_str = "" if abs(im) == 1 else str(abs(im))
        return "{}{}{}i".format(re_str if re else "", minus_str, im_str)

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(self.value)
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return str(self)
        yield


class Dict:
    def __init__(
        self,
        table: typing.Sequence[tuple[StrictValue, int, Value]],
    ):
        self.table = tuple(table)
        self.mapping = {k: v for _, k, v in table}
        self._key = None
        self._format = None

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        if self._key is None:
            keys: list[tuple[int, int]] = []
            for key, value in self.mapping.items():
                v = yield from (yield value).as_key()
                keys.append((key, v))
            self._key = hash(("평범한 한글/사전", frozenset(keys)))
        return self._key

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        if self._format is None:
            formatted: list[tuple[str, str]] = []
            for orig_key, key, value in self.table:
                del key  # Unused
                k = yield from (yield orig_key).format()
                v = yield from (yield value).format()
                formatted.append((k, v))
            formatted.sort(key=lambda pair: pair[0])
            self._format = (
                "{" + ", ".join(f"{k}: {v}" for k, v in formatted) + "}"
            )
        return self._format


class IO:
    def __init__(
        self,
        inst: str,
        argv: typing.Sequence[Value],
        continuation: typing.Callable[
            [
                typing.Callable[
                    [IO],
                    typing.Generator[Value, StrictValue, NonIOStrictValue],
                ]
            ],
            EvalContext,
        ],
    ):
        self._inst = inst
        self._argv = argv
        self.continuation = continuation
        self._key = None

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        if self._key is None:
            keys: list[int] = []
            for item in self._argv:
                item = yield item
                keys.append((yield from item.as_key()))
            self._key = hash(("평범한 한글/드나듦", self._inst, tuple(keys)))
        return self._key

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return f"<드나듦 {self._inst}>"
        yield


@dataclasses.dataclass
class BuiltinFunction:  # Is not a value
    literal: Literal


class Function(abc.ABC):
    def __init__(self, adj: str = ""):
        self._str = f"<{adj} 함수>"

    def as_key(self) -> typing.Generator[Value, StrictValue, int]:
        return hash(("평범한 한글/함수", id(self)))
        yield

    def format(self) -> typing.Generator[Value, StrictValue, str]:
        return self._str
        yield

    @abc.abstractmethod
    def __call__(
        self, metadata: Metadata, argv: typing.Sequence[Value]
    ) -> EvalContext:
        raise NotImplementedError


class Closure(Function):
    def __init__(self, body: AST, env: Env):
        self.body = body
        self.env = env
        super().__init__(f"깊이 {len(env.args)}에서 생성된")

    def __call__(
        self, metadata: Metadata, argv: typing.Sequence[Value]
    ) -> EvalContext:
        del metadata  # Unused
        canned_funs, canned_args = self.env
        new_env = Env(canned_funs, canned_args + [tuple(argv)])
        return Expr(self.body, new_env)
        yield


# Intermediate value
class CacheBox:
    def __init__(self):
        self._value: StrictValue | UnsuspectedHangeulError | None = None
        self.requestor: CacheBox | None = None

    @property
    def value(self):
        return self._value

    def resolve(self, value: StrictValue | UnsuspectedHangeulError):
        self._value = value
        if self.requestor:
            self.requestor.resolve(value)


class Expr:
    """Represents not yet evaluated value."""

    def __init__(self, expr: AST, env: Env):
        self.expr = expr
        self.env = env
        self.cache_box = CacheBox()


# Collection
Real = Integer | Float
Number = Real | Complex
Sequence = List | String | Bytes
Callable = Function | Boolean | Sequence | Dict | Complex | ErrorValue

NonIOStrictValue = Number | Callable | Nil
StrictValue = NonIOStrictValue | IO
Value = StrictValue | Expr

EvalContext = typing.Generator[
    Value,
    StrictValue,
    Value,
]
Evaluation = typing.Callable[[Metadata, typing.Sequence[Value]], EvalContext]
