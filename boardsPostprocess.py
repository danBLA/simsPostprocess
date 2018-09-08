import os
import numpy as np
from sim import Simulation
import sim
import simconfig as sc
import shutil
import matplotlib.pyplot as plt
import winglet_visualize as wv


#filenames = ["data/forces_original_mod.log"]
forces_folder = os.path.join(os.getenv("HOME"), "Dropbox/forcesWinglets/Mon_Aug_27_17.59.54_CEST_2018/")
filenames = [os.path.join(forces_folder, filename) for filename in os.listdir(forces_folder)]


simulation_dict, set_solids, set_yrot, set_zrot = sim.load_from_files(filenames)

# create some dicts for plot mappings

zrot_solids_dict = sim.create_forcesDict_zrot_solid(set_zrot, set_solids, simulation_dict)


#wv.plot_sideforce_all(set_zrot,set_solids,zrot_solids_dict)
#wv.plot_lift(simulation_dict,set_zrot,set_solids,zrot_solids_dict)
#wv.plot_lift_winglet_proto_EM18(simulation_dict, set_zrot, set_solids, zrot_solids_dict)

#wv.plot_derivative_lift_all(set_zrot, set_solids, zrot_solids_dict)
#wv.plot_derivative_sideforce_all(set_zrot, set_solids, zrot_solids_dict)

#wv.plot_yaw_derivative_lift_all(set_zrot, set_solids, zrot_solids_dict)
#wv.plot_dragforceratio_all(set_zrot, set_solids, zrot_solids_dict)


refsolid = "winglet_proto_EM18"
newsims = sc.calculate_new_sims(refsolid, set_solids, set_zrot, zrot_solids_dict)

#print("\n")
#print(newsims)
#print("\n")
#newsimsdir = "newsims"
#if os.path.exists(newsimsdir):
    #shutil.rmtree(newsimsdir)
#newsims.write(prefix=newsimsdir)

forces_folder = os.path.join(os.getenv("HOME"), "Dropbox/forcesWinglets/resultsFromFirstCalcRun/")
filenames = [os.path.join(forces_folder, filename) for filename in os.listdir(forces_folder)]

simulation_dict2, set_solids2, set_yrot2, set_zrot2 = sim.load_from_files(filenames)

sim.match_newsims_to_results(newsims, set_solids2, simulation_dict2)


zrot_solids_dict2 = sim.create_forcesDict_zrot_solid(set_zrot, set_solids2, simulation_dict2, useref=True)

#wv.plot_lift_ref_other(refsolid, zrot_solids_dict, set_zrot, set_solids2, zrot_solids_dict2)
#wv.plot_drag_ref_other(refsolid, zrot_solids_dict, set_zrot, set_solids2, zrot_solids_dict2)
#wv.plot_liftangle_ref_other(refsolid, zrot_solids_dict, set_zrot, set_solids2, zrot_solids_dict2)

sim.create_dragforcelift_ratios(set_zrot, set_solids, zrot_solids_dict)
wv.plot_dragforceratio_ref_other2(refsolid , zrot_solids_dict, set_zrot, set_solids2, zrot_solids_dict2)
