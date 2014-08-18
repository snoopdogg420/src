from pandac.PandaModules import *
from DistributedNPCToonBase import *
from otp.nametag.NametagConstants import *
from toontown.estate import BankGUI, BankGlobals
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from otp.nametag.NametagConstants import *
from toontown.toonbase import TTLocalizer

class DistributedNPCBanker(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.jellybeanJar = None
        self.bankGUI = None

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

        if mode == BankGlobals.BANK_MOVIE_TIMEOUT:
            av = base.cr.doId2do.get(avId)
            if av:
                self.putAwayJellybeanJar(av)
            if isLocalToon:
                self.cleanupBankingGUI()
                self.freeAvatar()
                self.detectAvatars()
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG,
                CFSpeech | CFTimeout)
        elif mode == BankGlobals.BANK_MOVIE_GUI:
            av = base.cr.doId2do.get(avId)
            if av:
                self.setupAvatars(av)
                self.takeOutJellybeanJar(av)
            if isLocalToon:
                camera.wrtReparentTo(render)
                seq = Sequence((camera.posQuatInterval(1, Vec3(-5, 9, self.getHeight() - 0.5),
                    Vec3(-150, -2, 0), other=self, blendType='easeOut',
                    name=self.uniqueName('lerpCamera'))))
                seq.start()
                taskMgr.doMethodLater(2.0, self.popupBankingGUI,
                    self.uniqueName('popupBankingGUI'))
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GREETING,
                CFSpeech | CFTimeout)

    def takeOutJellybeanJar(self, av):
        #av.getJar()
        pass

    def putAwayJellbeanJar(self, av):
        #av.removeJar()
        pass

    def __handleBankingDone(self, transactionAmount):
        self.sendUpdate('transferMoney', [transactionAmount])

    def popupBankingGUI(self, task):
        self.accept('bankDone', self.__handleBankingDone)
        self.bankGUI = BankGUI.BankGui('bankDone')
        return task.done

    def cleanupBankingGUI(self):
        if self.bankGUI:
            self.bankGUI.destroy()
        self.bankGUI = None
