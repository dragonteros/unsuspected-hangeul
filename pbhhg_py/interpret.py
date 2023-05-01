from typing import NamedTuple

from pbhhg_py import builtins
from pbhhg_py.abstract_syntax import *
from pbhhg_py.parse import encode_number
from pbhhg_py import utils, error


class ComputationRequest(NamedTuple):
    request: Expr


class Computation:

    def __init__(self, coroutine: utils.Coroutine):
        self.coroutine = coroutine
        self._last_request: Expr | None = None

    def communicate(
        self,
        response: UnsuspectedHangeulStrictValue
        | error.UnsuspectedHangeulError | None,
    ) -> (ComputationRequest | UnsuspectedHangeulValue |
          error.UnsuspectedHangeulError):
        if self._last_request is not None and not self._last_request.cache_box:
            self._last_request.cache_box.append(response)

        assert not isinstance(response, Expr)
        try:
            while True:
                if isinstance(response, error.UnsuspectedHangeulError):
                    request = self.coroutine.throw(response)
                else:
                    request = self.coroutine.send(response)

                if isinstance(request, Expr):
                    if not request.cache_box:
                        self._last_request = request
                        return ComputationRequest(request)
                    request = request.cache_box[0]
                response = request

        except StopIteration as result:
            return_value: UnsuspectedHangeulValue = result.value
            return return_value
        except error.UnsuspectedHangeulError as e:
            return e


def evaluate(coroutine: utils.Coroutine):
    '''Executes coroutine and provides strictly evaluated values
       as it requests.'''
    MAX_STACK_SIZE = 5000
    return_value_or_error = None
    stack_of_cortns = [Computation(coroutine)]

    while stack_of_cortns:
        if len(stack_of_cortns) > MAX_STACK_SIZE:
            raise RuntimeError('Maximum Stack Size Exceeded.')
        computation = stack_of_cortns[-1]
        request_or_result = computation.communicate(return_value_or_error)

        if isinstance(request_or_result, ComputationRequest):
            new_computation = Computation(interpret(request_or_result.request))
            stack_of_cortns.append(new_computation)
            return_value_or_error = None
        else:
            stack_of_cortns.pop()
            if isinstance(request_or_result, Expr):
                new_computation = Computation(interpret(request_or_result))
                stack_of_cortns.append(new_computation)
                return_value_or_error = None
            else:
                return_value_or_error = request_or_result

    return return_value_or_error


def interpret(value: Expr) -> utils.Coroutine:
    '''Interpreter coroutine.
    Args:
        value: an Expr value to interpret
    Yields:
        expr: an Expr value to send to main routine
            which in turn sends strictly evaluated value
    Returns:
        A little more evaluated version of value.
    '''
    expr, env, cache_box = value
    if cache_box:
        return cache_box[0]

    if isinstance(expr, Literal):
        return Integer(expr.value)

    elif isinstance(expr, FunRef):
        return env.funs[-expr.rel - 1]

    elif isinstance(expr, ArgRef):
        assert len(env.funs) == len(env.args)
        relA, relF = expr
        args = env.args[-relF - 1]

        relA = yield Expr(relA, env, [])
        utils.check_type(relA, Integer)
        relA = relA.value

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


def proc_functional(
    fun: UnsuspectedHangeulValue,
    allow: type[Any] | None = None,
    stricted: UnsuspectedHangeulStrictValue | None = None,
):
    """
    Args:
        fun: A maybe-Expr value that may correspond to a function.
        allow: Union of types that are allowed for execution.
        stricted: Cached strict value of fun
    Returns:
        A generator that receives argument list and returns maybe-Expr value.
    """
    if isinstance(fun, Expr) and isinstance(fun.expr, Literal):
        return find_builtin(fun.expr.value)

    fun = stricted or (yield fun)
    allow = Function if allow is None else Function | allow
    utils.check_type(fun, allow)

    if isinstance(fun, Function):
        return fun

    elif isinstance(fun, Boolean):

        def _proc_boolean(arguments):
            utils.check_arity(arguments, 2)
            return arguments[0 if fun.value else 1]
            yield

        return _proc_boolean

    elif isinstance(fun, Dict):

        def _proc_dict(arguments):
            utils.check_arity(arguments, 1)
            arg = yield from utils.recursive_strict(arguments[0])
            return fun.value[arg]

        return _proc_dict

    elif isinstance(fun, Complex):

        def _proc_complex(arguments):
            [arg] = yield from utils.match_arguments(arguments, Integer, 1)
            num, idx = fun.value, arg.value
            if idx in [0, 1]:
                return Float(num.real if idx == 0 else num.imag)
            raise ValueError(
                'Expected 0 or 1 for argument but received {}'.format(idx))

        return _proc_complex

    else:

        def _proc_seq(arguments):
            [arg] = yield from utils.match_arguments(arguments, Integer, 1)
            seq, idx = fun.value, arg.value
            if isinstance(fun, List):
                return seq[idx]
            return utils.guessed_wrap(seq[idx:][:1])

        return _proc_seq


def find_builtin(id: int):
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
    table: dict[str, utils.Coroutine] = {}
    for name in builtins.__all__:
        imported = __import__('pbhhg_py.builtins.' + name, fromlist=[name])
        new_table = imported.build_tbl(proc_functional)
        table.update(new_table)
    return table


BUITLINS = build_builtin_tables()
