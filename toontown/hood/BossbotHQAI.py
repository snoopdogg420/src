from toontown.building import DistributedBBElevatorAI
from toontown.building import DoorTypes
from toontown.building import FADoorCodes
from toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from toontown.coghq import DistributedCogHQDoorAI
from toontown.coghq import DistributedCogKartAI
from toontown.coghq import LobbyManagerAI
from toontown.hood import HoodAI
from toontown.suit import DistributedBossbotBossAI
from toontown.toonbase import ToontownGlobals


class BossbotHQAI(HoodAI.HoodAI):
    def __init__(self, air):
        self.air = air
        self.zoneId = ToontownGlobals.BossbotHQ
        self.canonicalHoodId = ToontownGlobals.BossbotHQ

        self.lobbyMgr = None
        self.lobbyElevator = None
        self.cogKarts = []

        self.notify.info('Creating objects... BossbotHQAI')
        self.startup()

    def startup(self):
        self.createLobbyManager()
        self.createLobbyElevator()
        self.makeCogHQDoor(
            ToontownGlobals.BossbotLobby, 0, 0,
            FADoorCodes.BB_DISGUISE_INCOMPLETE)
        self.createCogKarts()
        if simbase.config.GetBool('want-boarding-groups', True):
            self.createBoardingParties()

    def createLobbyManager(self):
        self.lobbyMgr = LobbyManagerAI.LobbyManagerAI(
            self.air, DistributedBossbotBossAI.DistributedBossbotBossAI)
        self.lobbyMgr.generateWithRequired(ToontownGlobals.BossbotLobby)

    def createLobbyElevator(self):
        self.lobbyElevator = DistributedBBElevatorAI.DistributedBBElevatorAI(
            self.air, self.lobbyMgr, ToontownGlobals.BossbotLobby, antiShuffle=1)
        self.lobbyElevator.generateWithRequired(ToontownGlobals.BossbotLobby)

    def makeCogHQDoor(self, destinationZone, intDoorIndex, extDoorIndex, lock=0):
        intDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.BossbotHQ,
            doorIndex=intDoorIndex, lockValue=lock)
        intDoor.zoneId = destinationZone

        extDoor = DistributedCogHQDoorAI.DistributedCogHQDoorAI(
            self.air, 0, DoorTypes.EXT_COGHQ, destinationZone,
            doorIndex=extDoorIndex, lockValue=lock)

        extDoor.setOtherDoor(intDoor)
        intDoor.setOtherDoor(extDoor)

        intDoor.generateWithRequired(destinationZone)
        intDoor.sendUpdate('setDoorIndex', [intDoor.getDoorIndex()])

        extDoor.generateWithRequired(ToontownGlobals.BossbotHQ)
        extDoor.sendUpdate('setDoorIndex', [extDoor.getDoorIndex()])

    def createCogKarts(self):
        posList = (
            (154.762, 37.169, 0), (141.403, -81.887, 0),
            (-48.44, 15.308, 0)
        )
        hprList = ((110.815, 0, 0), (61.231, 0, 0), (-105.481, 0, 0))
        mins = ToontownGlobals.FactoryLaffMinimums[3]
        for cogCourse in xrange(len(posList)):
            pos = posList[cogCourse]
            hpr = hprList[cogCourse]
            cogKart = DistributedCogKartAI.DistributedCogKartAI(
                self.air, cogCourse, pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2],
                self.air.countryClubMgr, minLaff=mins[cogCourse])
            cogKart.generateWithRequired(ToontownGlobals.BossbotHQ)
            self.cogKarts.append(cogKart)

    def createBoardingParties(self):
        self.boardingParty = DistributedBoardingPartyAI(self.air, [self.lobbyElevator.doId], 8)
        self.boardingParty.generateWithRequired(ToontownGlobals.BossbotLobby)
        cogKartIdList = []
        for cogKart in self.cogKarts:
            cogKartIdList.append(cogKart.doId)
        self.courseBoardingParty = DistributedBoardingPartyAI(self.air, cogKartIdList, 4)
        self.courseBoardingParty.generateWithRequired(ToontownGlobals.BossbotHQ)
