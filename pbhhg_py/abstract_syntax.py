from collections import namedtuple

# AST
Literal = namedtuple('Literal', 'value')  # integer
FunRef = namedtuple('FunRef', 'rel')  # integer
ArgRef = namedtuple('ArgRef', 'relA relF')  # relF integer
FunDef = namedtuple('FunDef', 'body')
BuiltinFun = namedtuple('BuiltinFun', 'id')  # integer
FunCall = namedtuple('FunCall', 'fun argv')

# Env
Env = namedtuple('Env', 'funs args')

# Values
Number = namedtuple('Number', 'value')
Boolean = namedtuple('Boolean', 'value')
Closure = namedtuple('Closure', 'body env')
List = namedtuple('List', 'value')
String = namedtuple('String', 'value')
IO = namedtuple('IO', 'inst argv')
Nil = namedtuple('Nil', '')

# Intermediate values
Expr = namedtuple('Expr', 'expr env cache_box')
Any = (Number, Boolean, Closure, List, String, IO, Nil)

# BuiltinModule = namedtuple('BuiltinModule', 'imported')
