import os
from typing import Mapping, Sequence

from pbhhg_py import abstract_syntax as AS
from pbhhg_py import error
from pbhhg_py import modules
from pbhhg_py import parse
from pbhhg_py import utils


class BuiltinModule(AS.Function):
    def __init__(self, module: AS.Evaluation, keys: list[str]):
        self.module = module
        self._str = "<Builtin Module {}>".format(" ".join(keys))

    def __call__(
        self, metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        return (yield from self.module(metadata, argv))


_BUITLIN_MODULE_REGISTRY: dict[AS.StrictValue, AS.Value] = {}
_MODULE_REGISTRY: dict[str, AS.Value] = {}


def _get_module_from_registry(filepath: str):
    for regpath in _MODULE_REGISTRY:
        if os.path.samefile(filepath, regpath):
            return _MODULE_REGISTRY[regpath]
    return None


def _load_from_path(filepath: str):
    module = _get_module_from_registry(filepath)
    if module is not None:
        return module

    with open(filepath, "r", encoding="utf-8") as reader:
        program = reader.read()
    exprs = parse.parse(filepath, program)
    if len(exprs) != 1:
        raise error.UnsuspectedHangeulValueError(
            exprs[0].metadata,
            f"모듈에는 표현식이 하나만 있어야 하는데 {len(exprs)}개가 있습니다.",
        )
    env = AS.Env([], [])
    module = AS.Expr(exprs[0], env)

    _MODULE_REGISTRY[filepath] = module
    return module


def _load_from_literal(metadata: AS.Metadata, literals: list[int]):
    """Loads a module at a path described by `literals`

    Args:
        literals: A list of numbers.

    Returns:
        module: Imported module. BuiltinModule or arbitrary pbhhg object.
    """
    name = " ".join(parse.encode_number(n) for n in literals)
    errmsg = f"정수 리터럴열 {name}에 맞는 모듈을 찾지 못했습니다."
    # Search builtins
    if literals[0] == 5:
        module = AS.Dict(_BUITLIN_MODULE_REGISTRY)
        for idx in literals[1:]:
            if not isinstance(module, AS.Dict):
                raise error.UnsuspectedHangeulNotFoundError(metadata, errmsg)
            module = module.value[AS.Integer(idx)]
        return module

    # Search files
    filepath = _search_file_from_literal(metadata, literals)
    if filepath is None:
        raise error.UnsuspectedHangeulNotFoundError(metadata, errmsg)
    module = _load_from_path(filepath)
    return module


def _search_file_from_literal(
    metadata: AS.Metadata, literals: list[int], location: str = "."
) -> str | None:
    if not literals:
        if not os.path.isfile(location):
            return None  # TODO: Dict?
        return location

    results: list[str] = []
    cur, *sub = literals
    for entry in os.listdir(location):
        if not _matches_literal(entry, cur):
            continue
        search_path = os.path.join(location, entry)
        result = _search_file_from_literal(metadata, sub, search_path)
        if result:
            results.append(result)

    if len(results) > 1:  # maybe filter by extension?
        raise error.UnsuspectedHangeulImportError(
            metadata,
            f"{location}에 정수 리터럴열 {literals}에 맞는 모듈이 "
            f"{len(results)}개 있어 모호합니다.",
        )
    return results[0] if results else None


def _matches_literal(string: str, literal: int):
    string = " ".join(parse.normalize(string)).strip()
    try:
        parsed_literal = parse.parse_number(string)
    except ValueError:
        return False
    return literal == parsed_literal


def _get_literals(exprs: Sequence[AS.Value]) -> list[int] | None:
    literals: list[int] = []
    for expr in exprs:
        if isinstance(expr, AS.Expr) and isinstance(expr.expr, AS.Literal):
            literals.append(expr.expr.value)
        else:
            return None
    return literals


_CONSTANT_TYPES = int | float | complex | bool | str | bytes


def _construct_builtin_module(
    data: _CONSTANT_TYPES
    | AS.Evaluation
    | utils.DeepDict[str, _CONSTANT_TYPES | AS.Evaluation],
    keys: list[str],
):
    """Recursively iterates over dict to convert python values
    to pbhhg values and wrap functions in BuiltinModule."""
    if isinstance(data, Mapping):
        return _construct_builtin_modules(data, keys)
    elif callable(data):
        return BuiltinModule(data, keys)
    else:
        return utils.guessed_wrap(data)


def _construct_builtin_modules(
    data: utils.DeepDict[str, _CONSTANT_TYPES | AS.Evaluation],
    keys: list[str],
) -> AS.Dict:
    """Recursively iterates over dict to convert python values
    to pbhhg values and wrap functions in BuiltinModule."""
    value: dict[AS.StrictValue, AS.Value] = {
        AS.Integer(parse.parse_number(k)): _construct_builtin_module(
            v, keys + [k]
        )
        for k, v in data.items()
    }
    return AS.Dict(value)


def build_tbl(
    proc_functional: utils.ProcFunctional,
) -> dict[str, AS.Evaluation]:
    def _register_builtin_module(name: str) -> AS.Dict:
        """Builds a Dict based on the table from module `name`."""
        module = __import__("pbhhg_py.modules." + name, fromlist=[name])
        data: dict[str, AS.Evaluation] = module.build_tbl(proc_functional)
        return _construct_builtin_modules(data, ["ㅂ"])

    def _import(
        metadata: AS.Metadata, argv: Sequence[AS.Value]
    ) -> AS.EvalContext:
        utils.check_min_arity(metadata, argv, 1)
        literals = _get_literals(argv)
        if literals is not None:
            return _load_from_literal(metadata, literals)

        utils.check_arity(metadata, argv, 1)
        filepath = yield argv[0]
        [filepath] = utils.check_type(metadata, [filepath], AS.String)
        return _load_from_path(filepath.value)

    for name in modules.__all__:
        module = _register_builtin_module(name)
        _BUITLIN_MODULE_REGISTRY.update(module.value)

    return {
        "ㅂ": _import,  # 불러오기
    }
