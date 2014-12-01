from direct.distributed.DistributedObject import DistributedObject


class DistributedEvent(DistributedObject):
    notify = directNotify.newCategory('DistributedEvent')
