from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *


def _all_equal(seq):
    """Checks if all elements in `seq` are equal.
    Args:
        seq: A list of python values."""
    seq = list(seq)
    return not seq or seq.count(seq[0]) == len(seq)


def build_tbl(proc_functional):
    def _listed_equals(seqs):
        """Check equality for lists of pbhhg values."""
        seqs = list(seqs)
        if not _all_equal(len(l) for l in seqs):
            return False
        for tiers in zip(*seqs):
            if not (yield from _equals(tiers)).value:
                return False
        return True

    def _dict_equals(dicts):
        """Check equality for dicts of pbhhg values."""
        dicts = list(dicts)
        if not dicts:
            return True
        if not _all_equal(d.keys() for d in dicts):
            return False
        for k in dicts[0]:
            if not (yield from _equals(d[k] for d in dicts)).value:
                return False
        return True

    def _equals(argv):
        argv = yield from [(yield arg) for arg in argv]
        if not is_type(argv, Any):  # check all have same type
            return Boolean(False)
        if is_type(argv, Nil):
            return Boolean(True)
        if is_type(argv, List):
            lists = [seq.value for seq in argv]
            return Boolean((yield from _listed_equals(lists)))
        if is_type(argv, Dict):
            dicts = [d.value for d in argv]
            return Boolean((yield from _dict_equals(dicts)))
        if is_type(argv, IO):
            if not _all_equal(a.inst for a in argv):
                return Boolean(False)
            argvs = [a.argv for a in argv]
            return Boolean((yield from _listed_equals(argvs)))
        return Boolean(_all_equal(argv))

    def _negate(argv):
        check_arity(argv, 1)
        arg = yield argv[0]
        check_type(arg, Boolean)
        return Boolean(not arg.value)

    def _less_than(argv):
        check_arity(argv, 2)
        argv = yield from [(yield arg) for arg in argv]
        check_type(argv, Number)
        return Boolean(argv[0].value < argv[1].value)

    def _true(argv):
        check_arity(argv, 0)
        return Boolean(True)
        yield

    def _false(argv):
        check_arity(argv, 0)
        return Boolean(False)
        yield

    return {
        'ㄴ': _equals,  # 같다 (<- 는)
        'ㅁ': _negate,  # 부정 (<- 못하다)
        'ㅈ': _less_than,  # 작다
        'ㅈㅈ': _true,  # 진짜
        'ㄱㅈ': _false,  # 가짜
    }
