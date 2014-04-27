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
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(self.air, DistributedLawbotBossAI.DistributedLawbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.LawbotLobby)
        
        self.lobbyElevator = DistributedCJElevatorAI.DistributedCJElevatorAI(self.air, self.lobbyMgr, ToontownGlobals.LawbotLobby, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.LawbotLobby)

        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.LawbotLobby)

        destinationZone = ToontownGlobals.LawbotLobby
        extDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=1, lockValue=FADoorCodes.LB_DISGUISE_INCOMPLETE)
        extDoorList = [extDoor0]
        intDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.LawbotHQ, doorIndex=0)
        intDoor0.setOtherDoor(extDoor0)
        intDoor0.zoneId = ToontownGlobals.LawbotLobby
        
        for extDoor in extDoorList:
            extDoor.setOtherDoor(intDoor0)
            extDoor.zoneId = ToontownGlobals.LawbotHQ
            extDoor.generateWithRequired(ToontownGlobals.LawbotHQ)
            extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

        intDoor0.generateWithRequired(ToontownGlobals.LawbotLobby)
        intDoor0.sendUpdate('setDoorIndex', [intDoor0.getDoorIndex()])
        
        #DA Office elevator
        officeTypes = [
            ToontownGlobals.LawbotStageIntA,
            ToontownGlobals.LawbotStageIntB,
            ToontownGlobals.LawbotStageIntC,
            ToontownGlobals.LawbotStageIntD
            ]
        mins = ToontownGlobals.FactoryLaffMinimums[2]
        elevators = []
        
        for index, officeType in enumerate(officeTypes):
            elevator = DistributedLawOfficeElevatorExtAI.DistributedLawOfficeElevatorExtAI(self.air, self.air.officeMgr, officeType, index, antiShuffle=0, minLaff=mins[index])
            elevator.generateWithRequired(ToontownGlobals.LawbotOfficeExt)
            elevators.append(elevator)
            
        #Boarding groups for DA offices    
        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingOfficeParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [elevators[0].doId, elevators[1].doId, elevators[2].doId, elevators[3].doId], 4)
            self.boardingOfficeParty.generateWithRequired(ToontownGlobals.LawbotOfficeExt)
        
        #DA Office waiting area
        extDoor0 = DistributedDoorAI.DistributedDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, doorIndex=0)
        intDoor0 = DistributedDoorAI.DistributedDoorAI(self.air, 1, DoorTypes.INT_COGHQ, doorIndex=0)
        intDoor0.setOtherDoor(extDoor0)
        intDoor0.zoneId = ToontownGlobals.LawbotOfficeExt
        
        extDoor0.setOtherDoor(intDoor0)
        extDoor0.zoneId = ToontownGlobals.LawbotHQ
        extDoor0.generateWithRequired(ToontownGlobals.LawbotHQ)
        extDoor0.sendUpdate('setDoorIndex', [extDoor0.getDoorIndex()])

        intDoor0.generateWithRequired(ToontownGlobals.LawbotOfficeExt)
        intDoor0.sendUpdate('setDoorIndex', [intDoor0.getDoorIndex()])
