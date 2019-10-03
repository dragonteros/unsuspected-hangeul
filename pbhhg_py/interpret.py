
from pbhhg_py import builtins
from pbhhg_py.abstract_syntax import *
from pbhhg_py.parse import encode_number
from pbhhg_py.check import *
from pbhhg_py.check import recursive_map


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
        fun = Expr(fun, env, [])
        argv = [Expr(arg, env, []) for arg in argv]
        recipe = proc_functional(fun, allow=Callable)
        return recipe(argv)

    raise ValueError('Unexpected expression: {}'.format(expr))


def proc_functional(fun, allow=(), stricted=None):
    """
    Args:
        fun: A maybe-Expr value that may correspond to a function.
        allow: A list of types that are allowed for execution.
        stricted: Cached strict value of fun
    Returns:
        A recipe function that receives argument list and returns the value.
    """
    if isinstance(fun, Expr) and isinstance(fun.expr, Literal):
        return find_builtin(fun.expr.value)

    fun = stricted or strict(fun)
    allowed_by_default = (Function, )
    check_type(fun, tuple(allow) + allowed_by_default)

    if isinstance(fun, Function):
        return fun

    elif isinstance(fun, Boolean):
        def _proc_boolean(arguments):
            check_arity(arguments, 2)
            return arguments[0 if fun.value else 1]
        return _proc_boolean

    elif isinstance(fun, Dict):
        def _proc_dict(arguments):
            check_arity(arguments, 1)
            arg = recursive_map(arguments[0], strict)
            return fun.value[arg]
        return _proc_dict

    else:
        def _proc_seq(arguments):
            check_arity(arguments, 1)
            arg = strict(arguments[0])
            check_type(arg, Number)
            seq, idx = fun.value, arg.value
            idx = int(round(idx))
            item = seq[idx:idx+1] if isinstance(fun, Bytes) else seq[idx]
            if isinstance(fun, List):
                return item
            elif isinstance(fun, String):
                return String(item)
            elif isinstance(fun, Bytes):
                return Bytes(item)
        return _proc_seq


def find_builtin(id):
    '''Finds the recipe function corresponding to the builtin function id.
    Args:
        id: Built-in Function ID
    Returns:
        Return corresponding function that takes arguments
    '''
    inst = encode_number(id)
    if inst in BUITLINS:
        return BUITLINS[inst]
    raise ValueError('Unexpected builtin functions ' + inst)


def build_builtin_tables():
    def _strict(argv):
        return [strict(arg) for arg in argv]

    table = {}
    for name in builtins.__all__:
        imported = __import__('pbhhg_py.builtins.' + name, fromlist=[name])
        new_table = imported.build_tbl(proc_functional, _strict)
        table.update(new_table)
    return table

BUITLINS = build_builtin_tables()
