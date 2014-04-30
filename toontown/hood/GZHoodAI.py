from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI

class GZHoodAI(HoodAI):
    HOOD = ToontownGlobals.GolfZone
        
    def createSafeZone(self):
        self.spawnObjects()
