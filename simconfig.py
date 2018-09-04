import unittest
import shutil
import os

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

    def add_config(self, rotx, roty, rotz, vel):
        if not self.has_config(rotx, roty, rotz, vel):
            self.configdict[NewSimConfig.create_filename(rotx, roty, rotz, vel)] = \
                NewSimConfig(rotx, roty, rotz, vel, self.solidname)
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

    def __init__(self, rotx, roty, rotz, vel, solidname, configfile=None):
        self.speed = -abs(vel)
        self.filename = os.path.join("config",NewSimConfig.create_filename(rotx, roty, rotz, vel))
        self.xrot = rotx
        self.yrot = roty
        self.zrot = rotz
        self.configfile = configfile if configfile is not None else os.path.join("geometries",solidname+".cfg")

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
