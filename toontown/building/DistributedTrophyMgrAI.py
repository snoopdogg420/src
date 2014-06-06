from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedTrophyMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedTrophyMgrAI')
    AVATAR_ID = 0
    NAME = 1
    SCORE = 2

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        backup = self.load()
        self.leaderInfo = backup[0]
        self.trophyScores = backup[1]

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
        if trophyScore <= 0:
            if avId in self.trophyScores:
                del self.trophyScores[avId]
            if avId in self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID]:
                scoreIndex = self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID].index(avId)
                del self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID][scoreIndex]
                del self.leaderInfo[DistributedTrophyMgrAI.NAME][scoreIndex]
                del self.leaderInfo[DistributedTrophyMgrAI.SCORE][scoreIndex]
            for avId in self.trophyScores:
                if avId not in self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID]:
                    self.updateTrophyScore(avId, self.trophyScores[avId])
        self.trophyScores[avId] = trophyScore
        if len(self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID]) < 10:
            if avId not in self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID]:
                self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID].append(avId)
                self.leaderInfo[DistributedTrophyMgrAI.NAME].append(av.getName())
                self.leaderInfo[DistributedTrophyMgrAI.SCORE].append(trophyScore)
            else:
                scoreIndex = self.leaderInfo[DistributedTrophyMgrAI.AVATAR_ID].index(avId)
                self.leaderInfo[DistributedTrophyMgrAI.SCORE][scoreIndex] = trophyScore
            self.organizeLeaderInfo()
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

    def addTrophy(self, avId, name, numFloors):
        if avId in self.trophyScores:
            trophyScore = self.trophyScores[avId] + numFloors
            self.updateTrophyScore(avId, trophyScore)

    def removeTrophy(self, avId, numFloors):
        if avId in self.trophyScores:
            trophyScore = self.trophyScores[avId] - numFloors
            self.updateTrophyScore(avId, trophyScore)

    def save(self):
        simbase.backups.save('trophy-mgr', (simbase.air.districtId,), (self.leaderInfo, self.trophyScores))

    def load(self):
        return simbase.backups.load('trophy-mgr', (simbase.air.districtId,), default=([[], [], []], {}))
