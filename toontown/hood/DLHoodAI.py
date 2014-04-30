from toontown.toonbase import ToontownGlobals
from toontown.classicchars import DistributedDonaldAI
from HoodAI import HoodAI

class DLHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()
        
        if simbase.config.GetBool('want-classicchar', 1):
            self.classicChar = DistributedDonaldAI.DistributedDonaldAI(self.air)
            self.classicChar.generateWithRequired(self.HOOD)
