from pbhhg_py.abstract_syntax import *
from pbhhg_py.check import *

Sequence = (List, String)


def _len(argv, _strict):
    check_arity(argv, 1)
    [seq] = _strict(argv)
    check_type(seq, Sequence)
    return Number(len(seq.value))


def _slice(argv, _strict):
    check_arity(argv, [2, 3, 4])
    argv = _strict(argv)
    check_type(argv[0], Sequence)
    check_type(argv[1:], Number)

    seq = argv[0].value
    start = int(round(argv[1].value))
    end = int(round(argv[2].value)) if len(argv) > 2 else len(seq)
    step = int(round(argv[3].value)) if len(argv) > 3 else 1
    result = seq[start:end:step]
    make = List if is_type(argv[0], List) else String
    return make(result)


def _expr_apply(fun, argv):
    body, canned_env = fun
    canned_funs, canned_args = canned_env
    new_env = Env(canned_funs, canned_args + [argv])
    return Expr(body, new_env, [])


def _map(argv, _strict):
    check_arity(argv, 2)
    seq, fun = _strict(argv)
    check_type(seq, List)  # ?
    check_type(fun, Closure)  # ?
    return List([_expr_apply(fun, [arg]) for arg in seq.value])


def _filter(argv, _strict):  # maybe lazy later?
    check_arity(argv, 2)
    seq, fun = _strict(argv)
    check_type(seq, List)  # Seq?
    check_type(fun, Closure)  # Seq?

    fit_check = [_expr_apply(fun, [arg]) for arg in seq.value]
    fit_check = _strict(fit_check)
    check_type(fit_check, Boolean)
    return List([arg for arg, fits in zip(seq.value, fit_check) if fits.value])


tbl = {
    'ㅈㄷ': _len,  # 장단
    'ㅂㅈ': _slice,  # 발췌
    'ㅁㄷ': _map,  # ~마다
    'ㅅㅂ': _filter,  # 선별
}

'''
  - spread (ㅈㄱ)
  - fold (ㅅㄹ)
'''
