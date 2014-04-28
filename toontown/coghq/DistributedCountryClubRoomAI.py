from direct.directnotify.DirectNotifyGlobal import *
from otp.level.DistributedLevelAI import DistributedLevelAI
from toontown.coghq import CountryClubRoomBase
from toontown.coghq import CountryClubRoomSpecs
from otp.level import LevelSpec
from toontown.coghq import LevelSuitPlannerAI
from toontown.suit import DistributedFactorySuitAI
from toontown.coghq import DistributedCountryClubBattleAI
from toontown.coghq import FactoryEntityCreatorAI


class DistributedCountryClubRoomAI(DistributedLevelAI, CountryClubRoomBase.CountryClubRoomBase):
    notify = directNotify.newCategory('DistributedCountryClubRoomAI')

    def __init__(self, air, countryClubId, countryClubDoId, zoneId, roomId,
            roomNum, avIds, battleExpAggreg):
        DistributedLevelAI.__init__(self, air, zoneId, 0, avIds)
        CountryClubRoomBase.CountryClubRoomBase.__init__(self)

        self.setCountryClubId(countryClubId)
        self.setRoomId(roomId)
        self.roomNum = roomNum
        self.countryClubDoId = countryClubDoId
        self.battleExpAggreg = battleExpAggreg

    def createEntityCreator(self):
        return FactoryEntityCreatorAI.FactoryEntityCreatorAI(level=self)

    def getBattleCreditMultiplier(self):
        return ToontownBattleGlobals.getCountryClubCreditMultiplier(self.countryClubId)

    def generate(self):
        specModule = CountryClubRoomSpecs.getCountryClubRoomSpecModule(self.roomId)
        roomSpec = LevelSpec.LevelSpec(specModule)
        DistributedLevelAI.generate(self, roomSpec)
        cogSpecModule = CountryClubRoomSpecs.getCogSpecModule(self.roomId)
        self.planner = LevelSuitPlannerAI.LevelSuitPlannerAI(
            self.air, self, DistributedFactorySuitAI.DistributedFactorySuitAI,
            DistributedCountryClubBattleAI.DistributedCountryClubBattleAI, cogSpecModule.CogData,
            cogSpecModule.ReserveCogData, cogSpecModule.BattleCells,
            battleExpAggreg=self.battleExpAggreg)
        suitHandles = self.planner.genSuits()
        messenger.send('plannerCreated-' + str(self.doId))
        self.suits = suitHandles['activeSuits']
        self.reserveSuits = suitHandles['reserveSuits']
        self.d_setSuits()

    def delete(self):
        suits = self.suits
        for reserve in self.reserveSuits:
            suits.append(reserve[0])
        self.planner.destroy()
        del self.planner
        for suit in suits:
            if not suit.isDeleted():
                suit.factoryIsGoingDown()
                suit.requestDelete()
        del self.battleExpAggreg
        DistributedLevelAI.delete(self, deAllocZone=False)

    def getCountryClubId(self):
        return self.countryClubId

    def getRoomId(self):
        return self.roomId

    def getRoomNum(self):
        return self.roomNum

    def getCogLevel(self):
        return self.cogLevel

    def d_setSuits(self):
        self.sendUpdate('setSuits', [self.getSuits(), self.getReserveSuits()])

    def getSuits(self):
        suitIds = []
        for suit in self.suits:
            suitIds.append(suit.doId)
        return suitIds

    def getReserveSuits(self):
        suitIds = []
        for suit in self.reserveSuits:
            suitIds.append(suit[0].doId)
        return suitIds

    def d_setBossConfronted(self, toonId):
        if toonId not in self.avIdList:
            return
        self.sendUpdate('setBossConfronted', [toonId])

    def setVictors(self, victorIds):
        activeVictors = []
        activeVictorIds = []
        for victorId in victorIds:
            toon = self.air.doId2do.get(victorId)
            if toon is not None:
                activeVictors.append(toon)
                activeVictorIds.append(victorId)
        # TODO: Make an interesting server event here.
        for toon in activeVictors:
            # simbase.air.questManager.toonDefeatedMint(toon, self.mintId, activeVictors)
            pass

    def b_setDefeated(self):
        self.d_setDefeated()
        self.setDefeated()

    def d_setDefeated(self):
        self.sendUpdate('setDefeated')

    def setDefeated(self):
        pass

    def forceOuch(self, hp):
        pass

    def allToonsGone(self, toonsThatCleared):
        DistributedLevelAI.allToonsGone(self, toonsThatCleared)
        if self.roomNum == 0:
            countryClub = self.air.doId2do.get(self.countryClubDoId)
            if countryClub is not None:
                countryClub.allToonsGone()

    def challengeDefeated(self):
        pass
