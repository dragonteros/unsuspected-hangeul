"""Useful utilities for arguments."""
from __future__ import annotations

from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Mapping,
    Protocol,
    Sequence,
    TypeGuard,
    TypeVar,
)

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error

_T = TypeVar("_T")
_U = TypeVar("_U")

DeepDict = Mapping[_T, _U | "DeepDict[_T, _U]"]


class ProcFunctional(Protocol):
    def __call__(
        self,
        metadata: AS.Metadata,
        fun: AS.StrictValue | AS.BuiltinFunction,
        general_callable: bool = False,
    ) -> AS.Evaluation:
        ...


def strict_functional(
    metadata: AS.Metadata,
    fun: AS.Value,
) -> Generator[AS.Value, AS.StrictValue, AS.Callable | AS.BuiltinFunction]:
    if isinstance(fun, AS.Expr) and isinstance(fun.expr, AS.Literal):
        return AS.BuiltinFunction(fun.expr)

    fun = yield fun
    [fun] = check_type(metadata, [fun], AS.Callable)
    return fun


def map_strict(
    seq: Iterable[AS.Value],
) -> Generator[AS.Value, AS.StrictValue, list[AS.StrictValue]]:
    result: list[AS.StrictValue] = []
    for item in seq:
        result.append((yield item))
    return result


def map_strict_with_hook(
    seq: Iterable[AS.Value],
    generator: Callable[[AS.Value], Generator[AS.Value, AS.StrictValue, _T]],
) -> Generator[AS.Value, AS.StrictValue, list[_T]]:
    result: list[_T] = []
    for item in seq:
        result.append((yield from generator(item)))
    return result


def recursive_strict(
    item: AS.Value,
) -> Generator[AS.Value, AS.StrictValue, AS.StrictValue]:
    item = yield item
    if isinstance(item, AS.List):
        v = item.value
        v = yield from map_strict_with_hook(v, recursive_strict)
        return AS.List(tuple(v))
    elif isinstance(item, AS.Dict):
        if not item.value:
            return AS.Dict({})
        values = item.value.values()
        values = yield from map_strict_with_hook(values, recursive_strict)
        d = dict(zip(item.value.keys(), values))
        return AS.Dict(d)
    if isinstance(item, AS.ErrorValue):
        v = item.value
        v = yield from map_strict_with_hook(v, recursive_strict)
        return AS.ErrorValue(item.metadatas, item.message, tuple(v))
    return item


def all_equal(seq: Iterable[Any]) -> bool:
    """Checks if all elements in `seq` are equal."""
    seq = list(seq)
    return not seq or seq.count(seq[0]) == len(seq)


_ValueT = TypeVar("_ValueT", bound=AS.StrictValue)


def is_type(
    argv: Sequence[AS.StrictValue],
    types: type[_ValueT],
) -> TypeGuard[Sequence[_ValueT]]:
    """Checks if all elements of `argv` are of type in `types`."""
    return all(isinstance(arg, types) for arg in argv)


def is_same_type(argv: Sequence[AS.StrictValue]) -> bool:
    return all_equal([type(arg) for arg in argv])


def _format_list(strings: Iterable[str], conj: str = "and"):
    return conj.join(strings)


def check_type(
    metadata: AS.Metadata,
    argv: Sequence[AS.StrictValue],
    types: type[_ValueT],
) -> Sequence[_ValueT]:
    if is_type(argv, types):
        return argv
    arg_type_formatted = _format_list(type(a).__name__ for a in argv)
    raise error.UnsuspectedHangeulTypeError(
        metadata,
        f"인수를 {types} 중에서 주어야 하는데 {arg_type_formatted}를 주었습니다.",
    )


def check_arity(
    metadata: AS.Metadata, argv: Sequence[Any], arities: int | Sequence[int]
):
    if isinstance(arities, int):
        arities = [arities]
    if len(argv) not in arities:
        arities_formatted = _format_list([str(n) for n in arities], "개나 ")
        raise error.UnsuspectedHangeulValueError(
            metadata,
            f"인수를 {arities_formatted}개를 주어야 하는데 {len(argv)}개를 주었습니다.",
        )


def check_min_arity(
    metadata: AS.Metadata, argv: Sequence[Any], minimum_arity: int
):
    if len(argv) < minimum_arity:
        raise error.UnsuspectedHangeulValueError(
            metadata,
            f"인수를 {minimum_arity}개 이상 주어야 하는데 {len(argv)}개를 주었습니다.",
        )


def check_max_arity(
    metadata: AS.Metadata, argv: Sequence[Any], maximum_arity: int
):
    if len(argv) > maximum_arity:
        raise error.UnsuspectedHangeulValueError(
            metadata,
            f"인수를 {maximum_arity}개 이하 주어야 하는데 {len(argv)}개를 주었습니다.",
        )


def match_arguments(
    metadata: AS.Metadata,
    argv: Sequence[AS.Value],
    types: type[_ValueT],
    arities: int | Sequence[int] | None = None,
    min_arity: int | None = None,
    max_arity: int | None = None,
) -> Generator[AS.Value, AS.StrictValue, list[_ValueT]]:
    if arities is not None:
        check_arity(metadata, argv, arities)
    if min_arity is not None:
        check_min_arity(metadata, argv, min_arity)
    if max_arity is not None:
        check_max_arity(metadata, argv, max_arity)
    argv = yield from map_strict(argv)
    return list(check_type(metadata, argv, types))


def match_defaults(
    metadata: AS.Metadata,
    argv: Sequence[_T],
    arity: int,
    defaults: Sequence[_T] = (),
) -> Sequence[_T]:
    argv = list(argv)
    check_max_arity(metadata, argv, arity)
    check_min_arity(metadata, argv, arity - len(defaults))
    if len(argv) < arity:
        deficiency = arity - len(argv)
        argv += list(defaults[-deficiency:])
    return argv


def guessed_wrap(arg: Any) -> AS.StrictValue:
    """Wraps arg based on its type."""
    converter: dict[Any, Any] = {
        int: AS.Integer,
        float: AS.Float,
        complex: AS.Complex,
        bool: AS.Boolean,
        tuple: AS.List,
        str: AS.String,
        bytes: AS.Bytes,
        dict: AS.Dict,
    }
    for t, T in converter.items():
        if isinstance(arg, t):
            return T(arg)
    assert False
