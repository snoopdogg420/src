from toontown.toonbase import ToontownGlobals
from toontown.classicchars import DistributedMinnieAI
from HoodAI import HoodAI

class MMHoodAI(HoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()
        
        if simbase.config.GetBool('want-classicchar', 1):
            self.classicChar = DistributedMinnieAI.DistributedMinnieAI(self.air)
            self.classicChar.generateWithRequired(self.HOOD)
