# -*- coding: utf-8 -*-
from typing import List

from functools import singledispatchmethod
from functools import singledispatch

# class IntegerVariable:
#     def __init__(self, name: str, domain: List[int]):
#         self.name = name
#         self.domain = domain
#
#     def get_name(self) -> str:
#         return self.name
#
#     def get_domain(self) -> List[int]:
#         return self.domain
#
#     def __str__(self) -> str:
#         return _c("int", self.name, _c(*self.domain))
#
#
# class BooleanVariable:
#     def __init__(self, name: str):
#         self.name = name
#
#     def get_name(self) -> str:
#         return self.name
#
#     def __str__(self) -> str:
#         return _c("bool", self.name)


class Expr:

    def variables(self):
        return []

    def bools(self):
        return []


# --------------- Constraint ---------------
class Constraint(Expr):
    def __str__(self) -> str:
        raise NotImplementedError()

    @classmethod
    def get_type(cls):
        return bool

    @classmethod
    def is_symbol(cls):
        return False

    @classmethod
    def is_constant(cls):
        return False

    @classmethod
    def is_true(cls):
        return False

    @classmethod
    def is_false(cls):
        return False


class Not(Constraint):
    def __init__(self, arg: Constraint):
        self.arg = arg

    def get_arg(self) -> Constraint:
        return self.arg

    def __str__(self):
        return _c("not", self.arg)


class And(Constraint):
    def __init__(self, *args: Constraint):
        self.args = args

    def get_args(self) -> List[Constraint]:
        return self.args

    def __str__(self):
        return _c("and", *self.args)


class Or(Constraint):
    def __init__(self, *args: Constraint):
        self.args = args

    def get_args(self) -> List[Constraint]:
        return self.args

    def __str__(self):
        return _c("or", *self.args)


class Imp(Constraint):
    pass


class Xor(Constraint):
    pass


class Iff(Constraint):
    def __init__(self, arg1: Constraint, arg2: Constraint):
        self.args = [arg1, arg2]

    def get_args(self) -> [Constraint]:
        return self.args

    def __str__(self):
        return _c("iff", *self.args)


# --------------- Term ---------------

class Term(Expr):
    def __str__(self) -> str:
        raise NotImplementedError()

    @classmethod
    def get_type(cls):
        return int

    @classmethod
    def is_constant(cls):
        return False

    @classmethod
    def is_symbol(cls):
        return False

    def __neg__(self):
        return Neg(self)
    def __add__(self, other):
        return Add(self, other)
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __truediv__(self, other):
        pass
    def __mod__(self, other):
        pass
    def max(self,x):
        pass
    def min(self,x):
        pass
    def __eq__(self, other):
        pass
    def __ne__(self, other):
        pass
    def __le__(self, other):
        pass
    def __ge__(self, other):
        pass
    def __lt__(self, other):
        pass
    def __gt__(self, other):
        pass
    def value(self, solution):
        pass



class Integer(Term):
    def __init__(self, value: int):
        self.value = value

    def get_value(self) -> int:
        return self.value

    @classmethod
    def is_constant(cls):
        return True

    def __str__(self) -> str:
        return str(self.value)


class IntegerVariableName(Term):
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def is_symbol(self):
        return True

    def __str__(self) -> str:
        return self.name


class Abs(Term):
    def __init__(self, arg: Term):
        self.arg = arg

    def get_arg(self) -> Term:
        return self.arg

    def __str__(self) -> str:
        return _c("abs", self.arg)


class Neg(Term):
    pass


class Add(Term):
    def __init__(self, *args: List[Term]):
        self.args = args

    def get_args(self) -> Term:
        return self.args

    def __str__(self) -> str:
        return _c("+", *self.args)


class Sub(Term):
    pass


class Mul(Term):
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> [Term]:
        return self.args

    def __str__(self) -> str:
        return _c("*", *self.args)


class Div(Term):
    pass


class Mod(Term):
    pass


class Pow(Term):
    pass


class Min(Term):
    pass


class Max(Term):
    pass


class Ite(Term):
    def __init__(self, arg1, arg2: Term, arg3: Term):
        self.args = [arg1, arg2, arg3]

    def get_args(self):
        return self.args

    def __str__(self) -> str:
        return _c("if", *self.args)


# --------------- AtomicFormula ---------------
class AtomicFormula(Constraint):
    pass


class TRUE(AtomicFormula):
    @classmethod
    def is_constant(cls):
        return True

    @classmethod
    def get_value(cls):
        return True

    @classmethod
    def is_true(cls):
        return True

    def __str__(self):
        return "true"


class FALSE(AtomicFormula):
    @classmethod
    def is_constant(cls):
        return True

    @classmethod
    def get_value(cls):
        return False

    @classmethod
    def is_false(cls):
        return True

    def __str__(self):
        return "false"


class Boolean(AtomicFormula):
    def __init__(self, value: bool):
        self.value = value

    @classmethod
    def is_constant(cls):
        return True

    def get_value(self):
        return self.value

    def __str__(self):
        if self.value:
            return "true"
        else:
            return "false"


class BooleanVariableName(AtomicFormula):
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def is_symbol(self):
        return True

    def __str__(self) -> str:
        return self.name


class Eq(AtomicFormula):
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> [Term]:
        return self.args

    def __str__(self) -> str:
        return _c("=", *self.args)


class Ne(AtomicFormula):
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> [Term]:
        return self.args

    def __str__(self) -> str:
        return _c("!=", *self.args)


class Le(AtomicFormula):
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> [Term]:
        return self.args

    def __str__(self) -> str:
        return _c("<=", *self.args)


class Lt(AtomicFormula):
    pass


class Ge(AtomicFormula):
    pass


class Gt(AtomicFormula):
    pass


class Alldifferent(AtomicFormula):
    pass


def _c(*args):
    elems = [str(x) for x in args]
    return "(" + " ".join(elems) + ")"


# ------------------------------------------
class AbstractDomain:
    def lb(self):
        pass

    def ub(self):
        pass

    def contains(self, a):
        pass


class IntervalDomain(AbstractDomain):
    def __init__(self, lo, hi):
        try:
            if lo > hi:
                raise ValueError(f"IntervalDomain: {lo} > {hi}")
        except ValueError as e:
            print(e)
        self.lo = lo
        self.hi = hi

    def lb(self):
        return self.lo

    def ub(self):
        return self.hi

    def contains(self, a):
        return self.lo <= a and a <= self.hi

    def __str__(self):
        return f"{self.lo} {self.hi}"

    def __name__(self):
        return "Domain"


class SetDomain(AbstractDomain):
    def __init__(self, values):
        self.values = values

    def lb(self):
        return self.values.min

    def ub(self):
        return self.values.max

    def contains(self, a):
        return self.values.contains(a)

    def __name__(self):
        return "Domain"


@singledispatch
def Domain():
    pass


@Domain.register
def _(lo: int, *hi: int):
    if hi == ():
        return IntervalDomain(lo, lo)
    return IntervalDomain(lo, hi[0])


@Domain.register
def _(values: list):
    return SetDomain(values)


# todo EnumDomain


### CSP
class CSP:
    def __init__(self, variables=[], bools=[], dom={}, constraints=[]):
        self.variables = variables
        self.bools = bools
        self.dom = dom
        self.constraints = constraints
        self._variablesSet = []
        self._variablesSize = 0
        self._boolsSet = []
        self._boolsSize = 0
        self._constraintsSize = 0
        self.objective = None
        self._target = 0

    def this(self):
        # todo
        # 複製用
        pass

    def init(self):
        self.variables = []
        self.bools = []
        self.dom = {}
        self.constraints = []
        self._variablesSet = []
        self._variablesSize = 0
        self._boolsSet = []
        self._boolsSize = 0
        self._constraintsSize = 0
        self.objective = None
        self._target = 0

    def int(self, x, d):
        if x in self._variablesSet:
            raise # todo 二重登録時のエラー処理
        self._variablesSet.append(x)
        self.variables.append(x)
        self.dom[x] = d
        return x

    def boolInt(self, x):
        return self.int(x, Domain(0, 1))

    def bool(self, p):
        if p in self._boolsSet:
            raise # todo
        self._boolsSet.append(p)
        self.bools.append(p)
        return p

    def add(self, *cs):
        # todo 追加できない場合エラー処理をかく
        self.constraints = self.constraints + list(cs)

    def commit(self):
        self._variablesSize = len(self.variables)
        self._boolsSize = len(self.bools)
        self._constraintsSize = len(self.constraints)

    def cancel(self):
        self.variables = self.variables[:self._variablesSize]
        self._variablesSet = self.variables
        self.bools = self.bools[:self._boolsSize]
        self._boolsSet = self.bools
        self.constraints = self.constraints[:self._constraintsSize]

    def variablesDelta(self):
        return self.variables[self._variablesSize:]

    def boolsDelta(self):
        return self.bools[self.bools:]

    def constraintsDelta(self):
        return self.constraints[self.constraints:]

    def minimize(self, x):
        self.objective = x
        self._target = -1
        return x

    def maximize(self, x):
        self.objective = x
        self._target = 1
        return x

    def isMinimize(self):
        return self._target < 0

    def isMaximize(self):
        return self._target > 0

    def satisfiedBy(self, solution):
        # todo
        pass

    def output(self):
        sb = ""
        for x in self.variables:
            if isinstance(self.dom[x], IntervalDomain):
                sb += f"int({x},{self.dom[x].lo},{self.dom[x].hi})\n"
            elif isinstance(self.dom[x], SetDomain):
                sb += f"int({x},{self.dom[x]})\n"
        for p in self.bools:
            sb += f"bool({p})\n"
        for c in self.constraints:
            sb += f"{c}\n"
        if self.isMinimize():
            sb += f"minimize({self.objective})\n"
        elif self.isMaximize():
            sb += f"maximize({self.objective})\n"
        return sb

