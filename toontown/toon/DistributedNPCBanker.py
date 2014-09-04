from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.estate import BankGUI, BankGlobals
from toontown.nametag.NametagGlobals import *
from toontown.toonbase import TTLocalizer


class DistributedNPCBanker(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.jellybeanJar = None
        self.bankGUI = None

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupBankingGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.bankGUI:
            self.bankGUI.destroy()
        self.av = None
        base.localAvatar.posCamera(0, 0)

        DistributedNPCToonBase.disable(self)

    def resetClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupBankingGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.bankGUI:
            self.bankGUI.destroy()
        self.clearMat()
        self.startLookAround()
        self.detectAvatars()

    def handleCollisionSphereEnter(self, collEntry):
        self.sendAvatarEnter()
        self.nametag3d.setDepthTest(0)
        base.cr.playGame.getPlace().setState('purchase')
        self.nametag3d.setBin('fixed', 0)

    def sendAvatarEnter(self):
        self.sendUpdate('avatarEnter')

    def setMovie(self, mode, avId, timestamp):
        isLocalToon = avId == base.localAvatar.doId
        timeStamp = globalClockDelta.localElapsedTime(timestamp)
        self.remain = 60 - timeStamp

        self.resetClerk()
        if mode == BankGlobals.BANK_MOVIE_CLEAR:
            if not avId:
                self.setChatAbsolute('', CFSpeech | CFTimeout)
            if isLocalToon:
                self.freeAvatar()
        elif mode == BankGlobals.BANK_MOVIE_TIMEOUT:
            if isLocalToon:
                self.cleanupBankingGUI()
                self.freeAvatar()
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                CFSpeech | CFTimeout)
        elif mode == BankGlobals.BANK_MOVIE_DEPOSIT:
            if isLocalToon:
                self.cleanupBankingGUI()
                self.freeAvatar()
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE,
                CFSpeech | CFTimeout)
        elif mode == BankGlobals.BANK_MOVIE_GUI:
            av = base.cr.doId2do.get(avId)
            if av:
                self.setupAvatars(av)
            if isLocalToon:
                self.hideNametag2d()
                camera.wrtReparentTo(render)
                seq = Sequence((camera.posQuatInterval(1, Vec3(-5, 9, self.getHeight() - 0.5),
                    Vec3(-150, -2, 0), other=self, blendType='easeOut',
                    name=self.uniqueName('lerpCamera'))))
                seq.start()
                taskMgr.doMethodLater(2.0, self.popupBankingGUI,
                    self.uniqueName('popupBankingGUI'))
            self.setChatAbsolute(TTLocalizer.STOREOWNER_BANKING,
                CFSpeech | CFTimeout)

    def __handleBankingDone(self, transactionAmount):
        self.sendUpdate('transferMoney', [transactionAmount])

    def popupBankingGUI(self, task):
        self.accept('bankDone', self.__handleBankingDone)
        self.bankGUI = BankGUI.BankGUI('bankDone')
        return task.done

    def cleanupBankingGUI(self):
        if self.bankGUI:
            self.bankGUI.destroy()
        self.bankGUI = None

    def freeAvatar(self):
        base.localAvatar.posCamera(0, 0)

        if base.cr.playGame.getPlace():
            base.cr.playGame.getPlace().setState('walk')

        self.showNametag2d()
