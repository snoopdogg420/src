from direct.directnotify.DirectNotifyGlobal import *

# For DNAParsing
from DNAParser import DNAVisGroup, DNALandmarkBuilding, DNAStorage, DNAFlatDoor

# For buildings/interiors.
from toontown.building.DistributedToonInteriorAI import DistributedToonInteriorAI
from toontown.building.DistributedToonHallInteriorAI import DistributedToonHallInteriorAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedPetshopInteriorAI import DistributedPetshopInteriorAI
from toontown.building.DistributedGagshopInteriorAI import DistributedGagshopInteriorAI
from toontown.building.KartShopBuildingAI import KartShopBuildingAI
from toontown.building.DistributedKnockKnockDoorAI import DistributedKnockKnockDoorAI
from toontown.building.DistributedBuildingAI import DistributedBuildingAI
from toontown.building.HQBuildingAI import HQBuildingAI
from toontown.building import DoorTypes

#For Golf
from toontown.safezone.DistributedGolfKartAI import DistributedGolfKartAI

# For Outdoor Playground
from toontown.safezone import DistributedGameTableAI
from toontown.safezone import DistributedPicnicBasketAI

# For GSW playground
from toontown.racing.DistributedRacePadAI import DistributedRacePadAI
from toontown.racing.DistributedViewPadAI import DistributedViewPadAI
from toontown.racing.DistributedStartingBlockAI import DistributedStartingBlockAI, DistributedViewingBlockAI
from toontown.racing import RaceGlobals

# For fishing
from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing import FishingTargetGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI

# For spawning NPCs in zones
from toontown.toon import NPCToons

# Parties
from toontown.safezone.DistributedPartyGateAI import DistributedPartyGateAI

#alfa only
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals

class DNASpawnerAI:
    notify = directNotify.newCategory('DNASpawnerAI')

    def __init__(self):
        self.dnaStore = None
        self.dnaData = None

    def spawnObjects(self, filename, baseZone):
        self.dnaStore = DNAStorage()
        self.dnaData = simbase.air.loadDNAFileAI(self.dnaStore, filename)
        simbase.air.dnaStoreMap[baseZone] = self.dnaStore
        self._createObjects(self.dnaData, baseZone)

    def getDNAStorage(self):
        return self.dnaStore

    def getDNAData(self):
        return self.dnaData

    def _createObjects(self, group, zone):
        if group.getName()[:10] == 'racing_pad':
            index, dest = group.getName()[11:].split('_', 2)
            index = int(index)

            pad = DistributedRacePadAI(simbase.air)
            pad.setArea(zone)
            pad.nameType = dest
            pad.index = index
            nri = RaceGlobals.getNextRaceInfo(-1, dest, index)
            pad.setTrackInfo([nri[0], nri[1]])
            pad.generateWithRequired(zone)
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:14] == 'starting_block':
                    spotIndex = int(posSpot.getName()[15:])
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    startingBlock = DistributedStartingBlockAI(simbase.air)
                    startingBlock.setPosHpr(x, y, z, h, p, r)
                    startingBlock.setPadDoId(pad.getDoId())
                    startingBlock.setPadLocationId(index)
                    startingBlock.generateWithRequired(zone)
                    pad.addStartingBlock(startingBlock)

        elif group.getName()[:10] == 'golf_kart_':
            golfCourse = int(group.getName()[10:].split('_', 2)[0])
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:14] == 'starting_block':
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    golfKart = DistributedGolfKartAI(simbase.air, golfCourse, x, y, z, h, p, r)
                    golfKart.generateWithRequired(ToontownGlobals.GolfZone)
                    golfKart.start()
        elif group.getName()[:11] == 'viewing_pad':
            pad = DistributedViewPadAI(simbase.air)
            pad.setArea(zone)
            pad.generateWithRequired(zone)
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:14] == 'starting_block':
                    spotIndex = int(posSpot.getName()[15:])
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    startingBlock = DistributedViewingBlockAI(simbase.air)
                    startingBlock.setPosHpr(x, y, z, h, p, r)
                    startingBlock.setPadDoId(pad.getDoId())
                    startingBlock.setPadLocationId(0)
                    startingBlock.generateWithRequired(zone)
                    pad.addStartingBlock(startingBlock)
        elif group.getName()[:11] == 'game_table_':
            if not simbase.config.GetBool('want-game-tables', 0):
                return
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if 'game_table' in posSpot.getName():
                    pos = posSpot.getPos()
                    hpr = posSpot.getHpr()
                    gameTable = DistributedGameTableAI.DistributedGameTableAI(simbase.air)
                    gameTable.setPosHpr(pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                    gameTable.generateWithRequired(zone)
        elif group.getName()[:13] == 'picnic_table_':
            nameInfo = group.getName().split('_')
            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if 'picnic_table' in posSpot.getName():
                    pos = posSpot.getPos()
                    hpr = posSpot.getHpr()
                    picnicTable = DistributedPicnicBasketAI.DistributedPicnicBasketAI(
                        simbase.air, nameInfo[2],
                        pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                    picnicTable.generateWithRequired(zone)
                    picnicTable.start()
        for i in range(group.getNumChildren()):
            self._createObjects(group.at(i), zone)
