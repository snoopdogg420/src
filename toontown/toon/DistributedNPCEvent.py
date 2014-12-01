from toontown.toon.DistributedNPCToon import DistributedNPCToon


class DistributedNPCEvent(DistributedNPCToon):
    def handleCollisionSphereEnter(self, collEntry):
        self.sendUpdate('requestEvent', [base.localAvatar.doId])