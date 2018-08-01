from collections import deque
from sim import Simulation
filename = "data/forces_original_mod.log"

linesPerSim = 8

simulations = []

with open(filename,'r') as fp:
    nlines = 0
    nsims = 0

    stack = deque(maxlen=linesPerSim)
    for line in fp:
        stack.append(line)

        nlines += 1

        if stack[0].startswith("SolidFile"):
            nsims += 1
            sim = Simulation(stack)
            print("\n%s"%sim)
            simulations.append(sim)
            stack.clear()

    print("File has %u lines" % nlines)
    print("File has %u simulations" % nsims)
