from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.PyDatagram import *

from toontown.dna.DNAParser import loadDNAFileAI
from toontown.dna.DNAStorage import DNAStorage
from toontown.event import ExperimentEventObjectives
from toontown.event.DistributedEventAI import DistributedEventAI
from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI
from toontown.toon.DistributedExperimentToonAI import DistributedExperimentToonAI
from toontown.toon.Experience import Experience
from toontown.toon.InventoryBase import InventoryBase
from toontown.toonbase import ToontownGlobals


class DistributedExperimentEventAI(DistributedEventAI):
    notify = directNotify.newCategory('DistributedExperimentEventAI')

    def __init__(self, air):
        DistributedEventAI.__init__(self, air)

        self.suitPlanner = None
        self.currentDifficulty = 0
        self.maxDifficulty = 3
        self.currentObjective = None
        self.experimentToons = {}

    def start(self):
        self.suitPlanner = DistributedSuitPlannerAI(self.air, self.zoneId, self.setupDNA)
        self.suitPlanner.generateWithRequired(self.zoneId)
        self.suitPlanner.d_setZoneId(self.zoneId)
        self.suitPlanner.resetSuitHoodInfo(30000)
        self.suitPlanner.initTasks()

        self.setObjective(1)

        self.createBlimp()

        DistributedEventAI.start(self)

    def increaseDifficulty(self):
        if self.currentDifficulty == self.maxDifficulty:
            return

        self.currentDifficulty += 1
        self.suitPlanner.resetSuitHoodInfo(30000 + self.currentDifficulty)

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

    def setParticipants(self, participants):
        self.participants = participants

        for avId in self.participants:
            self.createExperimentToon(avId)

            av = self.air.doId2do[avId]
            av.currentEvent = self
            av.setClientInterest(self.zoneId)

    def createExperimentToon(self, avId):
        av = self.air.doId2do[avId]

        newAv = DistributedExperimentToonAI(self.air)
        newAv.setName(av.name)
        newAv.setDNAString(av.dnaString)
        newAv.experience = Experience(owner=newAv)
        newAv.inventory = InventoryBase(newAv)
        newAv.gameAccess = ToontownGlobals.AccessFull
        newAv.currentEvent = self
        newAv.generateWithRequired(self.zoneId)

        self.experimentToons[avId] = newAv
        self.acceptOnce('distObjDelete-%s' % avId, self.deleteExperimentToon, [avId])

        datagram = PyDatagram()
        datagram.addServerHeader(
            newAv.doId,
            self.air.ourChannel,
            STATESERVER_OBJECT_SET_OWNER)
        datagram.addChannel(avId + (1001L<<32))
        self.air.send(datagram)

    def requestExperimentToon(self, avId):
        av = self.experimentToons[avId]
        self.air.doId2do[avId] = av
        self.sendUpdateToAvatarId(avId, 'setExperimentToon', [av.doId])

    def setExperimentToonResponse(self, avId):
        av = self.air.doId2do[avId]

        av.b_setMaxHp(15)
        av.b_setHp(15)
        av.b_setExperience(av.experience.makeNetString())
        av.b_setTrackAccess([0, 0, 0, 0, 1, 1, 0])
        av.b_setTrackBonusLevel([-1, -1, -1, -1, -1, -1, -1])
        av.b_setMaxCarry(20)
        av.inventory.maxOutInv()
        av.b_setInventory(av.inventory.makeNetString())
        av.b_setMoney(0)
        av.b_setCogMerits([0, 0, 0, 0])
        av.b_setCogParts([0, 0, 0, 0])
        av.b_setCogTypes([0, 0, 0, 0])
        av.b_setCogLevels([0, 0, 0, 0])
        av.b_setCogStatus([1] * 32)
        av.b_setCogCount([0] * 32)
        av.b_setCogRadar([0, 0, 0, 0])
        av.b_setBuildingRadar([0, 0, 0, 0])
        av.b_setPromotionStatus([0, 0, 0, 0])
        av.b_setQuestCarryLimit(1)
        av.b_setQuests([])
        av.b_setResistanceMessages([])
        av.b_setPinkSlips(1)

    def deleteExperimentToon(self, avId):
        self.experimentToons[avId].requestDelete()
