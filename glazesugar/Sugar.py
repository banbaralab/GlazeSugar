#!/usr/bin/env python3


import logging
import subprocess
import tempfile
import re
from . import CSP
from .Solver import Solution, Timer, TIMERCOUNT, AbstractSolver


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

    def run(self, satFileName:str, outFileName:str, logFileName:str, solver):
        pass

    def runProcess(self, args, logger, solver):
        # process = subprocess.run([self.command] + self.opts)
        process = subprocess.Popen([self.command] + self.opts, stdout=subprocess.PIPE)
        with open(logger, "w") as f:
            for l in process.stdout:
                l = l.decode('utf-8').strip()
                f.write(l + '\n')
        # todo logger
        # process.kill
        rc = process.returncode
        return rc

    def __str__(self):
        return self.command


class SatSolver1(AbstractSatSolver):
    def run(self, satFileName, outFileName, logFileName, solver):
        # todo
        # val outFile = new java.io.File(outFileName)
        # outFile.delete
        # val logger = ProcessLogger(outFile)
        logger = outFileName
        self.runProcess(self.opts.append(satFileName), logger, solver)


Kissat = SatSolver1("kissat", [])

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
        # memo: Coprisでは伝播を行いUNSATならば処理を行わないといったように分岐させているが，
        # memo: 今回は単位伝播なしでCSPのSAT符号化とMapファイルの出力のみを行う
        # todo: 単位伝播処理
        # cspファイル作成
        with open(self.cspFileName, "w") as f:
            for i in self.csp.variables:
                f.write(f"(int {i} {self.csp.dom[i]})\n")
            for i in self.csp.bools:
                f.write(f"(bool {i})\n")
            for i in self.csp.constraints:
                f.write(f"{i}\n")
        p = subprocess.Popen(["sugar", "-sat", self.satFileName, "-map", self.mapFileName, "-n", self.cspFileName], stdout=subprocess.PIPE)
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
        p = subprocess.Popen(["java", "-jar", "/usr/local/lib/sugar/sugar-2.3.4.jar", "-decode", outFileName, self.mapFileName], stdout=subprocess.PIPE)
        intValues = {}
        boolValues = {}
        for l in p.stdout:
            l = l.decode('utf-8').strip()
            i = re.match(r"^a\s+(\w+)\s+(\d+)", l)
            if i is not None:
                intValues[i.group(1)] = int(i.group(2))
            t = re.match(r"^a\s+(\w+)\s+true", l)
            if t is not None:
                intValues[t.group(1)] = "true"
            f = re.match(r"^a\s+(\w+)\s+false", l)
            if f is not None:
                intValues[f.group(1)] = "false"
        if intValues=={} and boolValues=={}:
            return None
        return Solution(intValues, boolValues)



class Solver(AbstractSolver):
    def __init__(self, csp, satSolver=Kissat):
        super().__init__(csp)
        # self.csp = csp
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
        self.solution = None
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
        self.satFileName = fileName("sat",".cnf")
        self.mapFileName = fileName("map",".map")
        self.outFileName = fileName("out",".out")
        self.logFileName = fileName("log",".log")
        self.cspFileName = fileName("csp",".csp")
        # todo javaSugar.SugarMain.init()
        self.encoder = Encoder(self.csp, Solver, self.satFileName, self.mapFileName, self.cspFileName)
        self.encoder.init()
        self.solution = None
        self.initial = True
        # self.addSolverInfo("solver", self.solverName)
        # self.addSolverInfo("satSolver", self.satSolver.__str__())
        self.addSolverInfo("satFile", self.satFileName)

    def encode(self):
        # todo measureTime
        # print("encode")
        return self.encoder.encode()


    def encodeDelta(self):
        # todo measureTime
        self.encoder.encodeDelta()

    def addDelta(self):
        self.encodeDelta()

    def satSolve(self):
        # print("satSolve")
        # self.addSolverStat("sat", "variables", self.encoder.encoder.getSatVariablesCount)
        # self.addSolverStat("sat", "clauses", self.encoder.encoder.getSatClausesCount)
        # self.addSolverStat("sat", "size", self.encoder.encoder.getSatFileSize)
        # todo measureTime("time", "find")
        self.satSolver.run(self.satFileName, self.outFileName, self.logFileName, self)
        # todo measureTime("time", "decode")
        sat = self.encoder.decode(self.outFileName)
        if sat is None:
            self.solution = None
            return False
        else:
            self.solution = sat
            return True

    def commit(self):
        self.encoder.commit()

    def cancel(self):
        self.encoder.cancel()

    def find(self, commitFlag=True):
        self.commitFlag = commitFlag
        return super().find()

    def findBody(self):
        # print("findBody")
        if self.initial:
            self.initial = False
            result = self.encode() and self.satSolve()
        else:
            self.encodeDelta()
            result = self.satSolve()
        if self.commitFlag:
            self.csp.commit()
            self.commit()
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
