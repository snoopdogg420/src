from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase.PythonUtil import Functor


class DistributedEventAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedEventAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.participants = []

    def start(self):
        self.sendUpdate('start', [])

    def messageParticipants(self, message):
        self.sendUpdate('messageParticipants', [message])

    def joinEvent(self, avId):
        if avId in self.participants:
            return

        av = self.air.doId2do[avId]
        av.currentEvent = self
        self.participants.append(avId)

    def leaveEvent(self, avId):
        if avId not in self.participants:
            return

        av = self.air.doId2do[avId]
        av.currentEvent = None
        self.participants.remove(avId)

    def toonChangedZone(self, avId, zoneId):
        pass

