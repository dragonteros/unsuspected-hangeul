from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def _all_equal(seq):
    """Checks if all elements in `seq` are equal.
    Args:
        seq: A list of python values."""
    seq = list(seq)
    return not seq or seq.count(seq[0]) == len(seq)


def _listed_equals(seqs, _strict):
    """Check equality for lists of pbhhg values."""
    seqs = list(seqs)
    if not _all_equal(len(l) for l in seqs):
        return False
    return all(_equals(tiers, _strict) for tiers in zip(*seqs))


def _equals(argv, _strict):
    argv = _strict(argv)
    if not is_type(argv, Any):  # check all have same type
        return Boolean(False)
    if is_type(argv, Nil):
        return Boolean(True)
    elif is_type(argv, Closure):
        # Note: Env, and therefore Closure, is equal to nothing but itself.
        return Boolean(not argv or all(argv[0] is a for a in argv[1:]))
    elif is_type(argv, List):
        lists = [seq.value for seq in argv]
        return Boolean(_listed_equals(lists, _strict))
    elif is_type(argv, IO):
        if not _all_equal(a.inst for a in argv):
            return Boolean(False)
        return Boolean(_listed_equals([a.argv for a in argv], _strict))
    else:
        return Boolean(_all_equal(argv))


def _negate(argv, _strict):
    check_arity(argv, 1)
    [arg] = _strict(argv)
    check_type(arg, Boolean)
    return Boolean(not arg.value)


def _less_than(argv, _strict):
    check_arity(argv, 2)
    argv = _strict(argv)
    check_type(argv, Number)
    return Boolean(argv[0].value < argv[1].value)


def _true(argv, _strict):
    check_arity(argv, 0)
    return Boolean(True)


def _false(argv, _strict):
    check_arity(argv, 0)
    return Boolean(False)


tbl = {
    'ㄴ': _equals,  # 같다 (<- 는)
    'ㅁ': _negate,  # 부정 (<- 못하다)
    'ㅈ': _less_than,  # 작다
    'ㅈㅈ': _true,  # 진짜
    'ㄱㅈ': _false,  # 가짜
}
