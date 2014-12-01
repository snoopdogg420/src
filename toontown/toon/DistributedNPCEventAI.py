from toontown.toon.DistributedNPCToonAI import DistributedNPCToonAI


class DistributedNPCEventAI(DistributedNPCToonAI):
    def __init__(self, air, npcId):
        DistributedNPCToonAI.__init__(self, air, npcId)

        self.eventManager = None

    def setEventManager(self, eventManager):
        self.eventManager = eventManager

    def requestEvent(self, avId):
        self.eventManager.createEvent([avId])