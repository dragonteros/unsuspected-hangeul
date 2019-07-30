
from pbhhg_py import builtins
from pbhhg_py.abstract_syntax import *
from pbhhg_py.parse import encode_number
from pbhhg_py.check import *
from pbhhg_py.builtins.sequence import _expr_apply


def strict(value):
    '''Forces strict evaluation of the value'''
    if isinstance(value, Expr):
        expr, env, cache_box = value
        if cache_box:
            return cache_box[0]
        else:
            cache = strict(interpret(expr, env))
            value.cache_box.append(cache)
            return cache
    else:
        return value


def interpret(expr, env):
    '''Evaluates the expression in given environment and returns a value'''
    if isinstance(expr, Literal):
        return Number(expr.value)

    elif isinstance(expr, FunRef):
        return env.funs[-expr.rel-1]

    elif isinstance(expr, ArgRef):
        assert len(env.funs) == len(env.args)
        relA, relF = expr
        args = env.args[-relF-1]

        relA = strict(interpret(relA, env))
        check_type(relA, Number)
        relA = int(round(relA.value))

        if 0 <= relA < len(args):
            return args[relA]

        raise ValueError(
            ('Out of Range: {} arguments received '
                'but {}-th argument requested').format(len(args), relA))

    elif isinstance(expr, FunDef):
        funs, args = env
        new_funs = funs[:]
        new_env = Env(new_funs, args)
        closure = Closure(expr.body, new_env)
        new_env.funs.append(closure)
        return closure

    elif isinstance(expr, FunCall):
        fun, argv = expr
        arguments = [Expr(arg, env, []) for arg in argv]  # lazy eval
        if isinstance(fun, BuiltinFun):
            return proc_builtin(fun.id, arguments)

        fun_value = strict(interpret(fun, env))
        check_type(fun_value, (Boolean, List, String, Closure))

        if isinstance(fun_value, Boolean):
            check_arity(arguments, 2)
            return arguments[0 if fun_value.value else 1]

        elif isinstance(fun_value, Closure):
            return _expr_apply(fun_value, arguments)

        else:
            check_arity(arguments, 1)
            arg = strict(arguments[0])
            check_type(arg, Number)
            seq, idx = fun_value.value, arg.value
            item = seq[int(round(idx))]
            if isinstance(fun_value, List):
                return item
            else:
                return String(item)

    raise ValueError('Unexpected expression: {}'.format(expr))


def proc_builtin(i, argv):
    '''Execute the built-in function with given arguments and environement
    Args:
        i: Built-in Function ID
        argv: Argument Values for the built-in function
    Returns:
        Return value of the built-in function
    '''
    def _strict(arr): return [strict(a) for a in arr]
    inst = encode_number(i)

    if inst == 'ㅁㄹ':  # 목록
        return List(list(argv))

    if inst == 'ㅁㅈ':  # 문자열
        check_arity(argv, [0, 1])
        if len(argv) == 0:
            return String('')
        [arg] = _strict(argv)
        check_type(arg, (Number, String))
        if is_type(arg, String):
            return arg
        elif arg.value == int(arg.value):
            return String(str(int(arg.value)))
        else:
            return String(str(arg.value))

    if inst == 'ㅂㄱ':  # 빈값
        check_arity(argv, 0)
        return Nil()

    for name in builtins.__all__:
        builtin = __import__('pbhhg_py.builtins.' + name, fromlist=[name])
        if inst in builtin.tbl:
            return builtin.tbl[inst](argv, _strict)

    raise ValueError('Unexpected builtin functions ' + inst)
