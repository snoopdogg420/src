from direct.distributed.ClockDelta import globalClockDelta

from toontown.dna.DNAParser import loadDNAFileAI
from toontown.dna.DNAStorage import DNAStorage
from toontown.event import ExperimentChallenges
from toontown.event.DistributedEventAI import DistributedEventAI
from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI
from toontown.event.ExperimentBarrelPlannerAI import ExperimentBarrelPlannerAI
from toontown.toon.Experience import Experience
from toontown.toon.InventoryBase import InventoryBase
from toontown.toon.ToonSerializer import ToonSerializer


class DistributedExperimentEventAI(DistributedEventAI):
    notify = directNotify.newCategory('DistributedExperimentEventAI')

    def __init__(self, air):
        DistributedEventAI.__init__(self, air)

        self.suitPlanner = None
        self.barrelPlanner = None
        self.currentChallenge = None

    def start(self):
        self.suitPlanner = DistributedSuitPlannerAI(self.air, self.zoneId, self.setupDNA)
        self.suitPlanner.generateWithRequired(self.zoneId)
        self.suitPlanner.d_setZoneId(self.zoneId)

        self.barrelPlanner = ExperimentBarrelPlannerAI(self)

        self.b_setState('Phase0')

        DistributedEventAI.start(self)

    def setCogDifficulty(self, difficulty):
        if difficulty > 3:
            self.notify.warning('Tried setting the cog difficulty too high')
            return

        self.suitPlanner.resetSuitHoodInfo(30000 + difficulty)
        self.suitPlanner.flySuits()

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

    def getInitialChallengeId(self):
        return min(len(self.participants), 5)

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

    def enterIntroduction(self):
        pass

    def exitIntroduction(self):
        pass

    def enterPhase0(self):
        self.suitPlanner.initTasks()
        self.barrelPlanner.start()
        self.setCogDifficulty(0)

        self.setChallenge(self.getInitialChallengeId())

    def exitPhase0(self):
        pass

    def enterPhase1(self):
        self.setCogDifficulty(1)

    def exitPhase1(self):
        pass

    def enterPhase2(self):
        self.setCogDifficulty(2)

    def exitPhase2(self):
        pass

    def enterPhase3(self):
        self.setCogDifficulty(3)

    def exitPhase3(self):
        pass

    def enterCredits(self):
        self.setChallenge(0)

        if self.barrelPlanner:
            self.barrelPlanner.cleanup()
            self.barrelPlanner = None

        if self.suitPlanner:
            self.suitPlanner.cleanup()
            self.suitPlanner = None

    def exitCredits(self):
        pass
