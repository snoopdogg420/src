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
        self.task = ''

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.busy:
            self.sendClearMovie(av=avId)
            return

        self.busy = avId
        self.sendGUIMovie()
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                self.__handleUnexpectedExit, extraArgs=[avId])
        DistributedNPCToonBaseAI.avatarEnter(self)

    def transferMoney(self, transactionAmount):
        av = self.air.doId2do.get(self.busy)
        if not av:
            return

        money = min(av.getMoney() - transactionAmount, 10000)
        av.b_setMoney(money)

        if transactionAmount != 0:
            self.air.bankManager.setMoney(self.busy,
                av.getBankMoney() + transactionAmount)

        self.clearTasks()
        self.sendDoneMovie()

    def sendGUIMovie(self):
        if self.task:
            taskMgr.remove(self.task)

        self.task = self.uniqueName('timeoutMovie')
        taskMgr.doMethodLater(60, self.sendTimeoutMovie,
                              self.task)
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_GUI,
         self.busy,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def sendTimeoutMovie(self, task=None):
        self.pendingAvId = None
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_TIMEOUT,
         self.busy,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.busy = 0

        if self.task:
            taskMgr.remove(self.task)

        self.task = self.uniqueName('clearMovie')
        taskMgr.doMethodLater(5.5, self.sendClearMovie,
            self.task)

        if task is not None:
            return task.done

    def sendClearMovie(self, task=None, av=0):
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_CLEAR,
         av,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

        if task is not None:
            return task.done

    def sendDoneMovie(self):
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_DEPOSIT,
         self.busy,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.busy = 0

        if self.task:
            taskMgr.remove(self.task)

        self.task = self.uniqueName('clearMovie')
        taskMgr.doMethodLater(5.5, self.sendClearMovie, self.task)

    def rejectAvatar(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [BankGlobals.BANK_MOVIE_REJECT,
         avId,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.clearTasks()
        self.sendTimeoutMovie()

    def clearTasks(self):
        if self.task:
            taskMgr.remove(self.task)

        self.task = None
