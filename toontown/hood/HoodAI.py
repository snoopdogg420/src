from direct.directnotify.DirectNotifyGlobal import *
from toontown.building import DistributedBuildingMgrAI
from toontown.dna.DNAParser import DNAStorage, DNAGroup, DNAVisGroup, DNAData
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.hood import ZoneUtil
from toontown.safezone import TreasureGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedPartyGateAI import DistributedPartyGateAI
from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI
from toontown.suit import DistributedSuitPlannerAI
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals


class HoodAI:
    notify = directNotify.newCategory('HoodAI')
    notify.setInfo(True)

    def __init__(self, air, zoneId, canonicalHoodId):
        self.air = air
        self.zoneId = zoneId
        self.canonicalHoodId = canonicalHoodId

        self.fishingPonds = []
        self.partyGates = []
        self.treasurePlanner = None
        self.buildingManagers = []
        self.suitPlanners = []

        for zoneId in self.getZoneTable():
            dnaFileName = self.air.lookupDNAFileName(zoneId)
            self.notify.info('Creating objects... ' + dnaFileName)
            dnaStore = DNAStorage()
            dnaData = simbase.air.loadDNAFileAI(dnaStore, dnaFileName)
            self.air.dnaStoreMap[zoneId] = dnaStore
            self.air.dnaDataMap[zoneId] = dnaData

    def getZoneTable(self):
        zoneTable = [self.zoneId]
        zoneTable.extend(ToontownGlobals.HoodHierarchy.get(self.canonicalHoodId, []))
        return zoneTable

    def startup(self):
        self.createFishingPonds()
        self.createPartyPeople()
        self.createTreasurePlanner()
        self.createBuildingManagers()
        self.createSuitPlanners()

    def shutdown(self):
        if self.treasurePlanner:
            self.treasurePlanner.stop()
            self.treasurePlanner.deleteAllTreasuresNow()
            self.treasurePlanner = None
        for suitPlanner in self.suitPlanners:
            suitPlanner.requestDelete()
            del self.air.suitPlanners[suitPlanner.zoneId]
        self.suitPlanners = []
        for buildingManager in self.buildingManagers:
            buildingManager.cleanup()
            del self.air.buildingManagers[buildingManager.branchId]
        self.buildingManagers = []
        del self.fishingPonds
        for distObj in self.doId2do.values():
            distObj.requestDelete()

    def findFishingPonds(self, dnaGroup, zoneId, area):
        fishingPonds = []
        fishingPondGroups = []
        if isinstance(dnaGroup, DNAGroup) and ('fishing_pond' in dnaGroup.getName()):
            fishingPondGroups.append(dnaGroup)

            fishingPond = DistributedFishingPondAI(simbase.air)
            fishingPond.setArea(area)
            fishingPond.generateWithRequired(zoneId)

            fishingPonds.append(fishingPond)
        elif isinstance(dnaGroup, DNAVisGroup):
            zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)
        for i in range(dnaGroup.getNumChildren()):
            (foundFishingPonds, foundFishingPondGroups) = self.findFishingPonds(dnaGroup.at(i), zoneId, area)
            fishingPonds.extend(foundFishingPonds)
            fishingPondGroups.extend(foundFishingPondGroups)
        return (fishingPonds, fishingPondGroups)

    def findFishingSpots(self, dnaGroup, fishingPond):
        fishingSpots = []
        if isinstance(dnaGroup, DNAGroup) and ('fishing_spot' in dnaGroup.getName()):
            fishingSpot = DistributedFishingSpotAI(simbase.air)
            fishingSpot.setPondDoId(fishingPond.doId)
            x, y, z = dnaGroup.getPos()
            h, p, r = dnaGroup.getHpr()
            fishingSpot.setPosHpr(x, y, z, h, p, r)
            fishingSpot.generateWithRequired(fishingPond.zoneId)

            fishingSpots.append(fishingSpot)
        for i in range(dnaGroup.getNumChildren()):
            foundFishingSpots = self.findFishingSpots(dnaGroup.at(i), fishingPond)
            fishingSpots.extend(foundFishingSpots)
        return fishingSpots

    def createFishingPonds(self):
        self.fishingPonds = []
        fishingPondGroups = []
        for zoneId in self.getZoneTable():
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            if isinstance(dnaData, DNAData):
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                (foundFishingPonds, foundFishingPondGroups) = self.findFishingPonds(dnaData, zoneId, area)
                self.fishingPonds.extend(foundFishingPonds)
                fishingPondGroups.extend(foundFishingPondGroups)
        for fishingPond in self.fishingPonds:
            NPCToons.createNpcsInZone(self.air, fishingPond.zoneId)
        fishingSpots = []
        for (dnaGroup, fishingPond) in zip(fishingPondGroups, self.fishingPonds):
            fishingSpots.extend(self.findFishingSpots(dnaGroup, fishingPond))

    def findPartyGates(self, dnaGroup, zoneId):
        partyGates = []
        if isinstance(dnaGroup, DNAGroup) and ('prop_party_gate' in dnaGroup.getName()):
            partyGate = DistributedPartyGateAI(simbase.air)
            partyGate.setArea(zoneId)
            partyGate.generateWithRequired(zoneId)

            partyGates.append(partyGates)
        for i in range(dnaGroup.getNumChildren()):
            foundPartyGates = self.findPartyGates(dnaGroup.at(i), zoneId)
            partyGates.extend(foundPartyGates)
        return partyGates

    def createPartyPeople(self):
        self.partyGates = []
        for zoneId in self.getZoneTable():
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            if isinstance(dnaData, DNAData):
                foundPartyGates = self.findPartyGates(dnaData, zoneId)
                self.partyGates.extend(foundPartyGates)

    def createTreasurePlanner(self):
        spawnInfo = TreasureGlobals.SafeZoneTreasureSpawns[self.canonicalHoodId]
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = spawnInfo
        self.treasurePlanner = SZTreasurePlannerAI(
            self.canonicalHoodId, treasureType, healAmount, spawnPoints,
            spawnRate, maxTreasures)
        self.treasurePlanner.start()

    def createBuildingManagers(self):
        for zoneId in self.getZoneTable():
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            dnaStore = self.air.dnaStoreMap[zoneId]
            buildingManager = DistributedBuildingMgrAI.DistributedBuildingMgrAI(
                self.air, zoneId, dnaStore, self.air.trophyMgr)
            self.buildingManagers.append(buildingManager)
            self.air.buildingManagers[zoneId] = buildingManager

    def createSuitPlanners(self):
        if not simbase.config.GetBool('want-suit-planners', True):
            return
        for zoneId in self.getZoneTable():
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            suitPlanner = DistributedSuitPlannerAI.DistributedSuitPlannerAI(self.air, zoneId)
            suitPlanner.generateWithRequired(zoneId)
            suitPlanner.d_setZoneId(zoneId)
            suitPlanner.initTasks()
            self.suitPlanners.append(suitPlanner)
            self.air.suitPlanners[zoneId] = suitPlanner
