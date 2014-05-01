from toontown.toonbase import ToontownGlobals
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.classicchars import DistributedChipAI
from toontown.classicchars import DistributedDaleAI
from HoodAI import HoodAI

class OZHoodAI(HoodAI):
    HOOD = ToontownGlobals.OutdoorZone
    
    def createSafeZone(self):
        HoodAI.createTreasurePlanner(self)

        self.spawnObjects()

        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)

        if simbase.config.GetBool('want-classicchar', 0):
            chip = DistributedChipAI.DistributedChipAI(self.air)
            chip.generateWithRequired(self.HOOD)
            chip.start()

            dale = DistributedDaleAI.DistributedDaleAI(self.air, chip.doId)
            dale.generateWithRequired(self.HOOD)
            dale.start()

            chip.setDaleId(dale.doId)
