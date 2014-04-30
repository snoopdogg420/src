from toontown.toonbase import ToontownGlobals
from toontown.classicchars import DistributedGoofySpeedwayAI
from HoodAI import HoodAI

class GSHoodAI(HoodAI):
    HOOD = ToontownGlobals.GoofySpeedway
        
    def createSafeZone(self):
        self.spawnObjects()
        
        if simbase.config.GetBool('want-classicchar', 1):
            self.classicChar = DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI(self.air)
            self.classicChar.generateWithRequired(self.HOOD)
        
