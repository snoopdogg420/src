from direct.distributed.DistributedObject import DistributedObject


class DistributedEvent(DistributedObject):
    notify = directNotify.newCategory('DistributedEvent')

    def start(self):
        pass

    def announceGenerate(self):
        self.cr.event = self

    def delete(self):
        self.cr.event = None
