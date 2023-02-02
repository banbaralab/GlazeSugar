#!/usr/bin/env python3

from Solver import *
import logging
import subprocess
import tempfile

"""
@author Shuji Kosuge
"""


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
    def __init__(self, command, opts):
        self.command = command
        self.opts = opts

    def run(self, satFileName, outFileName, logFileName, solver):
        pass

    def runProcess(self, args, logger, solver):
        # todo
        process = subprocess.run([self.command])

    def __str__(self):
        return self.command


class Kissat(AbstractSatSolver):
    # todo:
    pass


class Translator:
    def __init__(self):
        self.sugarVarNameMap = {}
        self.sugarBoolNameMap = {}

    def createSugarExpr(self, x, xs):
        # SugarExpr.create(x, xs.toArray)
        return

    def toSugarName(self, name, _is):
        pass

    @singledispatchmethod
    def toSugarName(self, x):
        pass

    @toSugarName.register
    def _(self,x :Var):
        # todo
        return self.sugarVarNameMap.getOrElse()

    @toSugarName.register
    def _(self, p :bool):
        # todo
        return self.sugarBoolNameMap.getOrElse()

    @singledispatchmethod
    def toSugar(self, x :Term):
        # todo
        pass

    @toSugar.register
    def _(self, x :Term):
        # todo
        pass

    @toSugar.register
    def _(self, c :Constraint):
        #todo
        pass

    def toSugarAny(self, a :Any):
        #todo
        pass

    def toSugarInt(self, csp, x):
        #todo
        pass

    def toSugarBool(self, csp, p):
        #todo
        pass

    @toSugar.register
    def toSugar(self, csp :CSP, outputObjective = True):
        # todo
        pass

    def toSugarDelta(self, csp):
        # todo
        pass


class Encoder:
    def __init__(self, csp, solver, satFileName, mapFileName):
        self.csp = csp
        self.solver = solver
        self.satFileName = satFileName
        self.mapFileName = mapFileName
        self.translator = Translator()
        # todo
        # var sugarCSP = new javaSugar.csp.CSP()
        # var converter = new javaSugar.converter.Converter(sugarCSP)
        # var encoder = new javaSugar.encoder.Encoder(sugarCSP)

    def init(self):
        self.translator = Translator()
        # todo
        # var sugarCSP = new javaSugar.csp.CSP()
        # var converter = new javaSugar.converter.Converter(sugarCSP)
        # var encoder = new javaSugar.encoder.Encoder(sugarCSP)

    def commit(self):
        # todo
        # memo: sugarCSPのcommit
        # memo: encoderのcommit
        pass

    def cancel(self):
        # todo
        # memo: sugarCSPのcancel
        # memo: encoderのcancel
        # memo: mapファイルの出力
        pass

    def encode(self):
        ### Translating
        expressions = self.translator.toSugar(self.csp)
        self.solver.checkTimeout()
        ### Converting
        # todo
        # javaSugar.converter.Converter.INCREMENTAL_PROPAGATION = true
        # converter.convert(expressions)
        self.solver.checkTimeout()
        expressions.clear()
        # todo
        # SugarExpr.clear
        ### Propagating
        # sugarCSP.propagate
        self.solver.checkTimeout()
        # todo
        # if (sugarCSP.isUnsatisfiable)
        #     false
        # else {
        # // println("Simplifying")
        # val simplifier = new javaSugar.converter.Simplifier(sugarCSP)
        # simplifier.simplify
        # solver.checkTimeout
        # // println("Encoding")
        # encoder.encode(satFileName, false)
        # solver.checkTimeout
        # encoder.outputMap(mapFileName)
        # // println("Done")
        # // commit
        # true
        # }

    def encodeDelta(self):
        # todo
        pass

    def decode(self):
        # todo
        pass


class Solver(AbstractSolver):
    def __init__(self, csp, satSolver=Kissat):
        self.csp = csp
        self.satSolver = satSolver
        self.solverName = "sugar"
        self.satFileName = None
        self.mapFileName = None
        self.outFileName = None
        self.logFileName = None
        self.encoder = None
        self.initial = True
        self.commitFlag = True
        self.solution = None
        self.init()

    def createTempFile(self, ext):
        # todo fileの名前
        file = tempfile.NamedTemporaryFile()
        return file

    def init(self):
        def fileName(key, ext):
            # todo
            pass
        super.init()
        self.satFileName = fileName("sat",".cnf")
        self.mapFileName = fileName("map",".map")
        self.outFileName = fileName("out",".out")
        self.logFileName = fileName("log",".log")
        # todo javaSugar.SugarMain.init()
        encoder = Encoder(self.csp, Solver, satFileName, mapFileName)
        encoder.init()
        self.solution = None
        self.initial = True
        self.addSolverInfo("solver", self.solverName)
        self.addSolverInfo("satSolver", self.satSolver.__str__())
        self.addSolverInfo("satFile", self.satFileName)

    def encode(self):
        # todo measureTime
        self.encoder.encode()

    def encodeDelta(self):
        # todo measureTime
        self.encoder.encodeDelta()

    def addDelta(self):
        self.encodeDelta()

    def satSolve(self):
        self.addSolverStat("sat", "variables", self.encoder.encoder.getSatVariablesCount)
        self.addSolverStat("sat", "clauses", self.encoder.encoder.getSatClausesCount)
        self.addSolverStat("sat", "size", self.encoder.encoder.getSatFileSize)
        # todo measureTime("time", "find")
        self.satSolver.run(self.satFileName, self.outFileName, self.logFileName, Solver)
        # todo measureTime("time", "decode")
        # todo


    def commit(self):
        self.encoder.commit()

    def cancel(self):
        self.encoder.cancel()

    def find(self, commitFlag=True):
        self.commitFlag = commitFlag
        return super.find()

    def findBody(self):
        if self.initial:
            self.initial = False
            result = self.encode() and self.satSolve()
        else:
            self.encodeDelta()
            result = self.satSolve()
        if self.commitFlag:
            self.csp.commit()
            return self.commit()
        return result

    def findNext(self, commitFlag = False):
        self.commitFlag = commitFlag
        return super.findNext()

    def findNextBody(self):
        # todo measureTime("time", "encode")
        # todo
        pass

    def findOptBody(self):
        # todo
        pass

    def findOptBoundBody(self):
        # todo
        pass

    def dumpCSP(self):
        #todo
        pass

    def dumpCNF(self):
        # todo
        pass

    def dump(self):
        # todo
        pass
