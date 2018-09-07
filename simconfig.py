import unittest
import shutil
import os
import sim
import numpy as np

class NewSimManager():
    def __init__(self):
        self.__solid_sim_managers = {}

    def __getitem__(self, item):
        try:
            return self.__solid_sim_managers[item]
        except KeyError:
            self.__solid_sim_managers[item] = SolidSimManager(item)
            return self.__solid_sim_managers[item]

    def __str__(self):
        string =  "Contains %u solids:" % len(self.__solid_sim_managers)
        for solid, manager in iter(self.__solid_sim_managers.items()):
                string += "\n* %s with %u configs" % (solid, manager.num_configs())
        return string

    def write(self,prefix=None):
        for solid, manager in iter(self.__solid_sim_managers.items()):
            manager.create_all_files(prefix=prefix)

class SolidSimManager(object):
    def __init__(self, solidname):
        self.solidname = solidname
        self.configdict = {}

    def num_configs(self):
        return len(self.configdict)

    def has_config(self, rotx, roty, rotz, vel):
        return NewSimConfig.create_filename(rotx, roty, rotz, vel) in self.configdict

    def add_config(self, rotx, roty, rotz, vel, refy=None, refz=None):
        if not self.has_config(rotx, roty, rotz, vel):
            self.configdict[NewSimConfig.create_filename(rotx, roty, rotz, vel)] = \
                NewSimConfig(rotx, roty, rotz, vel, self.solidname, refy=refy, refz=refz)
        else:
            raise KeyError("Key is already present in configdict, overwrite is not allowed")
    def get_config(self, rotx, roty, rotz, vel):
        return self.configdict[NewSimConfig.create_filename(rotx, roty, rotz, vel)]

    def create_all_files(self,prefix=None):
        self.create_config_files(prefix=prefix)
        self.create_run_files(prefix=prefix)

    def create_run_files(self,prefix=None):
        filename = self.solidname+".sh"
        if prefix:
            filename = os.path.join(prefix,filename)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as f:
            f.write("#!/bin/bash -x\n")
            f.write("\n")
            for key, config in iter(self.configdict.items()):
                f.write("./run.py -c %s -g %s -f force.%s.log\n" % (config.filename, config.configfile, self.solidname))

    def create_config_files(self,prefix=None):
        for key, config in iter(self.configdict.items()):
            config.write_config_file(prefix=prefix)

class NewSimConfig(object):
    @staticmethod
    def create_filename(rotx, roty, rotz, vel):
        # absolute velocity
        speed_string="%.1f" % abs(vel)
        xrot_string="X%.2f" % rotx
        yrot_string="Y%.2f" % roty
        zrot_string="Z%.2f" % rotz
        return "_".join([speed_string, xrot_string, yrot_string, zrot_string]) + ".cfg"

    def __init__(self, rotx, roty, rotz, vel, solidname, configfile=None, refy=None, refz=None):
        self.speed = -abs(vel)
        self.filename = os.path.join("config",NewSimConfig.create_filename(rotx, roty, rotz, vel))
        self.xrot = rotx
        self.yrot = roty
        self.zrot = rotz
        self.configfile = configfile if configfile is not None else os.path.join("geometries",solidname+".cfg")
        self.refyrot = refy
        self.refzrot = refz

    def write_config_file(self,prefix=None):
        filename = self.filename
        if prefix:
            filename = os.path.join(prefix, filename)

        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename,'w') as f:
            f.write("[VELOCITY]\n")
            f.write("speed = %.1f\n" % self.speed)
            f.write("[ROTATION]\n")
            f.write("Xrotation = %.2f\n" % self.xrot)
            f.write("Yrotation = %.2f\n" % self.yrot)
            f.write("Zrotation = %.2f\n" % self.zrot)


class TestNewSimConfig(unittest.TestCase):
    def test_name(self):
        rotx = 2.1
        roty = 1.2
        rotz = 3.9
        speed =  18.0
        filename = NewSimConfig.create_filename(rotx,roty,rotz,speed)
        self.assertEqual("18.0_X2.10_Y1.20_Z3.90.conf",filename)

        filename2 = NewSimConfig.create_filename(rotx,roty,rotz,-speed)
        self.assertEqual(filename,filename2,"Velocity sign shouldn't matter")

    def test_vel(self):
        rotx = 2.1
        roty = 1.2
        rotz = 3.9
        vel =  18.0
        sconfig1 = NewSimConfig(rotx,roty,rotz,vel,"unknown")
        sconfig2 = NewSimConfig(rotx,roty,rotz,-vel,"unknown")
        self.assertEqual(-vel,sconfig1.speed,"Speed is negative in object")
        self.assertEqual(-vel,sconfig2.speed,"Speed is negative in object")

class TestSolidSimManager(unittest.TestCase):
    def test_config(self):
        rotx = 2.1
        roty = 1.2
        rotz = 3.9
        vel =18.0
        solidname = "test"
        solidmanager = SolidSimManager(solidname)
        self.assertFalse(solidmanager.has_config(rotx, roty, rotz, vel))
        solidmanager.add_config(rotx, roty, rotz, vel)

        self.assertTrue(solidmanager.has_config(rotx, roty, rotz, vel))

        with self.assertRaises(KeyError):
            solidmanager.add_config(rotx, roty, rotz, vel)

    def test_file_folder_creation(self):
        prefixfolder = "testfolder"
        if os.path.exists(prefixfolder):
            print("WARNING: prefix folder exists already and will be deleted")
            shutil.rmtree(prefixfolder)

        solidname = "winglet_abc"
        solidmanager = SolidSimManager(solidname)
        solidmanager.add_config(1, 2, 3, 4)
        solidmanager.create_all_files(prefix=prefixfolder)

        self.assertTrue(os.path.exists(prefixfolder))

def calculate_new_sims(target_solid, set_solids, set_zrot, zrot_solids_dict):
    assert target_solid in set_solids

    sim.create_forces_derivative('yrot', 'fy', set_zrot, set_solids, zrot_solids_dict)
    sim.create_forces_derivative('yrot', 'fz', set_zrot, set_solids, zrot_solids_dict)
    sim.create_forces_zrot_derivative('fy', set_zrot, set_solids, zrot_solids_dict)

    newsims = NewSimManager()

    for zrot in set_zrot:
        refobj = zrot_solids_dict[zrot][target_solid]
        refarrayfx = refobj['fx']
        refarrayfy = refobj['fy']
        refarrayfz = refobj['fz']
        refarrayy = refobj['yrot']
        for reffx,reffy,reffz,refy in zip(refarrayfx, refarrayfy, refarrayfz, refarrayy):
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
                newsims[solid].add_config(0, new_y, new_z, 18.0, refy=refy, refz=zrot)
    return newsims
