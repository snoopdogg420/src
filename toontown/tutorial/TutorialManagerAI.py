from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pandac.PandaModules import *
from toontown.building import DistributedDoorAI
from toontown.building import DoorTypes, FADoorCodes
from toontown.building.DistributedHQInteriorAI import DistributedHQInteriorAI
from toontown.building.DistributedTutorialInteriorAI import DistributedTutorialInteriorAI
from toontown.suit import DistributedTutorialSuitAI
from toontown.suit import SuitDNA
from toontown.toon import Experience
from toontown.toon import NPCToons
from toontown.toon.DistributedNPCSpecialQuestGiverAI import DistributedNPCSpecialQuestGiverAI
from toontown.toonbase import ToontownGlobals

class TutorialManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('TutorialManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.zoneAllocator = self.air.zoneAllocator

        self.currentAllocatedZones = {}

    def requestTutorial(self):
        avId = self.air.getAvatarIdFromSender()

        zones = self.createTutorial()
        self.enterTutorial(
            avId, ToontownGlobals.Tutorial,
            zones[0], zones[1], zones[2])

    def rejectTutorial(self):
        avId = self.air.getAvatarIdFromSender()

        av = self.air.doId2do.get(avId)
        if not av:
            return

        self.acceptOnce('generate-%s'%(avId), self.avatarSkipTutorial)
        av.b_setTutorialAck(1)

    def requestSkipTutorial(self):
        avId = self.air.getAvatarIdFromSender()
        self.skipTutorialResponse(avId, 1)

        self.acceptOnce('generate-%s'%(avId), self.avatarSkipTutorial)

    def skipTutorialResponse(self, avId, allOk):
        self.sendUpdateToAvatarId(avId, 'skipTutorialResponse', [allOk])

    def avatarSkipTutorial(self, av):
        av.b_setQuests([[110, 1, 1000, 100, 0]])
        av.b_setQuestHistory([101])
        av.b_setRewardHistory(1, [])
        av.b_setTutorialAck(1)

    def enterTutorial(self, avId, branchZone, streetZone, shopZone, hqZone):
        self.currentAllocatedZones[avId] = (streetZone, shopZone, hqZone)
        self.sendUpdateToAvatarId(avId, 'enterTutorial',
                                  [branchZone, streetZone, shopZone, hqZone])

    def createTutorial(self):
        streetZone = self.zoneAllocator.allocate()
        shopZone = self.zoneAllocator.allocate()
        hqZone = self.zoneAllocator.allocate()

        self.createShop(streetZone, shopZone, hqZone)
        self.createHQ(streetZone, shopZone, hqZone)
        self.createStreet(streetZone, shopZone, hqZone)

        return (streetZone, shopZone, hqZone)

    def createShop(self, streetZone, shopZone, hqZone):
        shopInterior = DistributedTutorialInteriorAI(2, self.air, shopZone)

        desc = NPCToons.NPCToonDict.get(20000)
        npc = NPCToons.createNPC(self.air, 20000, desc, shopZone)
        npc.setTutorial(1)
        shopInterior.setTutorialNpcId(npc.doId)
        shopInterior.generateWithRequired(shopZone)

        extShopDoor = DistributedDoorAI.DistributedDoorAI(self.air, 2, DoorTypes.EXT_STANDARD,
                                        lockValue=FADoorCodes.DEFEAT_FLUNKY_TOM)
        intShopDoor = DistributedDoorAI.DistributedDoorAI(self.air, 2, DoorTypes.INT_STANDARD,
                                        lockValue=FADoorCodes.TALK_TO_TOM)
        extShopDoor.setOtherDoor(intShopDoor)
        intShopDoor.setOtherDoor(extShopDoor)
        extShopDoor.zoneId = streetZone
        intShopDoor.zoneId = shopZone
        extShopDoor.generateWithRequired(streetZone)
        extShopDoor.sendUpdate('setDoorIndex', [extShopDoor.getDoorIndex()])
        intShopDoor.generateWithRequired(shopZone)
        intShopDoor.sendUpdate('setDoorIndex', [intShopDoor.getDoorIndex()])

        self.accept('intShopDoor-{0}'.format(shopZone), intShopDoor.setDoorLock)
        self.accept('extShopDoor-{0}'.format(streetZone), extShopDoor.setDoorLock)

    def createHQ(self, streetZone, shopZone, hqZone):
        interior = DistributedHQInteriorAI(1, self.air, hqZone)
        interior.generateWithRequired(hqZone)
        interior.setTutorial(1)

        desc = NPCToons.NPCToonDict.get(20002)
        npc = NPCToons.createNPC(self.air, 20002, desc, hqZone)
        npc.setTutorial(1)
        npc.setHq(1)

        door0 = DistributedDoorAI.DistributedDoorAI(
            self.air, 1, DoorTypes.EXT_HQ, doorIndex=0,
            lockValue=FADoorCodes.DEFEAT_FLUNKY_HQ)
        door1 = DistributedDoorAI.DistributedDoorAI(
            self.air, 1, DoorTypes.EXT_HQ, doorIndex=1,
            lockValue=FADoorCodes.DEFEAT_FLUNKY_HQ)
        insideDoor0 = DistributedDoorAI.DistributedDoorAI(
            self.air, 1, DoorTypes.INT_HQ, doorIndex=0,
            lockValue=FADoorCodes.TALK_TO_HQ)
        insideDoor1 = DistributedDoorAI.DistributedDoorAI(
            self.air, 1, DoorTypes.INT_HQ, doorIndex=1,
            lockValue=FADoorCodes.TALK_TO_HQ)
        door0.setOtherDoor(insideDoor0)
        insideDoor0.setOtherDoor(door0)
        door1.setOtherDoor(insideDoor1)
        insideDoor1.setOtherDoor(door1)
        door0.zoneId = streetZone
        door1.zoneId = streetZone
        insideDoor0.zoneId = hqZone
        insideDoor1.zoneId = hqZone
        door0.generateWithRequired(streetZone)
        door1.generateWithRequired(streetZone)
        door0.sendUpdate('setDoorIndex', [door0.getDoorIndex()])
        door1.sendUpdate('setDoorIndex', [door1.getDoorIndex()])
        insideDoor0.generateWithRequired(hqZone)
        insideDoor1.generateWithRequired(hqZone)
        insideDoor0.sendUpdate('setDoorIndex', [insideDoor0.getDoorIndex()])
        insideDoor1.sendUpdate('setDoorIndex', [insideDoor1.getDoorIndex()])

        self.accept('extHqDoor0-{0}'.format(streetZone), door0.setDoorLock)
        self.accept('extHqDoor1-{0}'.format(streetZone), door1.setDoorLock)
        self.accept('intHqDoor0-{0}'.format(hqZone), insideDoor0.setDoorLock)
        self.accept('intHqDoor1-{0}'.format(hqZone), insideDoor1.setDoorLock)

    def createStreet(self, streetZone, shopZone, hqZone):
        flunky = DistributedTutorialSuitAI.DistributedTutorialSuitAI(self.air)
        suitType = SuitDNA.getSuitType('f')
        suitTrack = SuitDNA.getSuitDept('f')
        flunky.setupSuitDNA(1, suitType, suitTrack)
        flunky.generateWithRequired(streetZone)

        desc = NPCToons.NPCToonDict.get(20001)
        npc = NPCToons.createNPC(self.air, 20001, desc, streetZone)
        npc.setTutorial(1)
        npc.d_setPos(207.4, 18.81, -0.475)
        npc.d_setHpr(90.0, 0, 0)

    def allDone(self):
        avId = self.air.getAvatarIdFromSender()

        av = self.air.doId2do.get(avId)
        if not av:
            return

        av.b_setTutorialAck(1)

        allocatedZones = self.currentAllocatedZones.get(avId)
        if not allocatedZones:
            return

        streetZone, shopZone, hqZone = allocatedZones
        del self.currentAllocatedZones[avId]

        self.ignore('intShopDoor-{0}'.format(shopZone))
        self.ignore('extShopDoor-{0}'.format(streetZone))
        self.ignore('extHqDoor0-{0}'.format(streetZone))
        self.ignore('extHqDoor1-{0}'.format(streetZone))
        self.ignore('intHqDoor0-{0}'.format(hqZone))
        self.ignore('intHqDoor1-{0}'.format(hqZone))

        self.zoneAllocator.free(streetZone)
        self.zoneAllocator.free(shopZone)
        self.zoneAllocator.free(hqZone)

    def toonArrived(self):
        avId = self.air.getAvatarIdFromSender()

        av = self.air.doId2do.get(avId)
        if not av:
            return

        av.b_setTutorialAck(0)

        av.b_setHp(15)
        av.b_setMaxHp(15)

        experience = Experience.Experience(av.getExperience(), av)
        for i, track in enumerate(av.getTrackAccess()):
            if track:
                experience.experience[i] = 0
        av.b_setExperience(experience.makeNetString())

        av.b_setTrackAccess([0, 0, 0, 0, 1, 1, 0])
        av.b_setMaxCarry(20)

        inventory = av.inventory
        inventory.zeroInv(killUber=1)
        inventory.inventory[4][0] = 1
        inventory.inventory[5][0] = 1
        av.b_setInventory(inventory.makeNetString())

        av.b_setMoney(0)
        av.b_setBankMoney(0)

        av.b_setQuestCarryLimit(1)
        av.b_setQuests([])
        av.b_setQuestHistory([])
        av.b_setRewardHistory(0, [])
