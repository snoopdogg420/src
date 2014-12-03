from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedEventAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedEventAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.participants = []

    def start(self):
        self.sendUpdate('start', [])

    def removeParticipant(self, avId):
        if avId in self.participants:
            self.participants.remove(avId)
            av = self.air.doId2do[avId]
            av.currentEvent = None

    def setParticipants(self, participants):
        self.participants = participants

        for avId in self.participants:
            av = self.air.doId2do[avId]
            av.currentEvent = self
            av.setClientInterest(self.zoneId)
