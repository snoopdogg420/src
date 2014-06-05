from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
import DistributedBankerMgrAI

class DistributedBankerBobNPCAI(DistributedNPCToonBaseAI):
    FourthGagVelvetRopeBan = config.GetBool('want-ban-fourth-gag-velvet-rope', 0)

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.hq = hq
        self.tutorial = 0
        self.pendingAvId = None
        self.bankMgr = DistributedBankerMgrAI.DistributedBankerMgrAI(simbase.air)
        self.bankMgr.generateWithRequired(2514)
        return

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('avatar enter ' + str(avId))
        self.busy = avId
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        DistributedNPCToonBaseAI.avatarEnter(self)
        self.sendUpdate('exitInteraction', [])

    def sendTimeoutMovie(self, task):
        self.pendingAvId = None
        self.pendingQuests = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TIMEOUT,
         self.npcId,
         self.busy,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        self.busy = 0
        return Task.done

    def sendClearMovie(self, task):
        self.pendingAvId = None
        self.pendingQuests = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        self.busy = 0
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_CLEAR,
         self.npcId,
         0,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def rejectAvatar(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_REJECT,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(5.5, self.sendClearMovie, self.uniqueName('clearMovie'))

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.sendClearMovie(None)
        return
