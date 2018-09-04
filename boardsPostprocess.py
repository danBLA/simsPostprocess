import os
import numpy as np
from collections import deque
from sim import Simulation
import sim
import simconfig as sc
import shutil
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


#wv.plot_sideforce_all(set_zrot,set_solids,zrot_solids_dict)
#wv.plot_lift(simulation_dict,set_zrot,set_solids,zrot_solids_dict)
#wv.plot_lift_winglet_proto_EM18(simulation_dict, set_zrot, set_solids, zrot_solids_dict)

#wv.plot_derivative_lift_all(set_zrot, set_solids, zrot_solids_dict)
#wv.plot_derivative_sideforce_all(set_zrot, set_solids, zrot_solids_dict)

#wv.plot_yaw_derivative_lift_all(set_zrot, set_solids, zrot_solids_dict)
#wv.plot_dragforceratio_all(set_zrot, set_solids, zrot_solids_dict)

target_solid = "winglet_proto_EM18"
assert target_solid in set_solids

sim.create_forces_derivative('yrot', 'fy', set_zrot, set_solids, zrot_solids_dict)
sim.create_forces_derivative('yrot', 'fz', set_zrot, set_solids, zrot_solids_dict)
sim.create_forces_zrot_derivative('fy', set_zrot, set_solids, zrot_solids_dict)

newsims = sc.NewSimManager()

for zrot in set_zrot:
    refobj = zrot_solids_dict[zrot][target_solid]
    refarrayfx = refobj['fx']
    refarrayfy = refobj['fy']
    refarrayfz = refobj['fz']
    refarrayy = refobj['yrot']
    for reffx,reffy,reffz,refy in zip(refarrayfx, refarrayfy, refarrayfz,refarrayy):
        print("%s: fx=%.1f, fy=%.1f, fz=%.1f, rotY:%.1f, rotZ:%.1f" % (target_solid, reffx,reffy,reffz,refy,zrot))
        for solid in [s for s in set_solids if s != target_solid]:
            obj0 = zrot_solids_dict[set_zrot[0]][solid]
            obj1 = zrot_solids_dict[set_zrot[1]][solid]
            array0fx = obj0['fx']
            array0fy = obj0['fy']
            array0fz = obj0['fz']
            array0y  = obj0['yrot']
            array0z  = np.full(len(array0fx), set_zrot[0])
            array1fx = obj1['fx']
            array1fy = obj1['fy']
            array1fz = obj1['fz']
            array1y  = obj1['yrot']
            array1z  = np.full(len(array1fx), set_zrot[1])
            arrayfx  = np.concatenate((array0fx, array1fx))
            arrayfy  = np.concatenate((array0fy, array1fy))
            arrayfz  = np.concatenate((array0fz, array1fz))
            arrayz   = np.concatenate((array0z, array1z))
            arrayy   = np.concatenate((array0y, array1y))

            delta_fy = np.subtract(arrayfy, np.full(len(arrayfy), reffy))
            delta_fz = np.subtract(arrayfz, np.full(len(arrayfz), reffz))
            distance = np.sqrt(np.add(np.square(delta_fy), np.square(delta_fz)))
            i = np.argmin(distance)
            j = i % len(array0y)
            if i == len(arrayfy)-1 or i == len(array0fy) - 1:
                #print("at uppermost limit, set one below")
                i -= 1
                j -= 1
            if j > 0:
                # not at lower limit
                if min(arrayfy[j],arrayfy[j-1]) <= reffy and max(arrayfy[j],arrayfy[j-1]) >= reffy:
                    #print("set lower")
                    i -= 1
                    j -= 1
                else:
                    #print("use current")
                    pass
            else:
                #print("use lowest limit")
                pass
            #print("  -> %s: i=%u, mod(i)=%u, d=%f" % (solid, i, j, distance[i]))
            dfzdyrot0 = obj0['DfzDyrot']
            dfzdyrot0 = np.concatenate((dfzdyrot0,[dfzdyrot0[-1]]))
            dfydzrot0 = obj0['DfyDzrot']
            dfzdyrot1 = obj1['DfzDyrot']
            dfzdyrot1 = np.concatenate((dfzdyrot1,[dfzdyrot1[-1]]))
            dfydzrot1 = obj1['DfyDzrot']
            dfzdyrot = np.concatenate((dfzdyrot0, dfzdyrot1))
            dfydzrot = np.concatenate((dfydzrot0, dfydzrot1))

            start_y = arrayy[i]
            if i == j:
                start_z = set_zrot[0]
            else:
                start_z = set_zrot[1]

            dfydz = dfydzrot[i]
            dfzdy = dfzdyrot[i]

            fy = arrayfy[i]
            fz = arrayfz[i]

            new_y = (reffz - fz)/dfzdy + start_y
            new_z = (reffy - fy)/dfydz + start_z

            #print("       -> start: y=%.1f, z=%.1f, dfydz=%.1f, dfzdy=%.1f, fy=%.1f, fz=%.1f"%(start_y,start_z,dfydz,dfzdy,fy,fz))
            print("  -> %s: fy=%.1f, fz=(%.1f:%.1f), rotY=%.1f, rotZ=%.1f" % (solid, arrayfy[i], arrayfz[i], arrayfz[i+1], new_y, new_z))
            newsims[solid].add_config(0, new_y, new_z, 18.0)

print("\n")
print(newsims)
print("\n")
newsimsdir = "newsims"
if os.path.exists(newsimsdir):
    shutil.rmtree(newsimsdir)
newsims.write(prefix=newsimsdir)
