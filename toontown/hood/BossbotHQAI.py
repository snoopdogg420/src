from direct.directnotify import DirectNotifyGlobal
from HoodAI import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.coghq import LobbyManagerAI
from toontown.building import DistributedBBElevatorAI
from toontown.suit import DistributedBossbotBossAI
from toontown.building import FADoorCodes
from toontown.building import DistributedBoardingPartyAI
from toontown.coghq.DistributedCogKartAI import DistributedCogKartAI

class BossbotHQAI(HoodAI):
    HOOD = ToontownGlobals.BossbotHQ

    def createSafeZone(self):
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(self.air, DistributedBossbotBossAI.DistributedBossbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.BossbotLobby)
        
        self.lobbyElevator = DistributedBBElevatorAI.DistributedBBElevatorAI(self.air, self.lobbyMgr, ToontownGlobals.BossbotLobby, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.BossbotLobby)

        # self.cogKartA = DistributedCogKartAI(self.air)
        # self.cogKartA.setPosHpr(0, -10, 0, 0, 0, 0)
        # self.cogKartA.setCountryClubId(0)  # ToontownGlobals.BossbotCountryClubIntA
        # self.cogKartA.generateWithRequired(ToontownGlobals.BossbotHQ)

        if simbase.config.GetBool('want-boarding-groups', 1):
            self.boardingParty = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
            self.boardingParty.generateWithRequired(ToontownGlobals.BossbotLobby)
            # self.boardingPartyExt = DistributedBoardingPartyAI.DistributedBoardingPartyAI(self.air, [self.cogKartA.doId], 4)
            # self.boardingPartyExt.generateWithRequired(ToontownGlobals.BossbotHQ)

        destinationZone = ToontownGlobals.BossbotLobby
        extDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, destinationZone, doorIndex=0, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        extDoorList = [extDoor0]
        intDoor0 = DistributedCogHQDoorAI.DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.BossbotHQ, doorIndex=0)
        intDoor0.setOtherDoor(extDoor0)
        intDoor0.zoneId = ToontownGlobals.BossbotLobby
        for extDoor in extDoorList:
            extDoor.setOtherDoor(intDoor0)
            extDoor.zoneId = ToontownGlobals.BossbotHQ
            extDoor.generateWithRequired(ToontownGlobals.BossbotHQ)
            extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

        intDoor0.generateWithRequired(ToontownGlobals.BossbotLobby)
        intDoor0.sendUpdate('setDoorIndex', [intDoor0.getDoorIndex()])
