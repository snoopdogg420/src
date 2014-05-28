from direct.directnotify.DirectNotifyGlobal import *
from pandac.PandaModules import *
from toontown.battle import BattleManagerAI
from toontown.building import FADoorCodes
from toontown.suit import SuitDialog
from toontown.suit.DistributedSuitBaseAI import DistributedSuitBaseAI
from toontown.tutorial.DistributedBattleTutorialAI import DistributedBattleTutorialAI


class DistributedTutorialSuitAI(DistributedSuitBaseAI):
    notify = directNotify.newCategory('DistributedTutorialSuitAI')

    def __init__(self, air):
        DistributedSuitBaseAI.__init__(self, air, None)

        self.battleMgr = BattleManagerAI.BattleManagerAI(self.air)
        self.battleMgr.battleConstructor = DistributedBattleTutorialAI

    def requestBattle(self, x, y, z, h, p, r):
        toonId = self.air.getAvatarIdFromSender()
        if self.air.doId2do.get(toonId) is None:
            return
        self.confrontPos = Point3(x, y, z)
        self.confrontHpr = Vec3(h, p, r)
        toon = self.air.doId2do.get(toonId)
        if toon.getBattleId() > 0:
            self.notify.warning('We tried to request a battle when the toon was already in battle')
            self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))
            self.d_denyBattle(toonId)
            return
        pos = Point3(35, 20, -0.5)
        interactivePropTrackBonus = -1
        self.battleMgr.newBattle(
            self.zoneId, self.zoneId, pos, self, toonId, self.__battleFinished,
            1, interactivePropTrackBonus)

    def __battleFinished(self, zoneId):
        messenger.send('extShopDoor-{0}'.format(zoneId), [FADoorCodes.TALK_TO_HQ])
        messenger.send('extHqDoor0-{0}'.format(zoneId), [FADoorCodes.UNLOCKED])
        messenger.send('extHqDoor1-{0}'.format(zoneId), [FADoorCodes.UNLOCKED])

    def getConfrontPosHpr(self):
        return (self.confrontPos, self.confrontHpr)
