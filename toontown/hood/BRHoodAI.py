from toontown.toonbase import ToontownGlobals
from toontown.classicchars import DistributedPlutoAI
from HoodAI import HoodAI

class BRHoodAI(HoodAI):
    HOOD = ToontownGlobals.TheBrrrgh

    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()

        if simbase.config.GetBool('want-classicchar', 1):
            self.classicChar = DistributedPlutoAI.DistributedPlutoAI(self.air)
            self.classicChar.generateWithRequired(self.HOOD)
