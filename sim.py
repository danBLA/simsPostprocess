class Simulation(object):
    def __init__(self,stack):

        line = stack[0]
        self.solidfile = line.split(":")[-1].strip()
        self.solidgroup = self.solidfile.split("_",1)[0]

        line = stack[1]
        x,y,z,s = line.split(',')

        self.xrot = x.split(":")[-1].strip()
        self.yrot = y.split(":")[-1].strip()
        self.zrot = z.split(":")[-1].strip()
        self.speed = s.split(":")[-1].strip().split()[0]

        line = stack[2]
        self.dateAndTime = line.split(":",1)[1].strip()

        line = stack[3]
        self.nIterations = line.split(":")[-1].strip()
        self.force = [stack[5].strip(),stack[6].strip(),stack[7].strip()]


    def __str__(self):
        string =    "solidfile: %s" % self.solidfile
        string += "\nsolidgroup: %s"%(self.solidgroup)
        string += "\nx: %s, y: %s, z: %s"%(self.xrot,self.yrot,self.zrot)
        string += "\nspeed [kn]: %s"%(self.speed)
        string += "\ndate & time: %s"%(self.dateAndTime)
        string += "\nnumber of iterations: %s"%(self.nIterations)
        string += "\nforce [dN]: [%s]"%(",".join(self.force))
        return string
