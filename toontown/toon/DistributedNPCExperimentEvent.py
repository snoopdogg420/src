from toontown.toon.DistributedNPCToon import DistributedNPCToon


class DistributedNPCExperimentEvent(DistributedNPCToon):
    def __init__(self, cr):
        DistributedNPCToon.__init__(self, cr)

        self.participants = []

    def handleCollisionSphereEnter(self, collEntry):
        self.sendUpdate('requestJoin', [base.localAvatar.doId])

    def notifyJoin(self, avId):
        pass

    def notifyLeave(self, avId):
        pass

    def setParticipants(self, participants):
        self.participants = participants

    def setCoutdownStartTime(self, time):
        pass

    def delete(self):
        self.sendUpdate('requestLeave', [base.localAvatar.doId])
