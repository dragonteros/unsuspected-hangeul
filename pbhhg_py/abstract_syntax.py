from __future__ import annotations

import abc
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
class Integer(NamedTuple):
    value: int


class Float(NamedTuple):
    value: float


class Boolean(NamedTuple):
    value: bool

    def __hash__(self) -> int:
        return hash(("평범한 한글/참거짓", self.value))


class List(NamedTuple):
    value: tuple[Value, ...]

    def __hash__(self) -> int:
        return hash(("평범한 한글/목록", self.value))


class String(NamedTuple):
    value: str

    def __hash__(self) -> int:
        return hash(("평범한 한글/문자열", self.value))


class Bytes(NamedTuple):
    value: bytes

    def __hash__(self) -> int:
        return hash(("평범한 한글/바이트열", self.value))


class ErrorValue(NamedTuple):
    metadatas: tuple[Metadata, ...]
    message: str
    value: tuple[StrictValue, ...]

    def __hash__(self) -> int:
        return hash(("평범한 한글/예외", self.metadatas, self.value))


class Nil(NamedTuple):
    pass


def _to_int_if_possible(num: float) -> int | float:
    if math.isfinite(num) and math.isclose(num, int(num), abs_tol=1e-16):
        return int(num)
    return num


class Complex(NamedTuple):
    value: complex

    def __str__(self):
        re = _to_int_if_possible(self.value.real)
        im = _to_int_if_possible(self.value.imag)
        re_str = str(re) + ("" if im < 0 else "+")
        minus_str = "-" if im < 0 else ""
        im_str = "" if abs(im) == 1 else str(abs(im))
        return "{}{}{}i".format(re_str if re else "", minus_str, im_str)


class Dict(NamedTuple):
    value: typing.Mapping[StrictValue, Value]

    def __hash__(self):
        return hash(("평범한 한글/사전", tuple(self.value.items())))


class IO:
    def __init__(
        self,
        inst: str,
        argv: typing.Sequence[StrictValue | BuiltinFunction],
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
        self._hash = hash(("평범한 한글/드나듦", inst, tuple(argv)))
        self.continuation = continuation

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)


class BuiltinFunction(NamedTuple):  # Is not a value
    literal: Literal


class Function(abc.ABC):
    def __init__(self, adj: str = ""):
        self._str = "<{}Function>".format(adj)

    def __hash__(self):
        return id(self)

    def __str__(self):
        return self._str

    @abc.abstractmethod
    def __call__(
        self, metadata: Metadata, argv: typing.Sequence[Value]
    ) -> EvalContext:
        raise NotImplementedError


class Closure(Function):
    def __init__(self, body: AST, env: Env):
        self.body = body
        self.env = env
        self._str = "<Closure created at depth {}>".format(len(env.args))

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

    def __hash__(self):
        return hash((self.expr, id(self.env)))


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
