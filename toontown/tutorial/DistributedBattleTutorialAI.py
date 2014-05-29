from direct.directnotify.DirectNotifyGlobal import *
from toontown.battle.DistributedBattleAI import DistributedBattleAI


class DistributedBattleTutorialAI(DistributedBattleAI):
    notify = directNotify.newCategory('DistributedBattleTutorialAI')

    def __init__(self, air, battleMgr, pos, suit, toonId, zoneId,
                 finishCallback=None, maxSuits=4, tutorialFlag=1, levelFlag=0,
                 interactivePropTrackBonus=-1):
        DistributedBattleAI.__init__(self, air, battleMgr, pos, suit, toonId,
            zoneId, finishCallback=finishCallback, maxSuits=maxSuits,
            tutorialFlag=1, levelFlag=0,
            interactivePropTrackBonus=interactivePropTrackBonus)

    def startRewardTimer(self):
        pass  # We don't want a reward timer in the tutorial.
