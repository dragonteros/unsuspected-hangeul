"""Checking tools for arguments."""

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


def _force_list(condition):
    if isinstance(condition, list):
        return condition
    return [condition]


def _matches(argv, desired_type):
    argv = _force_list(argv)
    return all(isinstance(arg, desired_type) for arg in argv)


def is_type(argv, desired_types):
    desired_types = _force_list(desired_types)
    return any(_matches(argv, desired_type) for desired_type in desired_types)


def check_type(argv, desired_type):
    if not is_type(argv, desired_type):
        raise ValueError('Arguments of type {} expected but received {}.'
                         .format(desired_type, argv))


def check_arity(argv, desired_arities):
    desired_arities = _force_list(desired_arities)
    if len(argv) not in desired_arities:
        raise ValueError('{} arguments expected but received {}.'
                         .format(desired_arities, len(argv)))


def check_min_arity(argv, minimum_arity):
    if len(argv) < minimum_arity:
        raise ValueError('At least {} arguments expected but received {}.'
                         .format(minimum_arity, len(argv)))
