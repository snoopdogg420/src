from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedEventAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedEventAI')
