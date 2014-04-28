from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.coghq.DistributedLevelBattleAI import DistributedLevelBattleAI
from toontown.toonbase import ToontownGlobals
from direct.fsm import State
from toontown.battle.BattleBase import *


class DistributedCountryClubBattleAI(DistributedLevelBattleAI):
    notify = directNotify.newCategory('DistributedCountryClubBattleAI')

    def __init__(self, air, battleMgr, pos, suit, toonId, zoneId, level,
            battleCellId, roundCallback=None, finishCallback=None, maxSuits=4):
        DistributedLevelBattleAI.__init__(
            self, air, battleMgr, pos, suit, toonId, zoneId, level,
            battleCellId, 'CountryClubReward', roundCallback, finishCallback,
            maxSuits)
        self.battleCalc.setSkillCreditMultiplier(1)
        if self.bossBattle:
            self.level.d_setBossConfronted(toonId)
        self.fsm.addState(
            State.State('CountryClubReward', self.enterCountryClubReward,
                        self.exitCountryClubReward, ['Resume'])
        )
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('CountryClubReward')

    def getTaskZoneId(self):
        return self.level.countryClubId

    def handleToonsWon(self, toons):
        extraMerits = [0, 0, 0, 0]
        amount = ToontownGlobals.CountryClubCogBuckRewards[self.level.countryClubId]
        index = ToontownGlobals.cogHQZoneId2deptIndex(self.level.countryClubId)
        extraMerits[index] = amount

    def enterCountryClubReward(self):
        self.joinableFsm.request('Unjoinable')
        self.runableFsm.request('Unrunable')
        self.resetResponses()
        self.assignRewards()
        self.bossDefeated = 1
        self.level.setVictors(self.activeToons[:])
        self.timer.startCallback(BUILDING_REWARD_TIMEOUT, self.serverRewardDone)

    def exitCountryClubReward(self):
        pass

    def enterResume(self):
        DistributedLevelBattleAI.enterResume(self)
        if self.bossBattle and self.bossDefeated:
            self.battleMgr.level.b_setDefeated()
