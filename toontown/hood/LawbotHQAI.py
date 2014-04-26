from direct.directnotify import DirectNotifyGlobal
from HoodAI import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.coghq import LobbyManagerAI
from toontown.building import DistributedCJElevatorAI
from toontown.suit import DistributedLawbotBossAI
from toontown.building import FADoorCodes
from toontown.building import DistributedBoardingPartyAI

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
        extDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=1, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
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
        