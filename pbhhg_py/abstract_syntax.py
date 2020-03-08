from collections import namedtuple
from math import isclose, isfinite

# AST
Literal = namedtuple('Literal', 'value')  # integer
FunRef = namedtuple('FunRef', 'rel')  # integer
ArgRef = namedtuple('ArgRef', 'relA relF')  # relF integer
FunDef = namedtuple('FunDef', 'body')
FunCall = namedtuple('FunCall', 'fun argv')

# Env
Env = namedtuple('Env', 'funs args')

# Values
Integer = namedtuple('Integer', 'value')
Float = namedtuple('Float', 'value')
Boolean = namedtuple('Boolean', 'value')
List = namedtuple('List', 'value')
String = namedtuple('String', 'value')
Bytes = namedtuple('Bytes', 'value')
IO = namedtuple('IO', 'inst argv')
Nil = namedtuple('Nil', '')


def _to_int_if_possible(num):
    if isfinite(num) and isclose(num, int(num), abs_tol=1e-16):
        return int(num)
    return num


class Complex(namedtuple('Complex', 'value')):
    def __str__(self):
        re = _to_int_if_possible(self.value.real)
        im = _to_int_if_possible(self.value.imag)
        re_str = str(re) + ('' if im < 0 else '+')
        minus_str = '-' if im < 0 else ''
        im_str = '' if abs(im) == 1 else str(abs(im))
        return '{}{}{}i'.format(re_str if re else '', minus_str, im_str)


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
        return Expr(self.body, new_env, [])
        yield


Expr = namedtuple('Expr', 'expr env cache_box')

# Collection
Real = (Integer, Float)
Number = (Real, Complex)
Sequence = (List, String, Bytes)
Callable = (Function, Boolean, Sequence, Dict, Complex)
Any = (Number, Callable, IO, Nil)
