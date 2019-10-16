from collections import namedtuple

# AST
Literal = namedtuple('Literal', 'value')  # integer
FunRef = namedtuple('FunRef', 'rel')  # integer
ArgRef = namedtuple('ArgRef', 'relA relF')  # relF integer
FunDef = namedtuple('FunDef', 'body')
FunCall = namedtuple('FunCall', 'fun argv')

# Env
Env = namedtuple('Env', 'funs args')

# Values
Number = namedtuple('Number', 'value')
Boolean = namedtuple('Boolean', 'value')
List = namedtuple('List', 'value')
String = namedtuple('String', 'value')
Bytes = namedtuple('Bytes', 'value')
IO = namedtuple('IO', 'inst argv')
Nil = namedtuple('Nil', '')


class Dict (namedtuple('Dict', 'value')):
    def __hash__(self):
        return hash(tuple(self.value.items()))


# Intermediate values


class Function (object):
    def __init__(self, adj=''):
        self._str = '<{}Function>'.format(adj)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return self._str


class Closure (Function):
    def __init__(self, body, env):
        self.body = body
        self.env = env
        self._str = '<Closure created at depth {}>'.format(
            len(env.args))

    def __call__(self, argv):
        canned_funs, canned_args = self.env
        new_env = Env(canned_funs, canned_args + [argv])
        return (yield Expr(self.body, new_env, []))


Expr = namedtuple('Expr', 'expr env cache_box')

# Collection
Callable = (Function, Boolean, List, Dict, String, Bytes)
Any = (Number, Callable, IO, Nil)
