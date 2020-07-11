import workingMemory as wm

import random
import time
from multiprocessing import Pool
import statistics

from simulator import Simulator
from nBackTest import nBackTest

from config_atypical import *
from config_typical import *

intervalTime = 2
num_tests = 1000

class AgentSimulation:
    def __init__(self, config):
        self.retention = random.randrange(config["minRetention"], config["maxRetention"])
        self.connectionStrength = random.randrange(config["minConnStrength"], config["maxConnStrength"])
        self.percentConnection = config["minPercentConnection"] + random.random() * (config["maxPercentConnection"] - config["minPercentConnection"])
        self.memorySlots = random.randrange(config["minMemorySlots"], config["maxMemorySlots"])
        self.n = config["n"]

    def run(self):
        starting_time = time.time()
        self.simulation()
        #singleRun()
        #debugNBack()
        print("total runtime: %s" % (time.time() - starting_time))

    def simulation(self):
        start_time = time.time()
#    for numNodes in range(2, 9):
#        for maxDelayTime in range(1, 18, 2):
#            for n in range(1, 4):
#                #print("\t\tedges: ", createEdgeThreshold)
#                print(createEdgeThreshold, numNodes, maxDelayTime, n)
#                for edgeWeightMax in range(1, 32, 5):


        config = { "numNodes"           : self.memorySlots,
                   "maxDelayTime"       : self.retention,
                   "createEdgeThreshold": self.percentConnection,
                   "edgeWeightMax"      : self.connectionStrength
                  }

        nback = nBackTest(self.n, intervalTime = intervalTime, config = config)
        result = nback.test(draw = True) / nback.inputSize * 100
        print(result)

        print("total process time: %s" % (time.time() - start_time))

a = AgentSimulation(config_atypical)
a.run()
