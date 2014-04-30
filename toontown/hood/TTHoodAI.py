from toontown.toonbase import ToontownGlobals
from toontown.classicchars import DistributedMickeyAI
from HoodAI import HoodAI

class TTHoodAI(HoodAI):
    HOOD = ToontownGlobals.ToontownCentral
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()
        
        if simbase.config.GetBool('want-classicchar', 1):
            self.classicChar = DistributedMickeyAI.DistributedMickeyAI(self.air)
            self.classicChar.generateWithRequired(self.HOOD)
            self.classicChar.start()
            