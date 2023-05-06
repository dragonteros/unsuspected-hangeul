import dataclasses
from typing import Generator, Generic, Sequence, TypeVar

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import builtins
from pbhhg_py import error
from pbhhg_py import parse
from pbhhg_py import utils

_T = TypeVar("_T")


@dataclasses.dataclass
class ComputationRequest:
    value: AS.Expr


@dataclasses.dataclass
class ComputationResponse:
    value: AS.StrictValue | AS.UnsuspectedHangeulError


@dataclasses.dataclass
class ComputationResult(Generic[_T]):
    value: _T | AS.UnsuspectedHangeulError


class StackFrameBase(Generic[_T]):
    def __init__(self, coroutine: Generator[AS.Value, AS.StrictValue, _T]):
        self._coroutine = coroutine

    def communicate(
        self,
        response: ComputationResponse | None,
    ) -> ComputationRequest | ComputationResult[_T]:
        try:
            while True:
                if response is None:
                    request = next(self._coroutine)
                elif isinstance(response.value, AS.UnsuspectedHangeulError):
                    request = self._coroutine.throw(response.value)
                else:
                    request = self._coroutine.send(response.value)

                if isinstance(request, AS.Expr):
                    if not request.cache_box.value:
                        return ComputationRequest(request)
                    request = request.cache_box.value
                response = ComputationResponse(request)

        except StopIteration as result:
            return ComputationResult(result.value)
        except AS.UnsuspectedHangeulError as e:
            return ComputationResult(e)


class StackFrame(StackFrameBase[AS.Value]):
    def __init__(self, request: ComputationRequest):
        self._cache_box = request.value.cache_box
        super().__init__(interpret(request.value))

    def communicate(
        self, response: ComputationResponse | None
    ) -> ComputationRequest | ComputationResult[AS.Value]:
        request_or_result = super().communicate(response)
        if isinstance(request_or_result, ComputationResult):
            if isinstance(request_or_result.value, AS.Expr):
                request_or_result.value.cache_box.requestor = self._cache_box
            else:
                self._cache_box.resolve(request_or_result.value)
        return request_or_result


def evaluate(coroutine: Generator[AS.Value, AS.StrictValue, _T]) -> _T:
    """Executes coroutine and provides strictly evaluated values
    as it requests."""
    MAX_STACK_SIZE = 5000
    head = StackFrameBase(coroutine)
    tail: list[StackFrame] = []

    response: ComputationResponse | None = None
    while True:
        if tail:
            if len(tail) >= MAX_STACK_SIZE:
                raise RuntimeError("Maximum Stack Size Exceeded.")

            request_or_result = tail[-1].communicate(response)
            if isinstance(request_or_result, ComputationRequest):
                tail.append(StackFrame(request_or_result))
                response = None
            elif isinstance(request_or_result.value, AS.Expr):
                request = ComputationRequest(request_or_result.value)
                tail[-1] = StackFrame(request)
                response = None
            else:
                tail.pop()
                response = ComputationResponse(request_or_result.value)
        else:
            request_or_result = head.communicate(response)
            if isinstance(request_or_result, ComputationRequest):
                tail.append(StackFrame(request_or_result))
                response = None
            else:
                result = request_or_result.value
                if isinstance(result, AS.UnsuspectedHangeulError):
                    raise result
                return result


def interpret(value: AS.Expr) -> AS.EvalContext:
    """Interpreter coroutine.

    Args:
        value: an Expr value to interpret

    Yields:
        expr: an Expr value to send to main routine
            which in turn sends strictly evaluated value

    Returns:
        A little more evaluated version of value.
    """
    expr = value.expr
    env = value.env

    if value.cache_box.value:
        cache = value.cache_box.value
        if isinstance(cache, AS.UnsuspectedHangeulError):
            raise cache
        return cache

    if isinstance(expr, AS.Literal):
        return AS.Integer(expr.value)

    elif isinstance(expr, AS.FunRef):
        try:
            return env.funs[-expr.rel - 1]
        except IndexError:
            raise error.UnsuspectedHangeulOutOfRangeError("함수 참조의 범위를 벗어났습니다.")

    elif isinstance(expr, AS.ArgRef):
        assert len(env.funs) == len(env.args)
        relA, relF = expr
        try:
            args = env.args[-relF - 1]
        except IndexError:
            raise error.UnsuspectedHangeulOutOfRangeError(
                "존재하지 않는 함수에 대한 인수 참조를 시도했습니다."
            )

        relA = yield AS.Expr(relA, env)
        [relA] = utils.check_type([relA], AS.Integer)

        if not 0 <= relA.value < len(args):
            raise error.UnsuspectedHangeulOutOfRangeError(
                f"{relA.value}번째 인수를 참조하는데 {len(args)}개의 인수만 받았습니다."
            )
        return args[relA.value]

    elif isinstance(expr, AS.FunDef):
        funs, args = env
        new_funs = funs[:]
        new_env = AS.Env(new_funs, args)
        closure = AS.Closure(expr.body, new_env)
        new_env.funs.append(closure)
        return closure

    fun, argv = expr
    fun = AS.Expr(fun, env)
    argv = [AS.Expr(arg, env) for arg in argv]
    fun = yield from utils.strict_functional(fun)
    recipe = proc_functional(fun, general_callable=True)
    return (yield from recipe(argv))


def proc_functional(
    fun: AS.StrictValue | AS.BuiltinFunction,
    general_callable: bool = False,
) -> AS.Evaluation:
    """
    Args:
        fun: A maybe-Expr value that may correspond to a function.
        general_callable: Allow non-Function callable types.

    Returns:
        A generator that receives argument list and returns maybe-Expr value.
    """
    if isinstance(fun, AS.BuiltinFunction):
        return find_builtin(fun.literal.value)

    allow = AS.Callable if general_callable else AS.Function
    [fun] = utils.check_type([fun], allow)

    if isinstance(fun, AS.Boolean):
        value = fun.value

        def _proc_boolean(argv: Sequence[AS.Value]) -> AS.EvalContext:
            utils.check_arity(argv, 2)
            return argv[0 if value else 1]
            yield

        return _proc_boolean

    elif isinstance(fun, AS.Dict):

        def _proc_dict(argv: Sequence[AS.Value]) -> AS.EvalContext:
            utils.check_arity(argv, 1)
            arg = yield from utils.recursive_strict(argv[0])
            try:
                return fun.value[arg]
            except KeyError:
                raise error.UnsuspectedHangeulNotFoundError(
                    f"사전에 다음 표제가 없습니다: {arg}"
                )

        return _proc_dict

    elif isinstance(fun, AS.Complex):

        def _proc_complex(argv: Sequence[AS.Value]) -> AS.EvalContext:
            [arg] = yield from utils.match_arguments(argv, AS.Integer, 1)
            num, idx = fun.value, arg.value
            if idx in [0, 1]:
                return AS.Float(num.real if idx == 0 else num.imag)
            raise error.UnsuspectedHangeulValueError(
                f"복소수 객체의 {idx}번째 요소를 접근하려고 했습니다."
            )

        return _proc_complex

    elif isinstance(fun, AS.Sequence):
        seq = fun.value

        def _proc_seq(argv: Sequence[AS.Value]) -> AS.EvalContext:
            [arg] = yield from utils.match_arguments(argv, AS.Integer, 1)
            idx = arg.value
            if isinstance(seq, tuple):
                try:
                    return seq[idx]
                except IndexError:
                    raise error.UnsuspectedHangeulOutOfRangeError(
                        f"목록의 범위 밖의 번호를 요청했습니다."
                    )
            return utils.guessed_wrap(seq[idx:][:1])

        return _proc_seq

    return fun


def find_builtin(id: int):
    """Finds the recipe function corresponding to the builtin function id.

    Args:
        id: Built-in Function ID

    Returns:
        Corresponding function that takes arguments.
    """
    inst = parse.encode_number(id)
    if inst in BUITLINS:
        return BUITLINS[inst]
    raise error.UnsuspectedHangeulTypeError(
        f"{inst}라는 이름의 기본 제공 함수를 찾지 못했습니다."
    )


def build_builtin_tables():
    table: dict[str, AS.Evaluation] = {}
    for name in builtins.__all__:
        imported = __import__("pbhhg_py.builtins." + name, fromlist=[name])
        new_table = imported.build_tbl(proc_functional)
        table.update(new_table)
    return table


BUITLINS = build_builtin_tables()
