from __future__ import annotations

import abc
from math import isclose
from math import isfinite
import typing
from typing import NamedTuple


# AST
class Literal(NamedTuple):
    value: int


class FunRef(NamedTuple):
    rel: int


class ArgRef(NamedTuple):
    relA: AST
    relF: int


class FunDef(NamedTuple):
    body: AST


class FunCall(NamedTuple):
    fun: AST
    argv: tuple[AST, ...]


AST = Literal | FunRef | ArgRef | FunDef | FunCall


# Env
class Env(NamedTuple):
    funs: list[Closure]
    args: list[tuple[Value, ...]]

    def __hash__(self) -> int:
        return hash((tuple(self.funs), tuple(self.args)))


# Exception
class UnsuspectedHangeulError(Exception):
    def __init__(self, message: str, argv: typing.Sequence[StrictValue]):
        super().__init__(message)
        self.argv = tuple(argv)  # Exposed to user code


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


class Nil(NamedTuple):
    pass


def _to_int_if_possible(num: float) -> int | float:
    if isfinite(num) and isclose(num, int(num), abs_tol=1e-16):
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


class BuiltinFunction(NamedTuple):
    literal: Literal


class Function(abc.ABC):
    def __init__(self, adj: str = ""):
        self._str = "<{}Function>".format(adj)

    def __hash__(self):
        return id(self)

    def __str__(self):
        return self._str

    @abc.abstractmethod
    def __call__(self, argv: typing.Sequence[Value]) -> EvalContext:
        raise NotImplementedError


class Closure(Function):
    def __init__(self, body: AST, env: Env):
        self.body = body
        self.env = env
        self._str = "<Closure created at depth {}>".format(len(env.args))

    def __call__(self, argv: typing.Sequence[Value]) -> EvalContext:
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
        return hash((self.expr, self.env))


# Collection
Real = Integer | Float
Number = Real | Complex
Sequence = List | String | Bytes
Callable = Function | Boolean | Sequence | Dict | Complex

NonIOStrictValue = Number | Callable | Nil
StrictValue = NonIOStrictValue | IO
Value = StrictValue | Expr


EvalContext = typing.Generator[
    Value,
    StrictValue,
    Value,
]
Evaluation = typing.Callable[[typing.Sequence[Value]], EvalContext]
