"""Useful utilities for arguments."""
from typing import Generator, Iterable, TypeVar, TypeGuard

from pbhhg_py import abstract_syntax as AS

Coroutine = Generator[AS.UnsuspectedHangeulValue,
                      AS.UnsuspectedHangeulStrictValue,
                      AS.UnsuspectedHangeulValue]


def map_strict(
    seq: Iterable[AS.UnsuspectedHangeulValue],
    generator: Coroutine | None = None
) -> Generator[AS.UnsuspectedHangeulValue, AS.UnsuspectedHangeulStrictValue,
               list[AS.UnsuspectedHangeulStrictValue]]:
    result = []
    for item in seq:
        if generator is None:
            item = yield item
        else:
            item = yield from generator(item)
        result.append(item)
    return result


def recursive_strict(item):
    item = yield item
    if isinstance(item, AS.List):
        v = item.value
        v = yield from map_strict(v, recursive_strict)
        return AS.List(tuple(v))
    elif isinstance(item, AS.Dict):
        if not item.value:
            return AS.Dict({})
        keys, values = zip(*item.value.items())
        values = yield from map_strict(values, recursive_strict)
        d = dict(zip(keys, values))
        return AS.Dict(d)
    return item


_T = TypeVar('_T')


def all_equal(seq: Iterable[_T]):
    """Checks if all elements in `seq` are equal."""
    seq = list(seq)
    return not seq or seq.count(seq[0]) == len(seq)


def _force_list(condition: _T | list[_T]) -> list[_T]:
    if isinstance(condition, list):
        return condition
    return [condition]


_ValueT = TypeVar('_ValueT', bound=AS.Any)


def is_type(
    argv: AS.Any | list[AS.Any],
    types: type[_ValueT],
) -> TypeGuard[_ValueT | list[_ValueT]]:
    '''Checks if all elements of `argv` are of type in `types`.'''
    argv = _force_list(argv)
    return all(isinstance(arg, types) for arg in argv)


def is_same_type(argv: list[AS.Any]) -> TypeGuard[list[_ValueT]]:
    return all_equal(type(arg) for arg in argv)


def _format_list(strings: Iterable[str], conj='and'):
    strings = list(strings)
    if len(strings) < 2:
        return ''.join(strings)
    return '{} {} {}'.format(', '.join(strings[:-1]), conj, strings[-1])


def check_type(argv: AS.Any | list[AS.Any], types: type[AS.Any]):
    if not is_type(argv, types):
        argv = _force_list(argv)
        arg_type_formatted = _format_list(type(a).__name__ for a in argv)
        raise ValueError('Expected arguments of types '
                         f'among {types} but received {arg_type_formatted}.')


def check_same_type(argv: list[AS.Any]):
    if not is_same_type(argv):
        arg_type_formatted = _format_list(type(a).__name__ for a in argv)
        raise ValueError('Expected arguments of the same type '
                         'but received {}.'.format(arg_type_formatted))


def check_arity(argv: list[AS.Any], arities: int | list[int]):
    arities = _force_list(arities)
    if len(argv) not in arities:
        arities_formatted = _format_list(arities, 'or')
        raise ValueError('Expected {} arguments but received {}.'.format(
            arities_formatted, len(argv)))


def check_min_arity(argv: list[AS.Any], minimum_arity: int):
    if len(argv) < minimum_arity:
        raise ValueError(
            'Expected at least {} arguments but received {}.'.format(
                minimum_arity, len(argv)))


def check_max_arity(argv: list[AS.Any], maximum_arity: int):
    if len(argv) > maximum_arity:
        raise ValueError(
            'Expected at most {} arguments but received {}.'.format(
                maximum_arity, len(argv)))


def match_arguments(
    argv: list[AS.Any],
    types: type[AS.Any],
    arities: list[int] | None = None,
    min_arity: int = 0,
):
    if arities is not None:
        check_arity(argv, arities)
    if min_arity:
        check_min_arity(argv, min_arity)
    argv = yield from map_strict(argv)
    check_type(argv, types)
    return argv


def match_defaults(
        argv: list[AS.UnsuspectedHangeulValue],
        arity: int,
        defaults: Iterable[AS.UnsuspectedHangeulValue] = (),
):
    check_max_arity(argv, arity)
    check_min_arity(argv, arity - len(defaults))
    if len(argv) < arity:
        deficiency = arity - len(argv)
        argv += list(defaults[-deficiency:])
    return argv


def guessed_wrap(arg: AS.Any):
    """Wraps arg based on its type."""
    converter = {
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
    raise TypeError('Cannot guess type of {}.'.format(arg))
