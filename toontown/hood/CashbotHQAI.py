from direct.directnotify import DirectNotifyGlobal
from HoodAI import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.coghq import LobbyManagerAI
from toontown.building import DistributedCFOElevatorAI
from toontown.suit import DistributedCashbotBossAI
from toontown.building import FADoorCodes
from toontown.building import DistributedBoardingPartyAI
from toontown.coghq.DistributedMintElevatorExtAI import DistributedMintElevatorExtAI

class CashbotHQAI(HoodAI):
    HOOD = ToontownGlobals.CashbotHQ

    def createSafeZone(self):
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(self.air, DistributedCashbotBossAI.DistributedCashbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.CashbotLobby)
        
        self.lobbyElevator = DistributedCFOElevatorAI.DistributedCFOElevatorAI(self.air, self.lobbyMgr, ToontownGlobals.CashbotLobby, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.CashbotLobby)

        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.CashbotLobby)

        destinationZone = ToontownGlobals.CashbotLobby
        extDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=0, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoorList = [extDoor0]
        intDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.CashbotHQ, doorIndex=0)
        intDoor0.setOtherDoor(extDoor0)
        intDoor0.zoneId = ToontownGlobals.CashbotLobby
        for extDoor in extDoorList:
            extDoor.setOtherDoor(intDoor0)
            extDoor.zoneId = ToontownGlobals.CashbotHQ
            extDoor.generateWithRequired(ToontownGlobals.CashbotHQ)
            extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

        intDoor0.generateWithRequired(ToontownGlobals.CashbotLobby)
        intDoor0.sendUpdate('setDoorIndex', [intDoor0.getDoorIndex()])
        
        # Create mints
        mintTypes = [
            ToontownGlobals.CashbotMintIntA,
            ToontownGlobals.CashbotMintIntB,
            ToontownGlobals.CashbotMintIntC,
        ]
        mins = ToontownGlobals.FactoryLaffMinimums[1]
        self.elevators = []
        for index, mintType in enumerate(mintTypes):
            elevator = DistributedMintElevatorExtAI(self.air, self.air.mintMgr, mintType, antiShuffle=0, minLaff=mins[index])
            elevator.generateWithRequired(self.HOOD)
            self.elevators.append(elevator)