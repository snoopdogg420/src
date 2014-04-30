from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedDGFlowerAI
from toontown.classicchars import DistributedDaisyAI
from HoodAI import HoodAI

class DGHoodAI(HoodAI):
    HOOD = ToontownGlobals.DaisyGardens

    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()
        
        self.flower = DistributedDGFlowerAI.DistributedDGFlowerAI(self.air)
        self.flower.generateWithRequired(self.HOOD)
        
        if simbase.config.GetBool('want-classicchar', 0):
            self.classicChar = DistributedDaisyAI.DistributedDaisyAI(self.air)
            self.classicChar.generateWithRequired(self.HOOD)
            self.classicChar.start()