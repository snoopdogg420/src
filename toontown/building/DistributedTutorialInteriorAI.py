from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedTutorialInteriorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTutorialInteriorAI")

    def __init__(self, block, air, zoneId):
        DistributedObjectAI.__init__(self, air)
        self.zoneId = zoneId
        self.block = block
        self.tutorialNpcId = 0

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]

    def setTutorialNpcId(self, npcId):
        self.tutorialNpcId = npcId

    def getTutorialNpcId(self):
        return self.tutorialNpcId
