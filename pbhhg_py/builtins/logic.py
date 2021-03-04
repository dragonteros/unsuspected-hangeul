from pbhhg_py.abstract_syntax import *
from pbhhg_py.utils import *


def build_tbl(proc_functional):
    def _listed_equals(seqs):
        """Check equality for lists of pbhhg values."""
        seqs = list(seqs)
        if not all_equal(len(l) for l in seqs):
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
        if not all_equal(d.keys() for d in dicts):
            return False
        for k in dicts[0]:
            if not (yield from _equals(d[k] for d in dicts)).value:
                return False
        return True

    def _equals(argv):
        argv = yield from map_strict(argv)
        if is_type(argv, Number):
            return Boolean(all_equal(argv))
        if is_type(argv, List):
            lists = [seq.value for seq in argv]
            return Boolean((yield from _listed_equals(lists)))
        if is_type(argv, Dict):
            dicts = [d.value for d in argv]
            return Boolean((yield from _dict_equals(dicts)))
        if is_type(argv, IO):
            if not all_equal(a.inst for a in argv):
                return Boolean(False)
            argvs = [a.argv for a in argv]
            return Boolean((yield from _listed_equals(argvs)))
        return Boolean(is_same_type(argv) and all_equal(argv))

    def _negate(argv):
        [arg] = yield from match_arguments(argv, Boolean, 1)
        return Boolean(not arg.value)

    def _less_than(argv):
        argv = yield from match_arguments(argv, Real, 2)
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
