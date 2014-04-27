# For DNAParsing
from DNAParser import DNAVisGroup, DNALandmarkBuilding, DNAStorage, DNAFlatDoor

# For buildings/interiors.
from toontown.building.DistributedToonInteriorAI import DistributedToonInteriorAI
from toontown.building.DistributedToonHallInteriorAI import DistributedToonHallInteriorAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.building.DistributedPetshopInteriorAI import DistributedPetshopInteriorAI
from toontown.building.DistributedGagshopInteriorAI import DistributedGagshopInteriorAI
from toontown.building.DistributedKartShopInteriorAI import DistributedKartShopInteriorAI
from toontown.building.DistributedKnockKnockDoorAI import DistributedKnockKnockDoorAI
from toontown.building import DoorTypes

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
        
    def spawnObjects(self, filename, baseZone):       
        dnaStore = DNAStorage()
        dnaData = simbase.air.loadDNAFileAI(dnaStore, filename)
        self._createObjects(dnaData, baseZone)
        
    def _createObjects(self, group, zone):
        if group.getName()[:13] == 'fishing_pond_':
            visGroup = group.getVisGroup()
            pondZone = 0
            if visGroup is None:
                pondZone = zone
            else:
                pondZone = int(visGroup.getName().split(':')[0])

            pondIndex = int(group.getName()[13:])
            pond = DistributedFishingPondAI(simbase.air)
            pond.setArea(zone)
            pond.generateWithRequired(pondZone)
            #self.ponds[pondIndex] = pond
            
            bingoManager = DistributedPondBingoManagerAI(simbase.air)
            bingoManager.setPondDoId(pond.getDoId())
            bingoManager.generateWithRequired(pondZone)
            #temporary, until we have scheduled stuff
            bingoManager.createGame()
            pond.bingoMgr = bingoManager
            simbase.air.fishManager.ponds[zone] = pond

            for i in range(FishingTargetGlobals.getNumTargets(zone)):
                target = DistributedFishingTargetAI(simbase.air)
                target.setPondDoId(pond.getDoId())
                target.generateWithRequired(pondZone)

            for i in range(group.getNumChildren()):
                posSpot = group.at(i)
                if posSpot.getName()[:13] == 'fishing_spot_':
                    spot = DistributedFishingSpotAI(simbase.air)
                    spot.setPondDoId(pond.getDoId())
                    x, y, z = posSpot.getPos()
                    h, p, r = posSpot.getHpr()
                    spot.setPosHpr(x, y, z, h, p, r)
                    spot.generateWithRequired(pondZone)
                    
            NPCToons.createNpcsInZone(simbase.air, pondZone)
        
        elif isinstance(group, DNALandmarkBuilding):
            if group.getName()[:2] == 'tb' or group.getName()[:2] == 'sz':
                visGroup = group.getVisGroup()
                buildingZone = 0
                if visGroup is None:
                    buildingZone = zone
                else:
                    buildingZone = int(visGroup.getName().split(':')[0])
                index = int(group.getName()[2:].split(':')[0])
                interiorZone = zone + 500 + index
                type = group.getBuildingType()
                if type == 'hq':
                    if buildingZone % 1000 != 0:
                        return # Some bug with HQ DDoors on streets which I'm too lazy to fix right now.
                    hqDoor = DistributedDoorAI(simbase.air, index, DoorTypes.EXT_HQ)
                    hqDoor.zoneId = buildingZone
                    hqDoor.generateWithRequired(buildingZone)
                    
                    hqDoor2 = DistributedDoorAI(simbase.air, index, DoorTypes.EXT_HQ, 1)
                    hqDoor2.zoneId = buildingZone
                    hqDoor2.generateWithRequired(buildingZone)

                    hqDoorInt = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_HQ)
                    hqDoorInt.zoneId = interiorZone
                    hqDoorInt.setOtherDoor(hqDoor)
                    hqDoorInt.generateWithRequired(interiorZone)

                    hqDoorInt2 = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_HQ, 1)
                    hqDoorInt2.zoneId = interiorZone
                    hqDoorInt2.setOtherDoor(hqDoor2)
                    hqDoorInt2.generateWithRequired(interiorZone)

                    hqDoor.setOtherDoor(hqDoorInt)
                    hqDoor2.setOtherDoor(hqDoorInt2)

                    hqInterior = DistributedHQInteriorAI(simbase.air)
                    hqInterior.setZoneIdAndBlock(interiorZone, 0)
                    hqInterior.generateWithRequired(interiorZone)
					
                    NPCToons.createNpcsInZone(simbase.air, interiorZone)
                elif type == 'kartshop':
                    ksInterior = DistributedKartShopInteriorAI(simbase.air)
                    ksInterior.setZoneIdAndBlock(interiorZone, 0)
                    ksInterior.generateWithRequired(interiorZone)
                
                    ksDoor = DistributedDoorAI(simbase.air, 1, DoorTypes.EXT_KS, 1)
                    ksDoor.zoneId = buildingZone
                    ksDoor.generateWithRequired(buildingZone)
                    
                    ksDoor2 = DistributedDoorAI(simbase.air, 1, DoorTypes.EXT_KS, 2)
                    ksDoor2.zoneId = buildingZone
                    ksDoor2.generateWithRequired(buildingZone)
                    
                    ksDoorInt = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_KS, 1)
                    ksDoorInt.zoneId = interiorZone
                    ksDoorInt.setOtherDoor(ksDoor)
                    ksDoorInt.generateWithRequired(interiorZone)

                    ksDoorInt2 = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_KS, 2)
                    ksDoorInt2.zoneId = interiorZone
                    ksDoorInt2.setOtherDoor(ksDoor2)
                    ksDoorInt2.generateWithRequired(interiorZone)
                    
                    ksDoor.setOtherDoor(ksDoorInt)
                    ksDoor2.setOtherDoor(ksDoorInt2)
                    
                    NPCToons.createNpcsInZone(simbase.air, interiorZone)
                elif type == 'petshop':
                    interior = DistributedPetshopInteriorAI(simbase.air)
                    interior.setZoneIdAndBlock(interiorZone, 0)
                    interior.generateWithRequired(interiorZone)
                    
                    extDoor = DistributedDoorAI(simbase.air, index, DoorTypes.EXT_STANDARD, 1)
                    extDoor.zoneId = buildingZone
                    extDoor.generateWithRequired(buildingZone)
                    
                    intDoor = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_STANDARD)
                    intDoor.zoneId = interiorZone
                    intDoor.setOtherDoor(extDoor)
                    intDoor.generateWithRequired(interiorZone)
                    
                    extDoor.setOtherDoor(intDoor)
                    
                    NPCToons.createNpcsInZone(simbase.air, interiorZone)

                elif type == 'gagshop':
                    interior = DistributedGagshopInteriorAI(simbase.air)
                    interior.setZoneIdAndBlock(interiorZone, 0)
                    interior.generateWithRequired(interiorZone)
                    
                    extDoor = DistributedDoorAI(simbase.air, index, DoorTypes.EXT_STANDARD, 1)
                    extDoor.zoneId = buildingZone
                    extDoor.generateWithRequired(buildingZone)
                    
                    intDoor = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_STANDARD)
                    intDoor.zoneId = interiorZone
                    intDoor.setOtherDoor(extDoor)
                    intDoor.generateWithRequired(interiorZone)
                    
                    extDoor.setOtherDoor(intDoor)
                    
                    NPCToons.createNpcsInZone(simbase.air, interiorZone)
                else:
                    if group.getName() == 'sz13:toon_landmark_TT_toonhall_DNARoot':
                        interior = DistributedToonHallInteriorAI(simbase.air)
                        interior.setZoneIdAndBlock(interiorZone, 0)
                        interior.setState('toon')
			interior.generateWithRequired(interiorZone)
						
			extDoor = DistributedDoorAI(simbase.air, index, DoorTypes.EXT_STANDARD)
			extDoor.zoneId = buildingZone
			extDoor.generateWithRequired(buildingZone)
			
			intDoor = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_STANDARD)
			intDoor.zoneId = interiorZone
			intDoor.setOtherDoor(extDoor)
			intDoor.generateWithRequired(interiorZone)
			
			extDoor.setOtherDoor(intDoor)
			
			NPCToons.createNpcsInZone(simbase.air, interiorZone)
                    else:
                        interior = DistributedToonInteriorAI(simbase.air)
                        interior.setZoneIdAndBlock(interiorZone, 0)
                        interior.setState('toon')
                        interior.generateWithRequired(interiorZone)
                        
                        extDoor = DistributedDoorAI(simbase.air, index, DoorTypes.EXT_STANDARD, 1)
                        extDoor.zoneId = buildingZone
                        extDoor.generateWithRequired(buildingZone)
                        
                        intDoor = DistributedDoorAI(simbase.air, 0, DoorTypes.INT_STANDARD)
                        intDoor.zoneId = interiorZone
                        intDoor.setOtherDoor(extDoor)
                        intDoor.generateWithRequired(interiorZone)
                        
                        extDoor.setOtherDoor(intDoor)
                        
                        NPCToons.createNpcsInZone(simbase.air, interiorZone)
        elif isinstance(group, DNAFlatDoor):
            building = group.getParent().getParent()
            index = int(building.getName()[2:].split(':')[0])
            visGroup = group.getVisGroup()
            if visGroup == None:
                doorZone = zone
            else:
                doorZone = int(visGroup.getName().split(':')[0])
            door = DistributedKnockKnockDoorAI(simbase.air)
            door.setPropId(index)
            door.generateWithRequired(doorZone)
        elif group.getName()[:10] == 'racing_pad':
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
        if group.getName()[:15] == 'prop_party_gate':
            gate = DistributedPartyGateAI(simbase.air)
            gate.setArea(zone)
            gate.generateWithRequired(zone)
        for i in range(group.getNumChildren()):
            self._createObjects(group.at(i), zone)