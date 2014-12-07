from toontown.event.ExperimentBarrelBase import ExperimentBarrelBase
from direct.distributed.DistributedNodeAI import DistributedNodeAI
import random
import math


class DistributedExperimentBarrelAI(ExperimentBarrelBase, DistributedNodeAI):
    notify = directNotify.newCategory('DistributedExperimentBarrelAI')

    def __init__(self, air):
        ExperimentBarrelBase.__init__(self)
        DistributedNodeAI.__init__(self, air)

        self.usedBy = []

    def requestGrab(self, avId):
        if avId in self.usedBy:
            self.notify.info('Toon %s tried using the barrel more than once' % avId)
            return

        self.usedBy.append(avId)
        self.setGrab(avId)

    def gagGrab(self, avId):
        av = self.air.doId2do[avId]
        av.inventory.maxOutInv()
        av.d_setInventory(av.inventory.makeNetString())

    def toonupGrab(self, avId):
        av = self.air.doId2do[avId]
        av.toonUp(math.floor(av.getMaxHp() * 0.33))

    def experienceGrab(self, avId):
        av = self.air.doId2do[avId]
        for track, hasAccess in enumerate(av.trackArray):
            if hasAccess:
                level = av.experience.getExpLevel(track)
                xpNeeded = av.experience.getNextExpValue(track) - av.experience.getExp(track)
                xp = xpNeeded * max((random.random() / 2) - max(random.random() - ((level + 1) / 10), 0.1), 0.1)
                av.experience.setExp(track, av.experience.getExp(track) + math.floor(xp))
        av.d_setExperience(av.experience.makeNetString())

    def setGrab(self, avId):
        if self.type == self.GAG_BARREL:
            self.gagGrab(avId)
        elif self.type == self.TOONUP_BARREL:
            self.toonupGrab(avId)
        elif self.type == self.EXPERIENCE_BARREL:
            self.experienceGrab(avId)
        self.sendUpdate('setGrab', [avId])
