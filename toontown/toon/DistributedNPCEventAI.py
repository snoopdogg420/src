from toontown.toon.DistributedNPCToonAI import DistributedNPCToonAI
import time


class DistributedNPCEventAI(DistributedNPCToonAI):
    def __init__(self, air, npcId):
        DistributedNPCToonAI.__init__(self, air, npcId)

        self.eventManager = None
        self.participants = []

    def announceGenerate(self):
        DistributedNPCToonAI.announceGenerate(self)

        taskMgr.doMethodLater(10, self.startEvent, 'startEvent-%s' % id(self))
        self.setCountdownStartTime(int(time.time()))

    def setEventManager(self, eventManager):
        self.eventManager = eventManager

    def requestJoin(self, avId):
        self.participants.append(avId)
        self.sendUpdate('notifyJoin', [avId])
        self.d_setParticipants(self.participants)

    def requestLeave(self, avId):
        self.participants.remove(avId)
        self.sendUpdate('notifyLeave', [avId])
        self.d_setParticipants(self.participants)

    def d_setParticipants(self, participants):
        self.sendUpdate('setParticipants', [participants])

    def setCountdownStartTime(self, time):
        self.sendUpdate('setCountdownStartTime', [time])

    def startEvent(self):
        if self.participants:
            self.eventManager.createEvent(self.participants)
            self.participants = []
            self.d_setParticipants(self.participants)
        taskMgr.doMethodLater(10, self.startEvent, 'startEvent-%s' % id(self))
        self.setCountdownStartTime(int(time.time()))
