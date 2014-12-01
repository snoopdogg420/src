from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedEventAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedEventAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.participants = []

    def start(self):
        self.sendUpdate('start', [])
