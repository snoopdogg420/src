from toontown.toon.DistributedNPCToonAI import DistributedNPCToonAI
import time


class DistributedNPCExperimentEventAI(DistributedNPCToonAI):
    def __init__(self, air, npcId):
        DistributedNPCToonAI.__init__(self, air, npcId)

        self.scienceFair = None
        self.participants = []

    def announceGenerate(self):
        DistributedNPCToonAI.announceGenerate(self)

        taskMgr.doMethodLater(10, self.startEvent, 'startEvent-%s' % id(self))
        self.setCountdownStartTime(int(time.time()))

    def setScienceFair(self, scienceFair):
        self.scienceFair = scienceFair

    def requestJoin(self, avId):
        if avId not in self.participants:
            self.participants.append(avId)
            self.sendUpdate('notifyJoin', [avId])
            self.d_setParticipants(self.participants)

    def requestLeave(self, avId):
        if avId in self.participants:
            self.participants.remove(avId)
            self.sendUpdate('notifyLeave', [avId])
            self.d_setParticipants(self.participants)

    def d_setParticipants(self, participants):
        self.sendUpdate('setParticipants', [participants])

    def setCountdownStartTime(self, time):
        self.sendUpdate('setCountdownStartTime', [time])

    def startEvent(self, task):
        if self.participants:
            self.scienceFair.createEvent(self.participants)
            self.participants = []
            self.d_setParticipants(self.participants)
        taskMgr.doMethodLater(10, self.startEvent, 'startEvent-%s' % id(self))
        self.setCountdownStartTime(int(time.time()))
