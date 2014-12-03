from toontown.event import ExperimentEventObjectives
from toontown.event.DistributedEventAI import DistributedEventAI
from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI
from toontown.dna.DNAStorage import DNAStorage
from toontown.dna.DNAParser import loadDNAFileAI
import time


class DistributedExperimentEventAI(DistributedEventAI):
    notify = directNotify.newCategory('DistributedExperimentEventAI')
    DifficultyTime = 120

    def __init__(self, air):
        DistributedEventAI.__init__(self, air)

        self.suitPlanner = None
        self.currentDifficulty = 0
        self.maxDifficulty = 3
        self.currentObjective = None

    def start(self):
        self.suitPlanner = DistributedSuitPlannerAI(self.air, self.zoneId, self.setupDNA)
        self.suitPlanner.generateWithRequired(self.zoneId)
        self.suitPlanner.d_setZoneId(self.zoneId)
        self.suitPlanner.resetSuitHoodInfo(30000)
        self.suitPlanner.initTasks()

        self.setObjective(1)

        taskMgr.doMethodLater(self.DifficultyTime, self.increaseDifficulty, 'increaseDifficulty-%s' % id(self))
        self.createBlimp()

        DistributedEventAI.start(self)

    def increaseDifficulty(self, task):
        if self.currentDifficulty == self.maxDifficulty:
            return

        self.currentDifficulty += 1
        self.suitPlanner.resetSuitHoodInfo(30000 + self.currentDifficulty)
        taskMgr.doMethodLater(self.DifficultyTime, self.increaseDifficulty, 'increaseDifficulty-%s' % id(self))

    def createBlimp(self):
        self.sendUpdate('createBlimp', [int(time.time())])

    def setVisGroups(self, visGroups):
        self.sendUpdate('setVisGroups', [visGroups])

    def setupDNA(self, suitPlanner):
        if suitPlanner.dnaStore:
            return None
        suitPlanner.dnaStore = DNAStorage()
        loadDNAFileAI(suitPlanner.dnaStore, 'phase_4/dna/toontown_central_sz.pdna')

        visGroups = {}
        for visGroup in suitPlanner.dnaStore.DNAVisGroups:
            zone = int(visGroup.name)
            if zone == 2000:
                visGroups[2000] = self.zoneId
            else:
                visGroups[zone] = self.air.allocateZone()
            visGroup.name = str(visGroups[zone])

        for suitEdges in suitPlanner.dnaStore.suitEdges.values():
            for suitEdge in suitEdges:
                suitEdge.setZoneId(visGroups[suitEdge.zoneId])

        self.setVisGroups(visGroups.values())
        suitPlanner.initDNAInfo()

    def setObjectiveCount(self, count):
        self.sendUpdate('setObjectiveCount', [count])

    def setObjective(self, objectiveId):
        self.currentObjective = None
        if objectiveId:
            self.currentObjective = ExperimentEventObjectives.makeObjective(objectiveId, self)
        self.sendUpdate('setObjective', [objectiveId])

    def completeObjective(self):
        self.sendUpdate('completeObjective', [])
        self.setObjective(0)
