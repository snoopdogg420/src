from pandac.PandaModules import *

class CMover:

    def __init__(self, objNodePath, fwdSpeed=1, rotSpeed=1):
        self.objNodePath = objNodePath
        self.fwdSpeed = fwdSpeed
        self.rotSpeed = rotSpeed
        self.dt = None
        self.impulses = {}

    def setFwdSpeed(self, fwdSpeed):
        self.fwdSpeed = fwdSpeed

    def setRotSpeed(self, rotSpeed):
        self.rotSpeed = rotSpeed

    def getFwdSpeed(self):
        return self.fwdSpeed

    def getRotSpeed(self):
        return self.rotSpeed

    def addShove(self, shove):
        pass # TODO

    def addRotShove(self, rotShove):
        pass # TODO

    def getDt(self):
        return self.dt

    def addCImpulse(self, name, impulse):
        self.impulses[name] = impulse

    def removeCImpulse(self, name):
        self.impulses[name].clearMover(self)
        del self.impulses[name]

    def processCImpulses(self, dt):
        self.dt = dt

        for impulse in self.impulses.values():
            impulse._process(dt)

    def integrate(self):
        pass

    def getNodePath(self):
        return self.objNodePath
