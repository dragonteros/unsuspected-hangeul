import os

from pbhhg_py.abstract_syntax import *
from pbhhg_py import check
from pbhhg_py import modules
from pbhhg_py import parse


class BuiltinModule(Function):
    def __init__(self, module, keys):
        self.module = module
        self._str = '<Builtin Module {}>'.format(' '.join(keys))

    def __str__(self):
        return self._str

    def __call__(self, args):
        return (yield from self.module(args))


BUITLIN_MODULE_REGISTRY = {}
MODULE_REGISTRY = {}


def get_module_from_registry(filepath):
    for regpath in MODULE_REGISTRY:
        if os.path.samefile(filepath, regpath):
            return MODULE_REGISTRY[regpath]
    return None


def load_from_path(filepath):
    module = get_module_from_registry(filepath)
    if module is not None:
        return module

    with open(filepath, 'r') as reader:
        program = reader.read()
    exprs = parse.parse(program)
    if len(exprs) != 1:
        raise ValueError('A module file should contain exactly '
                         'one object but received: {}'.format(len(exprs)))
    env = Env([], [])
    module = yield Expr(exprs[0], env, [])

    MODULE_REGISTRY[filepath] = module
    return module


def load_from_literal(literals):
    """Loads a module at a path described by `literals`
    Args:
        literals: A list of numbers.
    Returns:
        module: Imported module. BuiltinModule or arbitrary pbhhg object.
    """
    name = ' '.join(parse.encode_number(l) for l in literals)
    errmsg = 'No module found under literal sequence {}.'.format(name)
    # Search builtins
    if literals[0] == 5:
        module = BUITLIN_MODULE_REGISTRY[Number(5)]
        for idx in literals[1:]:
            if not isinstance(module, Dict):
                raise ImportError(errmsg)
            module = module.value[Number(idx)]
        return module

    # Search files
    filepath = search_file_from_literal(literals)
    if filepath is None:
        raise ImportError(errmsg)
    module = yield from load_from_path(filepath)
    return module


def search_file_from_literal(literals, location='.'):
    if not literals:
        if not os.path.isfile(location):
            return None  # TODO: Dict?
        return location

    results = []
    cur, *sub = literals
    for entry in os.listdir(location):
        if not matches_literal(entry, cur):
            continue
        search_path = os.path.join(location, entry)
        result = search_file_from_literal(sub, search_path)
        if result:
            results.append(result)

    if len(results) > 1:  # maybe filter by extension?
        raise RuntimeError('Multiple files matched literal sequence '
                           '{} at {}'.format(literals, location))
    return results[0] if results else None


def matches_literal(string, literal):
    string = parse.normalize(string)
    try:
        parsed_literal = parse.parse_number(string)
    except:
        return False
    return literal == parsed_literal


def is_literal_expr(expr):
    return isinstance(expr, Expr) and isinstance(expr.expr, Literal)


def construct_builtin_module(keys, data):
    _key = Number(parse.parse_number(keys[-1]))
    if isinstance(data, dict):
        _value = Dict(dict(construct_builtin_module(
            keys + [k], data[k]) for k in data))
    else:
        _value = BuiltinModule(data, keys)
    return _key, _value


def build_tbl(proc_functional):
    def _register_builtin_module(name):
        module = __import__('pbhhg_py.modules.' + name, fromlist=[name])
        _key, data = module.build_tbl(proc_functional)
        return construct_builtin_module([_key], data)

    def _import(argv):
        check.check_min_arity(argv, 1)
        if all(is_literal_expr(arg) for arg in argv):
            literals = [arg.expr.value for arg in argv]
            module = yield from load_from_literal(literals)
            return module

        check.check_arity(argv, 1)
        filepath = yield argv[0]
        check.check_type(filepath, String)
        module = yield from load_from_path(filepath.value)
        return module

    BUITLIN_MODULE_REGISTRY.update(
        _register_builtin_module(name)
        for name in modules.__all__
    )

    return {
        'ㅂ': _import,  # 불러오기
    }
