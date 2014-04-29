from HoodAI import HoodAI
from direct.directnotify import DirectNotifyGlobal
from toontown.building import DistributedCJElevatorAI
from toontown.building import DistributedDoorAI
from toontown.building import DoorTypes
from toontown.building import FADoorCodes
from toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from toontown.coghq import DistributedCogHQDoorAI
from toontown.coghq import DistributedLawOfficeAI
from toontown.coghq import LobbyManagerAI
from toontown.coghq.DistributedLawOfficeElevatorExtAI import DistributedLawOfficeElevatorExtAI
from toontown.suit import DistributedLawbotBossAI
from toontown.toonbase import ToontownGlobals
# from toontown.suit import DistributedSuitPlannerAI


class LawbotHQAI(HoodAI):
    HOOD = ToontownGlobals.LawbotHQ

    def createSafeZone(self):
        # self.createSuitPlanners()

        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(
            self.air, DistributedLawbotBossAI.DistributedLawbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.LawbotLobby)

        self.lobbyElevator = DistributedCJElevatorAI.DistributedCJElevatorAI(
            self.air, self.lobbyMgr, ToontownGlobals.LawbotLobby, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.LawbotLobby)

        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingParty = DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.LawbotLobby)

        self.makeCogHQDoor(ToontownGlobals.LawbotLobby, 0, 1, FADoorCodes.LB_DISGUISE_INCOMPLETE)
        self.makeCogHQDoor(ToontownGlobals.LawbotOfficeExt, 0, 0)

        mins = ToontownGlobals.FactoryLaffMinimums[2]
        lawOfficeId0 = self.makeLawOfficeElevator(0, 0, mins[0])
        lawOfficeId1 = self.makeLawOfficeElevator(1, 0, mins[1])
        lawOfficeId2 = self.makeLawOfficeElevator(2, 0, mins[2])
        lawOfficeId3 = self.makeLawOfficeElevator(3, 0, mins[3])

        lawOfficeIdList = [lawOfficeId0, lawOfficeId1, lawOfficeId2, lawOfficeId3]
        if simbase.config.GetBool('want-boarding-parties', 1):
            self.officeBoardingParty = DistributedBoardingPartyAI(self.air, lawOfficeIdList, 4)
            self.officeBoardingParty.generateWithRequired(ToontownGlobals.LawbotOfficeExt)

    def makeCogHQDoor(self, destinationZone, intDoorIndex, extDoorIndex, lock=0):
        intDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.LawbotHQ,
            doorIndex=intDoorIndex, lockValue=lock)
        intDoor.zoneId = destinationZone

        extDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.EXT_COGHQ, destinationZone,
            doorIndex=extDoorIndex, lockValue=lock)

        extDoor.setOtherDoor(intDoor)
        intDoor.setOtherDoor(extDoor)

        intDoor.generateWithRequired(destinationZone)
        intDoor.sendUpdate('setDoorIndex', [intDoor.getDoorIndex()])

        extDoor.generateWithRequired(ToontownGlobals.LawbotHQ)
        extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

    def makeLawOfficeElevator(self, index, antiShuffle=0, minLaff=0):
        destZone = (
            ToontownGlobals.LawbotStageIntA,
            ToontownGlobals.LawbotStageIntB,
            ToontownGlobals.LawbotStageIntC,
            ToontownGlobals.LawbotStageIntD
        )[index]
        elevator = DistributedLawOfficeElevatorExtAI(
            self.air, self.air.lawOfficeMgr, destZone, index,
            antiShuffle=0, minLaff=minLaff)
        elevator.generateWithRequired(ToontownGlobals.LawbotOfficeExt)
        return elevator.doId

    def createSuitPlanners(self):
        self.suitPlanners = []
        sp = DistributedSuitPlannerAI.DistributedSuitPlannerAI(self.air, ToontownGlobals.LawbotHQ)
        sp.generateWithRequired(ToontownGlobals.LawbotHQ)
        sp.d_setZoneId(ToontownGlobals.LawbotHQ)
        sp.initTasks()
        self.suitPlanners.append(sp)
        # self.air.suitPlanners[zoneId] = sp
