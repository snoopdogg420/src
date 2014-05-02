from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedTrophyMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedTrophyMgrAI')
    AVATAR_ID = 0
    NAME = 1
    SCORE = 2

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.leaderInfo = [[], [], []]
        self.trophyScores = {}

    def requestTrophyScore(self):
        avId = self.air.getAvatarIdFromSender()
        trophyScore = self.trophyScores.get(avId, 0)
        av = self.air.doId2do.get(avId)
        if av:
            av.d_setTrophyScore(trophyScore)

    def getLeaderInfo(self):
        return self.leaderInfo

    def updateTrophyScore(self, avId, trophyScore):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        self.trophyScores[avId] = trophyScore
        if len(self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID]) < 10:
            if avId not in self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID]:
                self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID].append(avId)
                self.leaderInfo[DistributedTrophyMgrAI.NAME].append(av.getName())
                self.leaderInfo[DistributedTrophyMgrAI.SCORE].append(trophyScore)
            else:
                scoreIndex = self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID].index(avId)
                self.leaderInfo[DistributedTrophyMgrAI.SCORE][scoreIndex] = trophyScore
        else:
            if trophyScore > min(self.leaderInfo[DistributedTrophyMgrAI.SCORE]):
                self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID][-1] = avId
                self.leaderInfo[DistributedTrophyMgrAI.NAME][-1] = av.getName()
                self.leaderInfo[DistributedTrophyMgrAI.SCORE][-1] = trophyScore
        self.organizeLeaderInfo()

    def organizeLeaderInfo(self):
        leaderInfo = zip(*reversed(self.leaderInfo))
        leaderInfo.sort(reverse=True)
        self.leaderInfo = [[], [], []]
        for score, name, avId in leaderInfo:
            self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID].append(avId)
            self.leaderInfo[DistributedTrophyMgrAI.NAME].append(name)
            self.leaderInfo[DistributedTrophyMgrAI.SCORE].append(score)
