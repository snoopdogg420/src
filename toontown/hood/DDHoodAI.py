from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.classicchars import DistributedDonaldDockAI
from HoodAI import HoodAI

class DDHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDock

    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()

        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.HOOD)
        
        if simbase.config.GetBool('want-classicchar', 0):
            self.classicChar = DistributedDonaldDockAI.DistributedDonaldDockAI(self.air)
            self.classicChar.generateWithRequired(self.HOOD)
            self.classicChar.start()
