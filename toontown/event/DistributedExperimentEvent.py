from toontown.event.DistributedEvent import DistributedEvent


class DistributedExperimentEvent(DistributedEvent):
    notify = directNotify.newCategory('DistributedExperimentEvent')
