from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import *

from toontown.building.DistributedTutorialInteriorAI import DistributedTutorialInteriorAI
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building import DoorTypes, FADoorCodes
from toontown.toon import NPCToons

class TutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TutorialManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.zoneAllocator = self.air.zoneAllocator

        self.currentAllocatedZones = {}

    def requestTutorial(self):
        avId = self.air.getAvatarIdFromSender()

        print 'tutorial request from AvatarId: %s'%(avId)
        zones = self.createTutorial()
        self.enterTutorial(avId, ToontownGlobals.Tutorial, zones[0], zones[1],
                           zones[2])

    def rejectTutorial(self):
        #I have no idea what this is for...
        print 'tutorial reject'

    def requestSkipTutorial(self):
        avId = self.air.getAvatarIdFromSender()
        self.skipTutorialResponse(avId, 1)

    def skipTutorialResponse(self, avId, allOk):
        self.sendUpdateToAvatarId(avId, 'skipTutorialResponse', [allOk])

    def enterTutorial(self, avId, branchZone, streetZone, shopZone, hqZone):
        self.currentAllocatedZones[avId] = (streetZone, shopZone, hqZone)
        self.sendUpdateToAvatarId(avId, 'enterTutorial',
                                  [branchZone, streetZone, shopZone, hqZone])

    def createTutorial(self):
        streetZone = self.zoneAllocator.allocate()
        shopZone = self.zoneAllocator.allocate()
        hqZone = self.zoneAllocator.allocate()

        self.createShop(shopZone, streetZone)
        # self.createHQ(hqZone, streetZone)
        # self.createStreet(streetZone)

        return (streetZone, shopZone, hqZone)

    def createShop(self, shopZone, streetZone):
        shopInterior = DistributedTutorialInteriorAI(2, self.air, shopZone)

        desc = NPCToons.NPCToonDict.get(20000)
        npc = NPCToons.createNPC(self.air, 20000, desc, shopZone)
        npc.setTutorial(1)
        shopInterior.setTutorialNpcId(npc.doId)

        shopInterior.generateWithRequired(shopZone)

        extShopDoor = DistributedDoorAI(self.air, 2, DoorTypes.EXT_STANDARD,
                                        lockValue=FADoorCodes.DEFEAT_FLUNKY_TOM)
        intShopDoor = DistributedDoorAI(self.air, 2, DoorTypes.INT_STANDARD,
                                        lockValue=FADoorCodes.TALK_TO_TOM)
        extShopDoor.setOtherDoor(intShopDoor)
        intShopDoor.setOtherDoor(extShopDoor)
        extShopDoor.zoneId = shopZone
        intShopDoor.zoneId = streetZone
        extShopDoor.generateWithRequired(streetZone)
        intShopDoor.generateWithRequired(shopZone)
        extShopDoor.sendUpdate('setDoorIndex', [extShopDoor.getDoorIndex()])
        intShopDoor.sendUpdate('setDoorIndex', [intShopDoor.getDoorIndex()])

        self.accept(npc.uniqueName('talkToTom'), intShopDoor.setDoorLock, [FADoorCodes.UNLOCKED])

    def createHQ(self, hqZone, streetZone):
        pass

    def createStreet(self, streetZone):
        pass

    def allDone(self):
        avId = self.air.getAvatarIdFromSender()

        #Deallocate zones the Avatar took.
        for zoneId in self.currentAllocatedZones[avId]:
            self.zoneAllocator.free(zoneId)

    def toonArrived(self):
        avId = self.air.getAvatarIdFromSender()

        #Acknowledge the tutorial.


