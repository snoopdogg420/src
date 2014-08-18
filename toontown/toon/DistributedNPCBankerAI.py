from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.estate import BankGlobals

class DistributedNPCBankerAI(DistributedNPCToonBaseAI):
    FourthGagVelvetRopeBan = config.GetBool('want-ban-fourth-gag-velvet-rope', 0)

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.hq = hq
        self.tutorial = 0
        self.pendingAvId = None

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.busy:
            return

        self.busy = avId
        self.sendGUIMovie()
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                self.__handleUnexpectedExit, extraArgs=[avId])
        DistributedNPCToonBaseAI.avatarEnter(self)

    def sendGUIMovie(self):
        taskMgr.doMethodLater(60, self.sendTimeoutMovie,
                              self.uniqueName('clearMovie'))
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_GUI,
         self.busy,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def sendTimeoutMovie(self, task):
        self.pendingAvId = None
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_TIMEOUT,
         self.busy,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        self.busy = 0
        return Task.done

    def sendClearMovie(self, task):
        self.busy = 0
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_CLEAR,
         0,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def rejectAvatar(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_REJECT,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.sendClearMovie(None)
