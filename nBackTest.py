import workingMemory as wm
import drawGraph as dg

import random
import time
from multiprocessing import Pool
import statistics

from simulator import Simulator
#from config_typical import *

class nBackTest:

    def __init__(self, n, inputSize = 100, intervalTime = 2, config = dict()):
        self.inputSize = inputSize
        self.intervalTime = intervalTime
        self.n = n
        self.time = 0
        if config:
            self.simulator = Simulator(config)
        else:
            self.simulator = Simulator()

    def generateInput(self):
        self.testInput = [random.randint(0, 50) for _ in range(self.inputSize)]

    def test(self, draw = False):
        if draw:
            drawer = dg.DrawGraph(self.simulator.memory)
        correctCount = 0
        self.time = 0
        self.generateInput()
        check = False

        for i in range(len(self.testInput) + self.n):
            if i < len(self.testInput):
                self.simulator.addMemoryElement(self.testInput[i])
            self.simulator.run(self.time)
            if i >= self.n:
                check = self.simulator.memory.recall(self.testInput[i - self.n])
            if draw:
                drawer.updateMemory(self.simulator.memory)
                if i == 3 or i == int(len(self.testInput) / 4) or i == int(len(self.testInput) / 2) or i == int(len(self.testInput) * .75):
                    drawer.updateMemory(self.simulator.memory)
                    drawer.drawMemory(str(i))
#                check = False
#                for value in self.simulator.memory.elementSet.values():
#                    if value["value"] == self.testInput[i - self.n]:
#                        check = True
#                check = self.testInput[i - self.n] in self.simulator.memory.elementSet 
                #print("testing", self.simulator.currentTime, self.simulator.memory.elementSet, self.testInput[i - self.n], check)
                if(check):
                        correctCount += 1
            self.time += self.intervalTime
        return correctCount

def fileInit():
    f = open('results/test_results_%s.csv' % time.time(), 'w')
    f.write("n,memory slots,retention time,% connection,connection strength,accuracy,standardDeviation\n")
    return f

def singleSimulation(maxDelayTime, n = 1.5):
    print("delay: ", maxDelayTime)
    lines = []
    start_time = time.time()
    for numNodes in range(3, 9):
        print("\tnumNodes: ", numNodes)
        for createEdgeThreshold in range(1, 11, 2):
            #print("\t\tedges: ", createEdgeThreshold)
            for edgeWeightMax in range(5, 26, 5):

                config = { "numNodes"           : numNodes,
                           "maxDelayTime"       : maxDelayTime,
                           "createEdgeThreshold": createEdgeThreshold / 10,
                           "edgeWeightMax"      : edgeWeightMax
                          }

                results = []
                for _ in range(num_tests):
                    nback = nBackTest(n, intervalTime, config = config)
                    result = nback.test()
                    results.append(result / nback.inputSize * 100)

                correctness, standardDeviation = analyzeResults(results)
                line = "%d,%d,%d,%d,%d,%d,%f,%s\n" % (n, numNodes, maxDelayTime, createEdgeThreshold, edgeWeightMax, correctness, standardDeviation, results)
                lines.append(line)
    print("total process time: %s" % (time.time() - start_time))
    return lines

def allNSimulation(createEdgeThreshold):
    lines = []
    start_time = time.time()
#    for numNodes in range(2, 9):
#        for maxDelayTime in range(1, 18, 2):
#            for n in range(1, 4):
#                #print("\t\tedges: ", createEdgeThreshold)
#                print(createEdgeThreshold, numNodes, maxDelayTime, n)
#                for edgeWeightMax in range(1, 32, 5):


#    for numNodes in range(2, 6):
#        for delayTime in range(50, 95, 5):
#            for n in range(1, 4):
    for numNodes in range(5, 9):
        for delayTime in range(130, 175, 5):
            for n in range(1, 4):
                #print("\t\tedges: ", createEdgeThreshold)
                maxDelayTime = delayTime / 10
                print(createEdgeThreshold, numNodes, maxDelayTime, n)
                for edgeWeightMax in range(21, 26, 1):

                    config = { "numNodes"           : numNodes,
                               "maxDelayTime"       : maxDelayTime,
                               "createEdgeThreshold": createEdgeThreshold / 10,
                               "edgeWeightMax"      : edgeWeightMax
                              }

                    results = []
                    for _ in range(num_tests):
                        nback = nBackTest(n, intervalTime, config = config)
                        result = nback.test()



                        results.append(result / nback.inputSize * 100)

                    correctness, standardDeviation = analyzeResults(results)
                    line = "%d,%d,%f,%f,%d,%d,%f\n" % (n, numNodes, maxDelayTime, createEdgeThreshold, edgeWeightMax, correctness, standardDeviation)
                    lines.append(line)
    print("threadNo: %d, total process time: %s" % (createEdgeThreshold, (time.time() - start_time)))
    return lines

def allNSimulation2(createEdgeThreshold):
    lines = []
    start_time = time.time()
    for numNodes in range(3, 9):
        for maxDelayTime in range(5, 31, 2):
            for n in range(4):
                print(createEdgeThreshold, numNodes, maxDelayTime, n)
                #print("\t\tedges: ", createEdgeThreshold)
                for edgeWeightMax in range(5, 21, 5):

                    config = { "numNodes"           : numNodes,
                               "maxDelayTime"       : maxDelayTime,
                               "createEdgeThreshold": createEdgeThreshold / 10,
                               "edgeWeightMax"      : edgeWeightMax
                              }

                    results = []
                    for _ in range(num_tests):
                        nback = nBackTest(n, intervalTime, config = config)
                        result = nback.test()
                        results.append(result / nback.inputSize * 100)

                    correctness, standardDeviation = analyzeResults(results)
                    line = "%d,%d,%f,%d,%d,%d,%f\n" % (n, numNodes, maxDelayTime, createEdgeThreshold, edgeWeightMax, correctness, standardDeviation)
                    lines.append(line)
    print("threadNo: %d, total process time: %s" % (createEdgeThreshold, (time.time() - start_time)))
    return lines


def parallelRun():
    f = fileInit()
    # Uses processes to overcome GIL
    with Pool(4) as p:
        #for lines in p.imap(singleSimulation, range(3, 10)):
        for lines in p.imap(allNSimulation, [6, 6.5, 7, 7.5, 8, 8.5, 9]):
            for line in lines:
                f.write(line)
    f.close()

def analyzeResults(results):
    correctness = sum(results) / num_tests
    try:
        standardDeviation = statistics.stdev(results)
    except statistics.StatisticsError:
        standardDeviation = 0
    return correctness, standardDeviation
    #print("\t\tcorrectnes: ", correctness, "result", result, "%s seconds elasped." % (time.time() - start_time))


def singleRun():
    f = fileInit()
    nback = nBackTest(n, intervalTime)
    start_time = time.time()

    #create different config parameter values to tune parameter
    for numNodes in range(3,8):
        print("num: ", numNodes)
        for maxDelayTime in range(3, 10):
            print("\tdelay: ", maxDelayTime)
            for createEdgeThreshold in range(1,11):
                for edgeWeightMax in [3, 5, 7, 9, 11, 16]:

                    config = { "numNodes"           : numNodes,
                               "maxDelayTime"       : maxDelayTime,
                               "createEdgeThreshold": createEdgeThreshold / 10,
                               "edgeWeightMax"      : edgeWeightMax
                              }

                    results = []
                    for _ in range(num_tests):
                        nback.simulator.reset(config)
                        results.append(nback.test() / nback.inputSize * 100)

                    correctness, standardDeviation = analyzeResults(results)
                    line = "%d,%d,%d,%d,%d,%d,%f,%s\n" % (n, numNodes, maxDelayTime, createEdgeThreshold, edgeWeightMax, correctness, standardDeviation, results)
                    f.write(line)
            print("\ttime: %s" % (time.time() - start_time))
    f.close()

def debugNBack():
    nback = nBackTest(n, intervalTime)
    f = fileInit()
    config = { "numNodes"           : 7,
               "maxDelayTime"       : 100,
               "createEdgeThreshold": 0.999999999999,
               "edgeWeightMax"      : 25
              }

    results = []
    for _ in range(num_tests):
        nback.simulator.reset(config)
        results.append(nback.test() / nback.inputSize * 100)
    
    correctness, standardDeviation = analyzeResults(results)
    print(correctness)
    line = "%d,%d,%d,%d,%d,%d,%f,%s\n" % (n, config["numNodes"], config["maxDelayTime"], config["createEdgeThreshold"], config["edgeWeightMax"], correctness, standardDeviation, results)
    f.write(line)

def run():
    starting_time = time.time()
    parallelRun()
    #singleRun()
    #debugNBack()
    print("total runtime: %s" % (time.time() - starting_time))

#test parameters
num_tests = 1000
n = 1
intervalTime = 2

