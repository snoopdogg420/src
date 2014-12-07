from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.event.DistributedExperimentEventAI import DistributedExperimentEventAI
from toontown.toon import NPCToons


class DistributedScienceFairAI(DistributedObjectAI):
    def __init__(self, air, npcId):
        DistributedObjectAI.__init__(self, air)

        self.npc = None
        self.npcId = npcId
        self.events = []

    def generateWithRequired(self, zoneId):
        DistributedObjectAI.generateWithRequired(self, zoneId)

        self.npc = NPCToons.createNPC(self.air, self.npcId,
                                      NPCToons.NPCToonDict[self.npcId],
                                      self.zoneId)
        self.npc.setScienceFair(self)

    def createEvent(self, participants):
        zoneId = self.air.allocateZone()
        event = DistributedExperimentEventAI(self.air)
        event.generateWithRequired(zoneId)

        for avId in participants:
            av = self.air.doId2do[avId]
            event.joinEvent(avId)
            av.setClientInterest(event.zoneId)

        event.start()
        self.events.append(event)
