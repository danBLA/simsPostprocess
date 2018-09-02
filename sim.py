import numpy as np

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

    def has_rot(self, x=None, y=None, z=None, tolerance=np.float64(0.01)):
        assert (x is not None or y is not None or z is not None)
        if x is not None:
            if np.abs(np.float64(x) - self.xrot) > tolerance:
                return False

        if y is not None:
            if np.abs(np.float64(y) - self.yrot) > tolerance:
                return False

        if z is not None:
            if np.abs(np.float64(z) - self.zrot) > tolerance:
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

def create_forcesDict_zrot_solid(set_zrot, set_solids, simulation_dict):
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
                fyz_by_fx = np.divide(np.sqrt(sum_of_squares), np.abs(fx))
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
