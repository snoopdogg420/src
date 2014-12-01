from toontown.event.DistributedEventAI import DistributedEventAI


class DistributedExperimentEventAI(DistributedEventAI):
    notify = directNotify.newCategory('DistributedExperimentEventAI')
