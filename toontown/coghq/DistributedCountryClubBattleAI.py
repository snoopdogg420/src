import CogDisguiseGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.showbase.PythonUtil import addListsByValue
from toontown.battle.BattleBase import *
from toontown.coghq import DistributedLevelBattleAI
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import getCountryClubCreditMultiplier


class DistributedCountryClubBattleAI(DistributedLevelBattleAI.DistributedLevelBattleAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCountryClubBattleAI')

    def __init__(self, air, battleMgr, pos, suit, toonId, zoneId, level, battleCellId, roundCallback = None, finishCallback = None, maxSuits = 4):
        DistributedLevelBattleAI.DistributedLevelBattleAI.__init__(self, air, battleMgr, pos, suit, toonId, zoneId, level, battleCellId, 'CountryClubReward', roundCallback, finishCallback, maxSuits)
        self.battleCalc.setSkillCreditMultiplier(1)
        if self.bossBattle:
            self.level.d_setBossConfronted(toonId)
        self.fsm.addState(State.State('CountryClubReward', self.enterCountryClubReward, self.exitCountryClubReward, ['Resume']))
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
        DistributedLevelBattleAI.DistributedLevelBattleAI.enterResume(self)
        if self.bossBattle and self.bossDefeated:
            self.battleMgr.level.b_setDefeated()

    def enterReward(self):
        DistributedLevelBattleAI.DistributedLevelBattleAI.enterReward(self)
        roomDoId = self.getLevelDoId()
        room = simbase.air.doId2do.get(roomDoId)
        if room:
            room.challengeDefeated()
