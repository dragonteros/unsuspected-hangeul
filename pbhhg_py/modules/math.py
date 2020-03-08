"""Does math stuff."""
import math
import cmath

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import utils


def _isclose(a, b):
    return cmath.isclose(a, b, abs_tol=1e-16)


def _round_to_inf(x):
    return math.ceil(x) if x > 0 else math.floor(x)


def build_tbl(proc_functional):
    def _wrap(_fn, arity, ret_type=utils.guessed_wrap, arg_type=AS.Number):
        def _proc(argv):
            argv = yield from utils.match_arguments(argv, arg_type, arity)
            return ret_type(_fn(*(arg.value for arg in argv)))
        return _proc

    def _wrap2(_fn_real, _fn_complex):
        def _proc(argv):
            [arg] = yield from utils.match_arguments(argv, AS.Number, 1)
            try:
                return AS.Float(_fn_real(arg.value))
            except (TypeError, ValueError):
                return AS.Complex(_fn_complex(arg.value))
        return _proc

    _atan1 = _wrap2(math.atan, cmath.atan)
    _atan2 = _wrap(math.atan2, 2, AS.Float, arg_type=AS.Real)

    def _atan(argv):
        _fn = _atan2 if len(argv) == 2 else _atan1
        return (yield from _fn(argv))

    return {'ㅅ': {
        'ㅂ': math.pi,  # 파이
        'ㅈ': math.e,  # 자연상수
        'ㅁ': math.inf,  # 무한대
        'ㄴ': math.nan,  # NaN
        'ㄱ': _wrap(_isclose, 2, AS.Boolean),  # 가깝다
        'ㄴㄴ': _wrap(cmath.isnan, 1, AS.Boolean),  # ~ ㄴ ㄴㅎㄷ
        'ㅁㄴ': _wrap(cmath.isinf, 1, AS.Boolean),  # ~ ㅁ ㄴㅎㄷ
        'ㅈㄷ': _wrap(abs, 1),  # 절댓값
        'ㄹㄱ': _wrap2(math.log, cmath.log),  # log
        'ㅅㄴ': _wrap2(math.sin, cmath.sin),  # sin
        'ㄴㅅ': _wrap2(math.asin, cmath.asin),
        'ㄱㅅ': _wrap2(math.cos, cmath.cos),  # cos
        'ㅅㄱ': _wrap2(math.acos, cmath.acos),
        'ㄷㄴ': _wrap2(math.tan, cmath.tan),  # tan
        'ㄴㄷ': _atan,
        'ㅂㄹ': {  # 자르기
            'ㄱ': _wrap(math.trunc, 1, AS.Integer, arg_type=AS.Real),
            'ㄴ': _wrap(math.floor, 1, AS.Integer, arg_type=AS.Real),
            'ㄷ': _wrap(round, 1, AS.Integer, arg_type=AS.Real),
            'ㄹ': _wrap(math.ceil, 1, AS.Integer, arg_type=AS.Real),
            'ㅁ': _wrap(_round_to_inf, 1, AS.Integer, arg_type=AS.Real),
        }
    }}
