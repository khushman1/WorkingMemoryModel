import workingMemory as wm
import drawGraph as dg

from simulator import *

s = Simulator(config, 5)
drawer = dg.DrawGraph(s.memory)


s.addMemoryElement("pineapple")
s.addMemoryElement(534)
s.addMemoryElement("Jack and Jill")
s.addMemoryElement("tumbling")
s.addMemoryElement("tumbling")
s.addMemoryElement("tumbling")
s.addEvent(0.1, drawer.drawMemory, 0)
s.run(1)
s.addEvent(1.1, drawer.drawMemory, 1)
s.addEvent(4.6, drawer.updateMemory, s.memory)
s.addEvent(4.9, drawer.drawMemory, 5)
s.run(5)
s.addEvent(14.9, drawer.updateMemory, s.memory)
s.addEvent(15, drawer.drawMemory, 15)
s.run(15.1)