from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.PyDatagram import *

from toontown.dna.DNAParser import loadDNAFileAI
from toontown.dna.DNAStorage import DNAStorage
from toontown.event import ExperimentChallenges
from toontown.event.DistributedEventAI import DistributedEventAI
from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI
from toontown.toon.Experience import Experience
from toontown.toon.InventoryBase import InventoryBase
from toontown.toon.ToonSerializer import ToonSerializer


class DistributedExperimentEventAI(DistributedEventAI):
    notify = directNotify.newCategory('DistributedExperimentEventAI')

    def __init__(self, air):
        DistributedEventAI.__init__(self, air)

        self.suitPlanner = None
        self.currentDifficulty = 0
        self.maxDifficulty = 3
        self.currentChallenge = None

        self.phase = 0

    def start(self):
        self.suitPlanner = DistributedSuitPlannerAI(self.air, self.zoneId, self.setupDNA)
        self.suitPlanner.generateWithRequired(self.zoneId)
        self.suitPlanner.d_setZoneId(self.zoneId)
        self.suitPlanner.resetSuitHoodInfo(30000)
        self.suitPlanner.initTasks()

        self.setChallenge(1)

        self.createBlimp()

        DistributedEventAI.start(self)

    def increaseDifficulty(self):
        if self.currentDifficulty == self.maxDifficulty:
            return

        self.currentDifficulty += 1
        self.suitPlanner.resetSuitHoodInfo(30000 + self.currentDifficulty)
        self.suitPlanner.flySuits()

    def createBlimp(self):
        self.sendUpdate('createBlimp', [globalClockDelta.getRealNetworkTime(bits=32)])

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

    def setChallengeCount(self, count):
        self.sendUpdate('setChallengeCount', [count])

    def setChallenge(self, challengeId):
        self.currentChallenge = None
        if challengeId:
            self.currentObjective = ExperimentChallenges.makeChallenge(challengeId, self)
        self.sendUpdate('setChallenge', [challengeId])

    def challengeComplete(self):
        self.sendUpdate('challengeComplete', [])
        self.setChallenge(0)

    def setPhase(self, phase):
        self.phase = phase

        self.sendUpdate('setPhase', [phase, globalClockDelta.getRealNetworkTime(bits=32)])

    def joinEvent(self, avId):
        DistributedEventAI.joinEvent(self, avId)

        self.makeFreshToon(avId)

    def leaveEvent(self, avId):
        self.restoreToon(avId)

        DistributedEventAI.leaveEvent(self, avId)

    def toonChangedZone(self, avId, zoneId):
        self.leaveEvent(avId)

    def restoreToon(self, avId):
        av = self.air.doId2do[avId]
        toonSerializer = ToonSerializer(av)
        toonSerializer.restoreToon()

    def makeFreshToon(self, avId):
        av = self.air.doId2do[avId]
        toonSerializer = ToonSerializer(av)
        toonSerializer.saveToon(callback=self.__resetToonStats)

    def __resetToonStats(self, av):
        av.b_setMaxHp(15)
        av.b_setHp(15)

        av.b_setMaxCarry(20)
        av.b_setMoney(0)
        av.b_setQuestCarryLimit(1)

        av.b_setTrackAccess([0, 0, 0, 0, 1, 1, 0])
        av.b_setTrackBonusLevel([-1, -1, -1, -1, -1, -1, -1])

        av.experience = Experience(owner=av)
        av.b_setExperience(av.experience.makeNetString())

        av.inventory = InventoryBase(av)
        av.inventory.maxOutInv()
        av.b_setInventory(av.inventory.makeNetString())

        av.b_setPinkSlips(1)

        av.b_setCogMerits([0, 0, 0, 0])
        av.b_setCogParts([0, 0, 0, 0])
        av.b_setCogTypes([0, 0, 0, 0])
        av.b_setCogLevels([0, 0, 0, 0])
        av.b_setCogStatus([1] * 32)
        av.b_setCogCount([0] * 32)
        av.b_setCogRadar([0, 0, 0, 0])
        av.b_setBuildingRadar([0, 0, 0, 0])
        av.b_setPromotionStatus([0, 0, 0, 0])

        av.b_setQuests([])
        av.b_setResistanceMessages([])

        av.b_setNPCFriendsDict([])

        av.b_setExperience(av.experience.makeNetString())
