import numpy as np
from collections import deque

class Simulation(object):
    def __init__(self,stack):

        line = stack[0]
        self.solidfile = line.split(":")[-1].strip()
        self.solidgroup = self.solidfile.split(".",1)[0]

        line = stack[1]
        x, y, z, s = line.split(',')

        self.xrot = np.float64(x.split(":")[-1].strip())
        self.yrot = np.float64(y.split(":")[-1].strip())
        self.zrot = np.float64(z.split(":")[-1].strip())
        self.speed = np.float64(s.split(":")[-1].strip().split()[0])

        line = stack[2]
        self.dateAndTime = line.split(":",1)[1].strip()

        line = stack[3]
        self.nIterations = np.int(line.split(":")[-1].strip())
        self.force = np.array([stack[5].strip(), stack[6].strip(), stack[7].strip()], dtype=np.float64)

        self.refyrot = None
        self.refzrot = None

    def has_rot(self, x=None, y=None, z=None, refy=None, refz=None, tolerance=np.float64(0.01)):
        assert (x is not None or y is not None or z is not None or refy is not None or refz is not None)
        if x is not None:
            if np.abs(np.float64(x) - self.xrot) > tolerance:
                return False

        if y is not None:
            if np.abs(np.float64(y) - self.yrot) > tolerance:
                return False

        if z is not None:
            if np.abs(np.float64(z) - self.zrot) > tolerance:
                return False

        if refy is not None:
            if self.refyrot is None:
                return False
            if np.abs(np.float64(refy) - self.refyrot) > tolerance:
                return False

        if refz is not None:
            if self.refzrot is None:
                return False
            if np.abs(np.float64(refz) - self.refzrot) > tolerance:
                return False
        return True

    def __str__(self):
        string =    "solidfile: %s" % self.solidfile
        string += "\nsolidgroup: %s"%(self.solidgroup)
        string += "\nx: %s, y: %s, z: %s"%(self.xrot,self.yrot,self.zrot)
        string += "\nspeed [kn]: %s"%(self.speed)
        string += "\ndate & time: %s"%(self.dateAndTime)
        string += "\nnumber of iterations: %s"%(self.nIterations)
        string += "\nforce [dN]: [%s]"%(",".join(self.force))
        return string

def create_forcesDict_zrot_solid(set_zrot, set_solids, simulation_dict, useref=False):
    # [zrot][solidname]
    zrot_solids_dict = dict()
    for zrot in set_zrot:
        try:
            zrotelement = zrot_solids_dict[zrot]
        except KeyError:
            zrot_solids_dict[zrot] = {}
            zrotelement = zrot_solids_dict[zrot]
        for solid in set_solids:
            try:
                zrotelementsolid = zrotelement[solid]
            except KeyError:
                zrotelement[solid] = {}
                zrotelementsolid = zrotelement[solid]

    for zrot,i in zip(set_zrot, range(len(set_zrot))):
        for solid,j in zip(set_solids,range(len(set_solids))):
            zrotelementsolid = zrot_solids_dict[zrot][solid]
            solidlist = simulation_dict[solid]
            if useref:
                sorted_list_zrot = sorted([(sim.yrot, sim.force) for sim in solidlist if sim.has_rot(refz=zrot)])
            else:
                sorted_list_zrot = sorted([(sim.yrot, sim.force) for sim in solidlist if sim.has_rot(z=zrot)])
            yrot = np.array([a[0] for a in sorted_list_zrot])
            fx = np.array([a[1][0] for a in sorted_list_zrot])
            fy = np.array([a[1][1] for a in sorted_list_zrot])
            fz = np.array([a[1][2] for a in sorted_list_zrot])
            zrotelementsolid["lift"] = -yrot
            zrotelementsolid["yrot"] = yrot
            zrotelementsolid["fx"] = fx
            zrotelementsolid["fy"] = fy
            zrotelementsolid["fz"] = fz

    return zrot_solids_dict

def create_forces_derivative(dir, force, set_zrot, set_solids, zrot_solids_dict):
    for zrot in set_zrot:
        for solid in set_solids:
            zrotelementsolid = zrot_solids_dict[zrot][solid]

            avg_dircoord_name = "avg_"+dir
            delta_dircoord_name = "delta_"+dir
            delta_force_name = "delta_"+dir
            try:
                avg_dircoord = zrotelementsolid[avg_dircoord_name]
                delta_dircoord = zrotelementsolid[delta_dircoord_name]
            except KeyError:
                dircoord = np.array(zrotelementsolid[dir])
                avg_dircoord = np.divide(np.add(dircoord[:-1], dircoord[1:]), np.full((len(dircoord)-1, 1), 2.0))
                delta_dircoord = np.subtract(dircoord[1:], dircoord[:-1])
                zrotelementsolid[avg_dircoord_name] = avg_dircoord
                zrotelementsolid[delta_dircoord_name] = delta_dircoord

            dforceddir_name = "D"+force+"D"+dir
            forcearray = zrotelementsolid[force]
            try:
                dforceddir = zrotelementsolid[dforceddir_name]
            except KeyError:
                delta_force = np.subtract(forcearray[1:], forcearray[:-1])
                dforceddir = np.divide(delta_force, delta_dircoord)
                zrotelementsolid[dforceddir_name] = dforceddir

def create_dragforcelift_ratios(set_zrot, set_solids, zrot_solids_dict):
    for zrot in set_zrot:
        for solid in set_solids:
            zrotelementsolid = zrot_solids_dict[zrot][solid]

            try:
                fz_by_fx = zrotelementsolid['fzBYfx']
                fy_by_fx = zrotelementsolid['fyBYfx']
                fyz_by_fx = zrotelementsolid['fyzBYfx']
                fyz = zrotelementsolid['fyz']
            except KeyError:
                fx = zrotelementsolid['fx']
                fy = zrotelementsolid['fy']
                fz = zrotelementsolid['fz']
                #fz_by_fx = np.abs(np.divide(fz, fx))
                fz_by_fx = np.divide(fz, np.abs(fx))
                #fy_by_fx = np.abs(np.divide(fy, fx))
                fy_by_fx = np.divide(fy, np.abs(fx))
                #sum_of_squares = np.add(np.square(fy), np.square(fz))
                sum_of_squares = np.add(np.square(fy), np.square(fz))
                fyz = np.sqrt(sum_of_squares)
                fyz_by_fx = np.divide(fyz, np.abs(fx))
                zrotelementsolid['fyz'] = fyz
                zrotelementsolid['fzBYfx'] = fz_by_fx
                zrotelementsolid['fyBYfx'] = fy_by_fx
                zrotelementsolid['fyzBYfx']= fyz_by_fx


def create_forces_zrot_derivative(force, set_zrot, set_solids, zrot_solids_dict):

    assert len(set_zrot) == 2
    dir = "yaw"

    for solid in set_solids:
        zrotelementsolid_0 = zrot_solids_dict[set_zrot[0]][solid]
        zrotelementsolid_1 = zrot_solids_dict[set_zrot[1]][solid]

        assert len(zrotelementsolid_0['lift']) == len(zrotelementsolid_1['lift'])

        dforceddir_name = "D"+force+"D"+dir
        dforceddir_name2 = "D"+force+"Dzrot"
        forcearray_0 = zrotelementsolid_0[force]
        forcearray_1 = zrotelementsolid_1[force]
        try:
            dforceddir_0 = zrotelementsolid_0[dforceddir_name]
            dforceddir_1 = zrotelementsolid_1[dforceddir_name]
        except KeyError:
            delta_force = np.subtract(forcearray_1, forcearray_0)
            dforceddir = np.divide(delta_force, np.full(len(forcearray_0),set_zrot[1]-set_zrot[0]))
            zrotelementsolid_0[dforceddir_name] = dforceddir
            zrotelementsolid_1[dforceddir_name] = dforceddir
            zrotelementsolid_0[dforceddir_name2] = dforceddir
            zrotelementsolid_1[dforceddir_name2] = dforceddir

def load_from_files(filenames):
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

    return simulation_dict, set_solids, set_yrot, set_zrot

def match_newsims_to_results(new_sims_conf, solids, new_sims):
    for solid in solids:

        solidconf = new_sims_conf[solid]
        solidsims = new_sims[solid]
        for key, confi in iter(solidconf.configdict.items()):
            rotx = confi.xrot
            roty = confi.yrot
            rotz = confi.zrot
            refroty = confi.refyrot
            refrotz = confi.refzrot

            found = False
            for s in solidsims:
                if s.has_rot(x=rotx,y=roty,z=rotz):
                    found = True
                    s.refyrot = refroty
                    s.refzrot = refrotz
                    print("solid sim found -> %.2f, %.2f : %.2f, %.2f" % (roty, rotz, refroty, refrotz))
                    break
            if not found:
                raise ValueError()
     #for zrot, zrotdict in iter(zrot_solids_dict):

     #zrotelementsolid = zrot_solids_dict[zrot][solid]
