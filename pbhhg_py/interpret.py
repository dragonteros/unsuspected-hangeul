
from pbhhg_py import builtins
from pbhhg_py.abstract_syntax import *
from pbhhg_py.parse import encode_number
from pbhhg_py.check import *
from pbhhg_py.check import recursive_strict


def evaluate(coroutine):
    '''Executes coroutine and provides strictly evaluated values
       as it requests.'''
    value = None
    stack_of_cortns = [(coroutine, [])]
    while stack_of_cortns:
        coroutine, cache_boxes = stack_of_cortns[-1]
        try:
            value = coroutine.send(value)
            if isinstance(value, Expr):
                if value.cache_box:
                    value = value.cache_box[0]
                else:
                    cache_boxes = [value.cache_box]
                    stack_of_cortns.append((interpret(value), cache_boxes))
                    value = None
        except StopIteration as result:
            value = result.value
            stack_of_cortns.pop()
            if isinstance(value, Expr):
                cache_boxes += [value.cache_box]
                stack_of_cortns.append((interpret(value), cache_boxes))
                value = None
            else:
                while cache_boxes:
                    cache_boxes.pop().append(value)

    return value


def interpret(value):
    '''Interpreter coroutine.
    Args:
        value: a pbhhg value to interpret
    Yields:
        expr: an Expr value to send to main routine
            which in turn sends strictly evaluated value
    Returns:
        A little more evaluated version of value.
    '''
    if not isinstance(value, Expr):
        return value
    expr, env, cache_box = value
    if cache_box:
        return cache_box[0]

    if isinstance(expr, Literal):
        return Number(expr.value)

    elif isinstance(expr, FunRef):
        return env.funs[-expr.rel-1]

    elif isinstance(expr, ArgRef):
        assert len(env.funs) == len(env.args)
        relA, relF = expr
        args = env.args[-relF-1]

        relA = yield Expr(relA, env, [])
        check_type(relA, Number)
        relA = int(round(relA.value))

        if not 0 <= relA < len(args):
            raise ValueError(
                ('Out of Range: {} arguments received '
                 'but {}-th argument requested').format(len(args), relA))
        return args[relA]

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
        recipe = yield from proc_functional(fun, allow=Callable)
        return (yield from recipe(argv))

    raise ValueError('Unexpected expression: {}'.format(expr))


def proc_functional(fun, allow=(), stricted=None):
    """
    Args:
        fun: A maybe-Expr value that may correspond to a function.
        allow: A list of types that are allowed for execution.
        stricted: Cached strict value of fun
    Returns:
        A generator that receives argument list and returns maybe-Expr value.
    """
    if isinstance(fun, Expr) and isinstance(fun.expr, Literal):
        return find_builtin(fun.expr.value)

    fun = stricted or (yield fun)
    allowed_by_default = (Function, )
    check_type(fun, tuple(allow) + allowed_by_default)

    if isinstance(fun, Function):
        return fun

    elif isinstance(fun, Boolean):
        def _proc_boolean(arguments):
            check_arity(arguments, 2)
            return arguments[0 if fun.value else 1]
            yield
        return _proc_boolean

    elif isinstance(fun, Dict):
        def _proc_dict(arguments):
            check_arity(arguments, 1)
            arg = yield from recursive_strict(arguments[0])
            return fun.value[arg]
        return _proc_dict

    else:
        def _proc_seq(arguments):
            check_arity(arguments, 1)
            arg = yield arguments[0]
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
    table = {}
    for name in builtins.__all__:
        imported = __import__('pbhhg_py.builtins.' + name, fromlist=[name])
        new_table = imported.build_tbl(proc_functional)
        table.update(new_table)
    return table


BUITLINS = build_builtin_tables()
