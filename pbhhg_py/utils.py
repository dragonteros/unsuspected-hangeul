"""Useful utilities for arguments."""

from pbhhg_py import abstract_syntax as AS


def recursive_strict(item):
    item = yield item
    if isinstance(item, AS.List):
        v = item.value
        v = yield from [(yield from recursive_strict(a)) for a in v]
        return AS.List(tuple(v))
    elif isinstance(item, AS.Dict):
        d = item.value
        d = yield from {k: (yield from recursive_strict(d[k])) for k in d}
        return AS.Dict(d)
    return item


def all_equal(seq):
    """Checks if all elements in `seq` are equal."""
    seq = list(seq)
    return not seq or seq.count(seq[0]) == len(seq)


def _force_list(condition):
    if isinstance(condition, list):
        return condition
    return [condition]


def is_type(argv, types):
    '''Checks if all elements of `argv` are of type in `types`.'''
    argv = _force_list(argv)
    return all(isinstance(arg, types) for arg in argv)


def is_same_type(argv):
    argv = _force_list(argv)
    return all_equal(type(arg) for arg in argv)


def _format_list(strings, conj='and'):
    strings = list(strings)
    if len(strings) < 2:
        return ''.join(strings)
    return '{} {} {}'.format(', '.join(strings[:-1]), conj, strings[-1])


def _flatten_types(node):
    if isinstance(node, (list, tuple)):
        return sum([_flatten_types(a) for a in node], [])
    return [node]


def check_type(argv, types):
    if not is_type(argv, types):
        argv = _force_list(argv)
        arg_type_formatted = _format_list(type(a).__name__ for a in argv)
        types = _flatten_types(types)
        type_formatted = _format_list(a.__name__ for a in types)
        raise ValueError('Expected arguments of types '
                         'among {} but received {}.'
                         .format(type_formatted, arg_type_formatted))


def check_same_type(argv):
    argv = _force_list(argv)
    if not is_same_type(argv):
        arg_type_formatted = _format_list(type(a).__name__ for a in argv)
        raise ValueError('Expected arguments of the same type '
                         'but received {}.'.format(
                             arg_type_formatted))


def check_arity(argv, arities):
    arities = _force_list(arities)
    if len(argv) not in arities:
        arities_formatted = _format_list(arities, 'or')
        raise ValueError('Expected {} arguments but received {}.'
                         .format(arities_formatted, len(argv)))


def check_min_arity(argv, minimum_arity):
    if len(argv) < minimum_arity:
        raise ValueError('Expected at least {} arguments but received {}.'
                         .format(minimum_arity, len(argv)))


def check_max_arity(argv, maximum_arity):
    if len(argv) > maximum_arity:
        raise ValueError('Expected at most {} arguments but received {}.'
                         .format(maximum_arity, len(argv)))


def match_arguments(argv, types, arities=None, min_arity=0):
    if arities is not None:
        check_arity(argv, arities)
    if min_arity:
        check_min_arity(argv, min_arity)
    argv = yield from [(yield arg) for arg in argv]
    check_type(argv, types)
    return argv


def match_defaults(argv, arity, defaults=()):
    check_max_arity(argv, arity)
    check_min_arity(argv, arity - len(defaults))
    if len(argv) < arity:
        deficiency = arity - len(argv)
        argv += list(defaults[-deficiency:])
    return argv


def guessed_wrap(arg):
    """Wraps arg based on its type."""
    converter = {
        int: AS.Integer,
        float: AS.Float,
        complex: AS.Complex,
        bool: AS.Boolean,
        tuple: AS.List,
        str: AS.String,
        bytes: AS.Bytes,
        dict: AS.Dict
    }
    for t, T in converter.items():
        if isinstance(arg, t):
            return T(arg)
    raise TypeError('Cannot guess type of {}.'.format(arg))
