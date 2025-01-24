# -*- coding: utf-8 -*-
from typing import List

from functools import singledispatch
from typing import Any
from functools import total_ordering

# Decorators that checks arguments
def intCheck(f):
    def _wrapper(self, *args, **keywords):
        # if not all([ isinstance(i,int) or i.get_type() == int for i in args]):
        if not all([ isInt(i) for i in args]):
            class_name = f.__qualname__.split('.')[0]
            # class_name = self.__class__.__name__
            args_str = ",".join([f"{i}" for i in args])
            raise ValueError(f"{class_name}: type error: {class_name}({args_str})")
        # WRITE conversion n:int into Integer(n)
        v = f(self, *args, **keywords)
        return v
    return _wrapper

def boolCheck(f):
    def _wrapper(self, *args, **keywords):
        if not all([ i.get_type() == bool for i in args]):
            class_name = f.__qualname__.split('.')[0]
            args_str = ",".join([f"{i}" for i in args])
            raise ValueError(f"{class_name}: type error: {class_name}({args_str})")
        v = f(self, *args, **keywords)
        return v
    return _wrapper

def isBool(x):
    res = type(x) == bool or (isinstance(x,Expr) and x.get_type() == bool)
    return res
def isInt(x):
    res = type(x) == int or (isinstance(x,Expr) and x.get_type() == int)
    return res

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
    @boolCheck
    def __init__(self, arg: Constraint):
        self.arg = arg

    def get_arg(self) -> Constraint:
        return self.arg

    def __str__(self):
        return _c("not", self.arg)


class And(Constraint):
    @boolCheck
    def __init__(self, *args: Constraint):
        self.args = args

    def get_args(self) -> List[Constraint]:
        return self.args

    def __str__(self):
        return _c("and", *self.args)


class Or(Constraint):
    @boolCheck
    def __init__(self, *args: Constraint):
        self.args = args

    def get_args(self) -> List[Constraint]:
        return self.args

    def __str__(self):
        return _c("or", *self.args)


class Imp(Constraint):
    @boolCheck
    def __init__(self, arg1: Constraint, arg2: Constraint):
        self.args = [arg1, arg2]

    def get_args(self) -> [Constraint]:
        return self.args

    def __str__(self):
        return _c("=>", *self.args)


class Xor(Constraint):
    @boolCheck
    def __init__(self, arg1: Constraint, arg2: Constraint):
        self.args = [arg1, arg2]

    def get_args(self) -> [Constraint]:
        return self.args

    def __str__(self):
        return _c("xor", *self.args)


class Iff(Constraint):
    @boolCheck
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

    def get_lb(self) -> int:
        pass

    def get_ub(self) -> int:
        pass

    def __neg__(self, other):
        return Neg(self, other)

    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __mod__(self, other):
        return Mod(self, other)

    # def max(self,x):
    #     pass
    # def min(self,x):
    #     pass

    def __eq__(self, other):
        return Eq(self, other)

    def __ne__(self, other):
        return Ne(self, other)

    def __le__(self, other):
        return Le(self, other)

    def __ge__(self, other):
        return Ge(self, other)

    def __lt__(self, other):
        return Lt(self, other)

    def __gt__(self, other):
        return Gt(self, other)

    def value(self, solution):
        pass


@total_ordering
class Var(Term):
    def __init__(self, name, *is_):
        self.name = name
        self.is_ = is_
        self.str = name + " " + " ".join(is_)
        self.aux = False
        self.dom = None

    def __call__(self, *is1: Any):
        if any(isinstance(i, Expr) for i in is1):
            raise ValueError("Var: Expr cannot be used as an index")
        v = Var(self.name, *self.is_, *map(str, is1))
        v.aux = self.aux
        return v

    # def __lt__(self, other):
    #     if len(self.is_) != len(other.is_):
    #         return len(self.is_).__lt__(len(other.is_))
    #     else:
    #         return str(self).__lt__(str(other))
    #
    # def __eq__(self, other):
    #     if isinstance(other, Var):
    #         return self.name == other.name and self.is_ == other.is_
    #     else:
    #         return False

    def compare(self, other):
        if isinstance(other, Var):
            return self.name == other.name and self.is_ == other.is_
        else:
            return False


    def variables(self):
        yield self

    def value(self, solution):
        return solution.intValues[self]

    def __str__(self):
        if len(self.is_) == 0:
            return self.name
        else:
            return f"{self.name}({','.join(self.is_)})"

    def __hash__(self):
        return hash((self.name, self.is_))


    def get_name(self) -> str:
        return self.__str__()

    def is_symbol(self):
        return True

    def get_lb(self) -> int:
        return self.dom.lb()

    def get_ub(self) -> int:
        return self.dom.ub()


@total_ordering
class Integer(Term):
    def __init__(self, value: int):
        self.value = value

    def get_value(self) -> int:
        return self.value

    def get_lb(self) -> int:
        return self.value

    def get_ub(self) -> int:
        return self.value

    @classmethod
    def is_constant(cls):
        return True

    def __lt__(self, other) -> bool:
        return self.value.__lt__(other.value)

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, Integer):
            return self.value == other.value
        else:
            return False

class Abs(Term):
    @intCheck
    def __init__(self, arg: Term):
        # if arg.get_type() != int:
        #     class_name = self.__class__.__name__
        #     raise ValueError(f"{class_name}: type error: {class_name}({arg})")
        self.arg = arg

    def get_arg(self) -> Term:
        return self.arg

    def get_lb(self) -> int:
        if self.arg.get_ub() >= 0 and self.arg.get_lb() <= 0:
            return 0
        else:
            return min(abs(self.arg.get_lb()), abs(self.arg.get_ub()))

    def get_ub(self) -> int:
        return max(abs(self.arg.get_lb()), abs(self.arg.get_ub()))

    def __str__(self) -> str:
        return _c("abs", self.arg)


class Neg(Term):
    @intCheck
    def __init__(self, arg: Term):
        self.arg = arg

    def get_arg(self) -> Term:
        return self.arg

    def get_lb(self) -> int:
        return self.arg.get_ub() * -1

    def get_ub(self) -> int:
        return self.arg.get_lb() * -1

    def __str__(self) -> str:
        return _c("neg", self.arg)

class Add(Term):
    @intCheck
    def __init__(self, *args: List[Term]):
        self.args = args

    def get_args(self) -> Term:
        return self.args

    def get_lb(self) -> int:
        v = 0
        for a in self.args:
            v += a.get_lb()
        return v

    def get_ub(self) -> int:
        v = 0
        for a in self.args:
            v += a.get_ub()
        return v

    def __str__(self) -> str:
        return _c("+", *self.args)


class Sub(Term):
    # (- x y z)  ; means x-y-z
    @intCheck
    def __init__(self, arg, *args: List[Term]):
        self.args = [arg] + [i for i in args]

    def get_args(self) -> Term:
        return self.args

    def get_lb(self) -> int:
        v = self.args[0].get_lb()
        for a in self.args[1:]:
            v -= a.get_ub()
        return v

    def get_ub(self) -> int:
        v = self.args[0].get_ub()
        for a in self.args[1:]:
            v -= a.get_lb()
        return v

    def __str__(self) -> str:
        return _c("-", *self.args)


class Mul(Term):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def get_lb(self) -> int:
        return min(self.args[0].get_lb() * self.args[1].get_lb(),
                   self.args[0].get_lb() * self.args[1].get_ub(),
                   self.args[0].get_ub() * self.args[1].get_lb(),
                   self.args[0].get_ub() * self.args[1].get_ub())

    def get_ub(self) -> int:
        return max(self.args[0].get_lb() * self.args[1].get_lb(),
                   self.args[0].get_lb() * self.args[1].get_ub(),
                   self.args[0].get_ub() * self.args[1].get_lb(),
                   self.args[0].get_ub() * self.args[1].get_ub())

    def __str__(self) -> str:
        return _c("*", *self.args)


class Div(Term):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def get_lb(self) -> int:
        return min(self.args[0].get_lb() // self.args[1].get_lb(),
                   self.args[0].get_lb() // self.args[1].get_ub(),
                   self.args[0].get_ub() // self.args[1].get_lb(),
                   self.args[0].get_ub() // self.args[1].get_ub())

    def get_ub(self) -> int:
        return max(self.args[0].get_lb() // self.args[1].get_lb(),
                   self.args[0].get_lb() // self.args[1].get_ub(),
                   self.args[0].get_ub() // self.args[1].get_lb(),
                   self.args[0].get_ub() // self.args[1].get_ub())

    def __str__(self) -> str:
        return _c("/", *self.args)


class Mod(Term):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def get_lb(self) -> int:
        return min(self.args[0].get_lb() % self.args[1].get_lb(),
                   self.args[0].get_lb() % self.args[1].get_ub(),
                   self.args[0].get_ub() % self.args[1].get_lb(),
                   self.args[0].get_ub() % self.args[1].get_ub())

    def get_ub(self) -> int:
        return max(self.args[0].get_lb() % self.args[1].get_lb(),
                   self.args[0].get_lb() % self.args[1].get_ub(),
                   self.args[0].get_ub() % self.args[1].get_lb(),
                   self.args[0].get_ub() % self.args[1].get_ub())

    def __str__(self) -> str:
        return _c("%", *self.args)

# Pow is not supported by Sugar
# class Pow(Term):
#     def __init__(self, arg1: Term, arg2: Term):
#         self.args = [arg1, arg2]
#
#     def get_args(self) -> [Term]:
#         return self.args
#
#     def get_lb(self):
#         pass
#
#     def get_ub(self):
#         pass
#
#     def __str__(self) -> str:
#         return _c("pow", *self.args)


class Min(Term):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def get_lb(self) -> int:
        return min(self.args[0].get_lb(), self.args[1].get_lb())

    def get_ub(self) -> int:
        return max(self.args[0].get_ub(), self.args[1].get_ub())

    def __str__(self) -> str:
        return _c("min", *self.args)


class Max(Term):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def get_lb(self) -> int:
        return min(self.args[0].get_lb(), self.args[1].get_lb())

    def get_ub(self) -> int:
        return max(self.args[0].get_ub(), self.args[1].get_ub())

    def __str__(self) -> str:
        return _c("max", *self.args)


class Ite(Term,Constraint):
    def __init__(self, arg1, arg2: Term, arg3: Term):
        if not isBool(arg1) or arg2.get_type() != arg3.get_type():
            class_name = self.__class__.__name__
            raise ValueError(f"{class_name}: type error: {class_name}({arg1}, {arg2}, {arg3})")
        self.args = [arg1, arg2, arg3]

    def get_args(self):
        return self.args

    def get_type(self):
        return self.args[1].get_type()

    def get_lb(self) -> int:
        if self.get_type() != int:
            raise ValueError(f"get_lb used for Boolean: Ite({self.args[0]}, {self.args[1]}, {self.args[2]})")
        return min(self.args[1].get_lb(), self.args[2].get_lb())

    def get_ub(self) -> int:
        if self.get_type() != int:
            raise ValueError(f"get_ub used for Boolean: Ite({self.args[0]}, {self.args[1]}, {self.args[2]})")
        return max(self.args[1].get_ub(), self.args[2].get_ub())

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

    def __hash__(self):
        return hash(True)

    def __eq__(self, other):
        return True if isinstance(other, TRUE) else False


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

    def __hash__(self):
        return hash(False)

    def __eq__(self, other):
        return True if isinstance(other, FALSE) else False



class Bool(Constraint):
    def __init__(self, name, *is_):
        self.name = name
        self.is_ = is_
        self.str = name + " " + " ".join(is_)
        self.aux = False

    def __call__(self, *is1: Any):
        if any(isinstance(i, Expr) for i in is1):
            raise ValueError("Bool: Expr cannot be used as an index")
        p = Bool(self.name, *self.is_, *map(str, is1))
        p.aux = self.aux
        return p

    def variables(self):
        yield self

    def value(self, solution):
        return solution.boolValues[self]

    def __str__(self):
        if len(self.is_) == 0:
            return self.name
        else:
            return f"{self.name}({','.join(self.is_)})"

    def __hash__(self):
        return hash((self.name, self.is_))

    def __eq__(self, other):
        if isinstance(other, Var):
            return self.name == other.name and self.is_ == other.is_
        else:
            return False

    def get_name(self) -> str:#
        return self.__str__()

    def is_symbol(self):#
        return True


class Eq(AtomicFormula):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def __str__(self) -> str:
        return _c("=", *self.args)


class Ne(AtomicFormula):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def __str__(self) -> str:
        return _c("!=", *self.args)


class Le(AtomicFormula):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def __str__(self) -> str:
        return _c("<=", *self.args)


class Lt(AtomicFormula):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def __str__(self) -> str:
        return _c("<", *self.args)


class Ge(AtomicFormula):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def __str__(self) -> str:
        return _c(">=", *self.args)


class Gt(AtomicFormula):
    @intCheck
    def __init__(self, arg1: Term, arg2: Term):
        self.args = [arg1, arg2]

    def get_args(self) -> List[Term]:
        return self.args

    def __str__(self) -> str:
        return _c(">", *self.args)


class Alldifferent(Constraint):
    @intCheck
    def __init__(self, *args: Term):
        self.args = args

    def get_args(self) -> List[Term]:
        return self.args

    def __str__(self):
        return _c("alldifferent", *self.args)


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
    def __init__(self, lo: int, hi: int):
        try:
            if lo > hi:
                raise ValueError(f"IntervalDomain: {lo} > {hi}")
        except ValueError as e:
            print(e)
        self.lo = lo
        self.hi = hi

    def lb(self) -> int:
        return self.lo

    def ub(self) -> int:
        return self.hi

    def contains(self, a):
        return self.lo <= a and a <= self.hi

    def __str__(self):
        return f"{self.lo} {self.hi}"

    def __name__(self):
        return "Domain"


class SetDomain(AbstractDomain):
    def __init__(self, values):
        if not values:
            raise ValueError("Empty list: The input list must not be empty.")
        self.values = list(set(values))

    def lb(self):
        try:
            return min(self.values)
        except Exception as e:
            print(f"lb: {self} is not comparable")

    def ub(self):
        try:
            return max(self.values)
        except Exception as e:
            print(f"lb: {self} is not comparable")

    def contains(self, a):
        return self.values.contains(a)

    def get_values(self):
        return self.values

    def __str__(self):
        if len(self.values) == 1:
            return f"{self.values[0]}"
        return _c(*self.values)

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

    def int(self, x: Var, d):
        for y in self._variablesSet:
            if (x.compare(y)):
                raise ValueError(f"int: duplicate int declaration of {x}")
        if type(d.lb()) != int:
            raise ValueError(f"int: Domain type {type(d.lb())} is not int")
        self._variablesSet.append(x)
        self.variables.append(x)
        self.dom[x] = d
        x.dom = d
        return x

    def boolInt(self, x):
        return self.int(x, Domain(0, 1))

    def bool(self, p: Bool):
        if p in self._boolsSet:
            raise ValueError(f"bool: duplicate bool declaration of {p}")
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

    # def satisfiedBy(self, solution):
    #     pass

    def output(self):
        sb = ""
        for x in self.variables:
            if isinstance(self.dom[x], IntervalDomain):
                sb += f"(int {x} {self.dom[x].lo} {self.dom[x].hi})\n"
            elif isinstance(self.dom[x], SetDomain):
                sb += f"(int {x} {self.dom[x]})\n"
        for p in self.bools:
            sb += f"(bool {p})\n"
        for c in self.constraints:
            sb += f"{c}\n"
        if self.isMinimize():
            sb += f"(objective minimize {self.objective})\n"
        elif self.isMaximize():
            sb += f"(objective maximize {self.objective})\n"
        return sb

