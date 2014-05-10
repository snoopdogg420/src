from toontown.building import DistributedCFOElevatorAI
from toontown.building import FADoorCodes
from toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
from toontown.coghq.DistributedMintElevatorExtAI import DistributedMintElevatorExtAI
from toontown.hood import CogHQAI
from toontown.suit import DistributedCashbotBossAI
from toontown.toonbase import ToontownGlobals


class CashbotHQAI(CogHQAI.CogHQAI):
    def __init__(self, air):
        CogHQAI.CogHQAI.__init__(
            self, air, ToontownGlobals.CashbotHQ, ToontownGlobals.CashbotLobby,
            FADoorCodes.CB_DISGUISE_INCOMPLETE,
            DistributedCFOElevatorAI.DistributedCFOElevatorAI,
            DistributedCashbotBossAI.DistributedCashbotBossAI)

        self.mintElevators = []
        self.mintBoardingParty = None

        self.startup()

    def startup(self):
        CogHQAI.CogHQAI.startup(self)

        self.createMintElevators()
        if simbase.config.GetBool('want-boarding-groups', True):
            self.createMintBoardingParty()

    def createMintElevators(self):
        destZones = (
            ToontownGlobals.CashbotMintIntA,
            ToontownGlobals.CashbotMintIntB,
            ToontownGlobals.CashbotMintIntC
        )
        mins = ToontownGlobals.FactoryLaffMinimums[1]
        for i in xrange(len(destZones)):
            mintElevator = DistributedMintElevatorExtAI(
                self.air, self.air.mintMgr, destZones[i],
                antiShuffle=0, minLaff=mins[i])
            mintElevator.generateWithRequired(self.zoneId)
            self.mintElevators.append(mintElevator)

    def createMintBoardingParty(self):
        mintIdList = []
        for mintElevator in self.mintElevators:
            mintIdList.append(mintElevator.doId)
        self.mintBoardingParty = DistributedBoardingPartyAI(self.air, mintIdList, 4)
        self.mintBoardingParty.generateWithRequired(self.zoneId)
