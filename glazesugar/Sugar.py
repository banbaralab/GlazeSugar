#!/usr/bin/env python3


import logging
import subprocess
import tempfile
import re
from . import CSP
from .Solver import Solution, Timer, AbstractSolver, UnknownResultError
from typing import Union
import signal
import os

"""
@author Shuji Kosuge
"""

sugar_jar = os.path.expanduser("~/.sugar_solvers/prog-sugar/build/sugar-2.3.4.jar")


class AbstractSatSolverLogger:
    def __init__(self, file):
        self.file = file
        self.stat = {}

    def addStats(self, key, value):
        self.stat.update([key, value])
        return self.stat

    def parseLog(self, s):
        pass

    def out(self, s):
        logging.info(s)
        self.parseLog(s)

    def err(self, s):
        logging.error(s)
        self.parseLog(s)


class AbstractSatSolver:
    def __init__(self, command, opts=[]):
        self.command = command
        self.opts = opts

    def run(self, satFileName: str, outFileName: str, logFileName: str, solver):
        pass

    def runProcess(self, args, logger, solver):
        signal.signal(signal.SIGINT, lambda signum, frame: None)
        process = subprocess.Popen([self.command] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(logger, "w") as f:
            for l in process.stdout:
                l = l.decode('utf-8').strip()
                f.write(f'{l} \n')
            for l in process.stderr:
                l = l.decode('utf-8').strip()
                f.write(f'{l} \n')
        pass        # FileNotFoundError(2, 'No such file or directory')

    def __str__(self):
        return self.command


class SatSolver1(AbstractSatSolver):
    def run(self, satFileName, outFileName, logFileName, solver):
        logger = outFileName
        self.runProcess(self.opts + [satFileName], logger, solver)


Kissat = SatSolver1("kissat")
Glueminisat_core = SatSolver1("glueminisat-core", ["-model"])

DefaultSolver = Kissat


# class Kissat(AbstractSatSolver):
#     def __init__(self):


# class Translator:
#     def __init__(self):
#         self.sugarVarNameMap = {}
#         self.sugarBoolNameMap = {}
#
#     def createSugarExpr(self, x, *xs):
#         # SugarExpr.create(x, xs.toArray)
#         return
#
#     def toSugarName(self, name, s):
#         pass
#
#     # todo
#     @singledispatchmethod
#     def toSugarName(self, x):
#         pass
#
#     @toSugarName.register
#     def _(self, x):
#         # todo
#         return self.sugarVarNameMap.getOrElse()
#
#     @toSugarName.register
#     def _(self, p :bool):
#         # todo
#         return self.sugarBoolNameMap.getOrElse()
#
#     @singledispatchmethod
#     def toSugar(self, x):
#         # todo
#         pass
#
#     @toSugar.register
#     def _(self, x):
#         # todo
#         pass
#
#     @toSugar.register
#     def _(self, c ):
#         #todo
#         pass
#
#     def toSugarAny(self, a):
#         #todo
#         pass
#
#     def toSugarInt(self, csp, x):
#         #todo
#         pass
#
#     def toSugarBool(self, csp, p):
#         #todo
#         pass
#
#     @toSugar.register
#     def toSugar(self, csp, outputObjective = True):
#         # todo
#         pass
#
#     def toSugarDelta(self, csp):
#         # todo
#         pass


class Encoder:
    def __init__(self, csp: CSP, solver, satFileName, mapFileName, cspFileName):
        self.csp = csp
        self.solver = solver
        self.satFileName = satFileName
        self.mapFileName = mapFileName
        self.cspFileName = cspFileName
        # self.translator = Translator()
        # todo
        # var sugarCSP = new javaSugar.csp.CSP()
        # var converter = new javaSugar.converter.Converter(sugarCSP)
        # var encoder = new javaSugar.encoder.Encoder(sugarCSP)

    def init(self):
        # self.translator = Translator()
        # todo
        # var sugarCSP = new javaSugar.csp.CSP()
        # var converter = new javaSugar.converter.Converter(sugarCSP)
        # var encoder = new javaSugar.encoder.Encoder(sugarCSP)
        pass

    def commit(self):
        # todo
        # memo: sugarCSPのcommit
        # memo: encoderのcommit
        # sugarCSP.commit
        # if (! sugarCSP.isUnsatisfiable)
        #     encoder.commit

        pass

    def cancel(self):
        # todo
        # memo: sugarCSPのcancel
        # memo: encoderのcancel
        # memo: mapファイルの出力
        # sugarCSP.cancel
        # encoder.cancel
        # encoder.outputMap(mapFileName)

        pass

    def encode(self):
        with open(self.cspFileName, "w") as f:
            for i in self.csp.variables:
                f.write(f"(int {i} {self.csp.dom[i]})\n")
            for i in self.csp.bools:
                f.write(f"(bool {i})\n")
            for i in self.csp.constraints:
                f.write(f"{i}\n")
        p = subprocess.Popen(
            ["java", "-jar", sugar_jar, "-encode", self.cspFileName, self.satFileName, self.mapFileName],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for l in p.stdout:
            l = l.decode('utf-8').strip()
            unsat = re.match(r"^s\s+UNSATISFIABLE", l)
            if unsat is not None:
                return False
        return True

    def encodeDelta(self):
        # todo
        pass

    def decode(self, outFileName):
        p = subprocess.Popen(
            ["java", "-jar", sugar_jar, "-decode", outFileName, self.mapFileName],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        intValues = {}
        boolValues = {}
        for l in p.stdout:
            l = l.decode('utf-8').strip()
            i = re.match(r"^a\s+(\w+)\s+(\d+)", l)
            if i is not None:
                intValues[i.group(1)] = int(i.group(2))
            t = re.match(r"^a\s+(\w+)\s+true", l)
            if t is not None:
                boolValues[t.group(1)] = True
            f = re.match(r"^a\s+(\w+)\s+false", l)
            if f is not None:
                boolValues[f.group(1)] = False
            s = re.match(r"^s\s+UNKNOWN", l)
            if s is not None:
                raise UnknownResultError()
        if intValues == {} and boolValues == {}:
            return None
        return Solution(intValues, boolValues)


class Solver(AbstractSolver):
    def __init__(self, csp, satSolver=DefaultSolver):
        super().__init__(csp)
        self.satSolver = satSolver
        self.solverName = "sugar"
        self.satFileName = None
        self.mapFileName = None
        self.outFileName = None
        self.logFileName = None
        self.cspFileName = None
        self.encoder = None
        self.initial = True
        self.commitFlag = True
        self._solution = None
        self.init()

    def createTempFile(self, ext: str):
        file = tempfile.NamedTemporaryFile(prefix="sugar", suffix=ext)
        return file.name

    def init(self):
        def fileName(key, ext):
            self.options.setdefault(key, self.createTempFile(ext))
            file = self.options[key]
            return file

        super().init()
        self.satFileName = fileName("sat", ".cnf")
        self.mapFileName = fileName("map", ".map")
        self.outFileName = fileName("out", ".out")
        self.logFileName = fileName("log", ".log")
        self.cspFileName = fileName("csp", ".csp")
        self.encoder = Encoder(self.csp, Solver, self.satFileName, self.mapFileName, self.cspFileName)
        self.encoder.init()
        self._solution = None
        self.initial = True
        self.addSolverInfo("solver", self.solverName)
        # self.addSolverInfo("satSolver", self.satSolver.__str__())
        self.addSolverInfo("satFile", self.satFileName)

    def encode(self):
        with self.measureTime(self, "time", "encode"):
            return self.encoder.encode()

    def encodeDelta(self):
        with self.measureTime(self, "time", "encodeDelta"):
            self.encoder.encodeDelta()

    def addDelta(self):
        self.encodeDelta()

    def satSolve(self):
        # self.addSolverStat("sat", "variables", self.encoder.encoder.getSatVariablesCount)
        # self.addSolverStat("sat", "clauses", self.encoder.encoder.getSatClausesCount)
        # self.addSolverStat("sat", "size", self.encoder.encoder.getSatFileSize)

        with self.measureTime(self, "time", "find"):
            self.satSolver.run(self.satFileName, self.outFileName, self.logFileName, self)
        with self.measureTime(self, "time", "encode"):
            sat = self.encoder.decode(self.outFileName)
            if sat is None:
                self._solution = None
                return False
            else:
                self._solution = sat
                return True

    def commit(self):
        self.encoder.commit()

    def cancel(self):
        self.encoder.cancel()

    def find(self, commitFlag=True):
        self.commitFlag = commitFlag
        return super().find()

    def findBody(self):
        result = self.encode() and self.satSolve()
        if self.commitFlag:
            self.csp.commit()
            self.commit()
        return result

    def findNext(self, commitFlag=False):
        self.commitFlag = commitFlag
        return super().findNext()

    def findNextBody(self):
        with self.measureTime(self, "time", "encode"):
            cs1 = [CSP.Eq(x, self.solution(x)) for x in self.csp.variables if not x.aux]
            cs2 = [p if self.solution(p) else CSP.Not(p) for p in self.csp.bools if not p.aux]
            self.csp.add(CSP.Not(CSP.And(CSP.And(*cs1), CSP.And(*cs2))))
            if not self.encode():
                return False
            if self.commitFlag:
                self.csp.commit()
                self.commit()
        return self.satSolve()

    def findOptBody(self):
        v = self.csp.objective
        if v in self.csp.variables:
            lb = v.get_lb()
            ub = v.get_ub()
            self.csp.commit()
            self.commit()
            sat = self.encode() and self.satSolve()
            self.addSolverStat("result", "find", 1 if sat else 0)
            if sat:
                last_solution = self.solution()
                if self.csp.isMinimize():
                    ub = self.solution(v)
                    while lb < ub:
                        mid = (lb + ub) // 2
                        if self.findOptBound(lb, mid):
                            ub = self.solution(v)
                            last_solution = self.solution()
                        else:
                            ub = mid + 1
                else:
                    lb = self.solution(v)
                    while lb < ub:
                        mid = (lb + ub + 1) // 2
                        if self.findOptBound(mid, ub):
                            lb = self.solution(v)
                            last_solution = self.solution()
                        else:
                            ub = mid - 1
                self._solution = last_solution
                return True
            else:
                return False
        else:
            raise RuntimeError("Objective variable is not defined")

    def findOptBoundBody(self, lb, ub):
        v = self.csp.objective
        with self.measureTime(self, "time", "encode"):
            self.csp.cancel()
            self.csp.add(CSP.And(CSP.Ge(v, lb), CSP.Le(v, ub)))
            self.encode()
        return self.satSolve()

    def dumpCSP(self, filename):
        with open(filename, mode='w') as f:
            f.write(self.csp.output())

    # def dumpCNF(self):
    #     pass

    def dump(self, filename, format):
        if format == "" or format == "csp":
            self.dumpCSP(filename)
        # elif format == "cnf":
        #     self.dumpCNF(filename)

    def solution(self, *xs: Union[CSP.Var, CSP.Bool]):
        if len(xs) == 0:
            sol = {}
            sol.update(**self._solution.intValues, **self._solution.boolValues)
            return sol
        elif len(xs) == 1:
            return self._solution.value(*xs)
        else:
            sol = {}
            for x in xs:
                sol[str(x)] = self._solution.value(x)
            return sol
