from direct.directnotify import DirectNotifyGlobal
from HoodAI import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.coghq import LobbyManagerAI
from toontown.building import DistributedCFOElevatorAI
from toontown.suit import DistributedCashbotBossAI
from toontown.building import FADoorCodes
from toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from toontown.coghq.DistributedMintElevatorExtAI import DistributedMintElevatorExtAI

class CashbotHQAI(HoodAI):
    HOOD = ToontownGlobals.CashbotHQ

    def createSafeZone(self):
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(
            self.air, DistributedCashbotBossAI.DistributedCashbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.CashbotLobby)

        self.lobbyElevator = DistributedCFOElevatorAI.DistributedCFOElevatorAI(
            self.air, self.lobbyMgr, ToontownGlobals.CashbotLobby, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.CashbotLobby)

        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingParty = DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.CashbotLobby)

        destinationZone = ToontownGlobals.CashbotLobby
        extDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.EXT_COGHQ, destinationZone,
            doorIndex=0, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoorList = [extDoor0]
        intDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.CashbotHQ,
            doorIndex=0)
        intDoor0.setOtherDoor(extDoor0)
        intDoor0.zoneId = ToontownGlobals.CashbotLobby
        for extDoor in extDoorList:
            extDoor.setOtherDoor(intDoor0)
            extDoor.zoneId = ToontownGlobals.CashbotHQ
            extDoor.generateWithRequired(ToontownGlobals.CashbotHQ)
            extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])
        intDoor0.generateWithRequired(ToontownGlobals.CashbotLobby)
        intDoor0.sendUpdate('setDoorIndex', [intDoor0.getDoorIndex()])

        mins = ToontownGlobals.FactoryLaffMinimums[1]
        self.mintElevator0 = DistributedMintElevatorExtAI(
            self.air, self.air.mintMgr, ToontownGlobals.CashbotMintIntA,
            antiShuffle=0, minLaff=mins[0])
        self.mintElevator0.generateWithRequired(ToontownGlobals.CashbotHQ)
        self.mintElevator1 = DistributedMintElevatorExtAI(
            self.air, self.air.mintMgr, ToontownGlobals.CashbotMintIntB,
            antiShuffle=0, minLaff=mins[1])
        self.mintElevator1.generateWithRequired(ToontownGlobals.CashbotHQ)
        self.mintElevator2 = DistributedMintElevatorExtAI(
            self.air, self.air.mintMgr, ToontownGlobals.CashbotMintIntC,
            antiShuffle=0, minLaff=mins[2])
        self.mintElevator2.generateWithRequired(ToontownGlobals.CashbotHQ)

        mintIdList = [
            self.mintElevator0.doId, self.mintElevator1.doId,
            self.mintElevator2.doId
        ]
        if simbase.config.GetBool('want-boarding-groups', 1):
            self.mintBoardingParty = DistributedBoardingPartyAI(self.air, mintIdList, 4)
            self.mintBoardingParty.generateWithRequired(ToontownGlobals.CashbotHQ)
