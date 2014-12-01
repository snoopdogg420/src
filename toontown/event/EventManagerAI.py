from toontown.toon import NPCToons


class EventManagerAI:
    def __init__(self, air, zoneId, eventCtor, npcId):
        self.air = air
        self.zoneId = zoneId
        self.eventCtor = eventCtor

        self.npc = NPCToons.createNPC(self.air, npcId, NPCToons.NPCToonDict[npcId], self.zoneId)
        self.npc.setEventManager(self)

        self.events = []

    def createEvent(self, participants):
        zoneId = self.air.allocateZone()
        event = self.eventCtor(self.air)
        event.generateWithRequired(zoneId)
        event.setParticipants(participants)
        event.start()
        self.events.append(event)