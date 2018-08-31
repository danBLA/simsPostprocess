import os
import numpy as np
from collections import deque
from sim import Simulation
import sim
import matplotlib.pyplot as plt
import winglet_visualize as wv


#filenames = ["data/forces_original_mod.log"]
forces_folder = os.path.join(os.getenv("HOME"), "Dropbox/forcesWinglets/Mon_Aug_27_17.59.54_CEST_2018/")
filenames = [os.path.join(forces_folder,filename) for filename in os.listdir(forces_folder)]

linesPerSim = np.uint8(8)

simulations = []
simulation_dict = {}

for filename in filenames:
    with open(filename,'r') as fp:
        nlines = np.uint32(0)
        nsims = np.uint16(0)

        stack = deque(maxlen=int(linesPerSim))
        for line in fp:
            stack.append(line)

            nlines += 1

            if stack[0].startswith("SolidFile"):
                nsims += 1
                isim = Simulation(stack)
                #print("\n%s"%isim)
                simulations.append(isim)
                try:
                    simulation_dict[isim.solidgroup].append(isim)
                except KeyError:
                    simulation_dict[isim.solidgroup] = [isim]
                stack.clear()

        #print("File %s has %u lines" % (filename, nlines))
        print("File %s has %u simulations" % (filename, nsims))

set_solids = list(set(isim.solidgroup for isim in simulations))
set_yrot = list(sorted(set(isim.yrot for isim in simulations)))
set_zrot = list(set(isim.zrot for isim in simulations))

print(set_solids)
print(set_yrot)
print(set_zrot)



# create some dicts for plot mappings

zrot_solids_dict = sim.create_forcesDict_zrot_solid(set_zrot, set_solids, simulation_dict)


#wv.plot_lift(simulation_dict,set_zrot,set_solids,zrot_solids_dict)
#wv.plot_lift_winglet_proto_EM18(simulation_dict, set_zrot, set_solids, zrot_solids_dict)

sim.create_forces_derivative('lift', 'fz', set_zrot, set_solids, zrot_solids_dict)
