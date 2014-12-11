from toontown.event.DistributedExperimentBarrelAI import DistributedExperimentBarrelAI
from toontown.event.ExperimentBarrelBase import ExperimentBarrelBase
import random


BarrelPosHpr = [(37.963, -26.464, 4.025, 48.889, 0, 0),
 (29.876, -42.159, 4.025, 19.128, 0, 0),
 (65, -59, 6.051, 6.051, 0, 0),
 (57, -59, 6.051, 6.051, 0, 0),
 (69, -82, 3.025, 128.959, 0, 0),
 (83, -108, 2.525, 103.767, 0, 0),
 (85, -136, 2.525, 67, 0, 0),
 (9, -130, 3.025, -8, 0, 0),
 (5.972, -100.866, 2.525, -165.629, 0, 0),
 (-31, -85, 0.525, -320, 0, 0),
 (-59.860, -91.097, 0.525, -375.564, 0, 0),
 (-81.445, -87.351, 0.525, -374.622, 0, 0),
 (-142.566, -58.951, 0.545, -504.030, 0, 0),
 (-127.437, -79.355, 0.545, -328.539, 0, 0),
 (-61.067, -5.004, 1.227, -355.695, 0, 0),
 (-60.515, -12.329, 1.227, -372.098, 0, 0),
 (-95.093, 31.552, -3.201, -107.794, 0, 0),
 (-90.206, 42.588, -3.312, -134.913, 0, 0),
 (-77.506, 47.471, -3.280, -181.143, 0, 0),
 (-63.348, 41.722, -3.360, -238.973, 0, 0),
 (-30.753, 53.763, 0.024, -194.624, 0, 0),
 (6.868, 95.654, 2.525, -191.939, 0, 0),
 (-20.639, 69.441, 0.029, -157.822, 0, 0),
 (21.564, 44.777, 4.983, -247.421, 0, 0),
 (15.858, 27.424, 4.025, -221.450, 0, 0)]


class ExperimentBarrelPlannerAI:
    notify = directNotify.newCategory('ExperimentBarrelPlannerAI')
    MIN_TIME = 7
    MAX_TIME = 14
    MIN_BARRELS = 2
    MAX_BARRELS = 5

    def __init__(self, experimentEvent):
        self.experimentEvent = experimentEvent
        self.air = self.experimentEvent.air
        self.zoneId = self.experimentEvent.zoneId
        self.taskName = 'barrel-planner-%s' % id(self)
        self.activeBarrels = []
        self.usedPositions = []

    def start(self):
        taskMgr.doMethodLater(0, self.barrelSpawnTask, self.taskName)

    def stop(self):
        taskMgr.remove(self.taskName)

    def barrelSpawnTask(self, task):
        self.deleteBarrels()

        usedPositions = []
        for i in xrange(random.randint(self.MIN_BARRELS, self.MAX_BARRELS)):
            pos = random.choice(BarrelPosHpr)
            while (pos in self.usedPositions) or (pos in usedPositions):
                pos = random.choice(BarrelPosHpr)
            usedPositions.append(pos)

            barrel = DistributedExperimentBarrelAI(self.air)
            barrel.setType(random.choice(ExperimentBarrelBase.BARREL_TYPES))
            barrel.generateWithRequired(self.zoneId)
            barrel.b_setPosHpr(*pos)
            self.activeBarrels.append(barrel)

        self.usedPositions = usedPositions

        taskMgr.doMethodLater(random.randint(self.MIN_TIME, self.MAX_TIME),
                              self.barrelSpawnTask, self.taskName)

    def deleteBarrels(self):
        for barrel in self.activeBarrels:
            barrel.requestDelete()
        self.activeBarrels = []

    def cleanup(self):
        self.stop()
        self.deleteBarrels()
