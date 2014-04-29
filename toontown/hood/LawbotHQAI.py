from direct.directnotify import DirectNotifyGlobal
from HoodAI import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.coghq import LobbyManagerAI
from toontown.building import DistributedCJElevatorAI
from toontown.suit import DistributedLawbotBossAI
from toontown.coghq import DistributedLawOfficeElevatorExtAI
from toontown.coghq import DistributedLawOfficeAI
from toontown.building import FADoorCodes
from toontown.building import DistributedBoardingPartyAI
from toontown.building import DistributedDoorAI

class LawbotHQAI(HoodAI):
    HOOD = ToontownGlobals.LawbotHQ

    def createSafeZone(self):
        
        def makeOfficeElevator(index, antiShuffle = 0, minLaff = 0):
            destZone = (ToontownGlobals.LawbotStageIntA, ToontownGlobals.LawbotStageIntB, ToontownGlobals.LawbotStageIntC, ToontownGlobals.LawbotStageIntD)[index]
            elev = DistributedLawOfficeElevatorExtAI.DistributedLawOfficeElevatorExtAI(self.air, self.air.lawOfficeMgr, destZone, index, antiShuffle = 0, minLaff = minLaff)
            elev.generateWithRequired(ToontownGlobals.LawbotOfficeExt)
            return elev.doId

        mins = ToontownGlobals.FactoryLaffMinimums[2]
        officeId0 = makeOfficeElevator(0, 0, mins[0])
        officeId1 = makeOfficeElevator(1, 0, mins[1])
        officeId2 = makeOfficeElevator(2, 0, mins[2])
        officeId3 = makeOfficeElevator(3, 0, mins[3])
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(self.air, DistributedLawbotBossAI.DistributedLawbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.LawbotLobby)
        self.lobbyElevator = DistributedCJElevatorAI.DistributedCJElevatorAI(self.air, self.lobbyMgr, ToontownGlobals.LawbotLobby, antiShuffle = 1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.LawbotLobby)
        
        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.LawbotLobby)
        
        def makeDoor(destinationZone, intDoorIndex, extDoorIndex, lock = 0):
            intDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, self.HOOD, doorIndex = intDoorIndex, lockValue = lock)
            intDoor.zoneId = destinationZone
            extDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex = extDoorIndex, lockValue = lock)
            extDoor.setOtherDoor(intDoor)
            intDoor.setOtherDoor(extDoor)
            intDoor.generateWithRequired(destinationZone)
            intDoor.sendUpdate('setDoorIndex', [intDoor.getDoorIndex()])
            extDoor.generateWithRequired(self.HOOD)
            extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

        makeDoor(ToontownGlobals.LawbotLobby, 0, 1, FADoorCodes.LB_DISGUISE_INCOMPLETE)
        makeDoor(ToontownGlobals.LawbotOfficeExt, 0, 0)
        officeIdList = [officeId0, officeId1, officeId2, officeId3]
        
        if simbase.config.GetBool('want-boarding-parties', 1):
            self.officeBoardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, officeIdList, 4)
            self.officeBoardingParty.generateWithRequired(ToontownGlobals.LawbotOfficeExt)
        
