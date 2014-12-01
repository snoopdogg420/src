from toontown.event.DistributedEventAI import DistributedEventAI
from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI


class DistributedExperimentEventAI(DistributedEventAI):
    notify = directNotify.newCategory('DistributedExperimentEventAI')

    def __init__(self, air):
        DistributedEventAI.__init__(self, air)

        self.suitPlanner = None

    def start(self):
        # Create the DistributedSuitPlannerAI...
        self.suitPlanner = DistributedSuitPlannerAI(self.air, self.zoneId)
        self.suitPlanner.generateWithRequired(self.zoneId)
        self.suitPlanner.d_setZoneId(self.zoneId)
        self.suitPlanner.initTasks()

        DistributedEventAI.start(self)
