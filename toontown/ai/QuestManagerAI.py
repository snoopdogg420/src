from toontown.quest import Quests

#REMINDER:
#QUEST = [questId, toNpc, hood, progress, completed]

class QuestManagerAI():
    
    def __init__(self, air):
        self.air = air
    
    def requestInteract(self, avId, npc):
        toon = self.air.doId2do[avId]
        toonQuestPocketSize = toon.getQuestCarryLimit()
        
        currentQuests = toon.getQuests()
        
        if (npc.npcId == ''):
            pass
        elif (len(currentQuests) == toonQuestPocketSize):
            npc.rejectAvatar(avId)
        elif (len(currentQuests) != toonQuestPocketSize):
            quests = self.avatarQuestChoice(toon, npc)
            npc.presentQuestChoice(avId, quests)
            
    def avatarQuestChoice(self, toon, npc):
        tasks = Quests.chooseBestQuests(Quests.DD_TIER, npc, toon)
        return tasks
    
    def avatarCancelled(self, avId):
        pass
    
    def avatarChoseQuest(self, avId, npc, questId, rewardId, building):
        toon = self.air.doId2do[avId]
        fromNpc = Quests.QuestDict[questId][Quests.QuestDictFromNpcIndex]
        toNpc = Quests.QuestDict[questId][Quests.QuestDictToNpcIndex]
        
        toon.addQuest([questId, fromNpc, toNpc, rewardId, 0], Quests.getFinalRewardId(questId))
        npc.assignQuest(avId, questId, rewardId, toNpc)
            
    def avatarChoseTrack(self, avId, pendingTrackQuest, trackId):
        pass
        
    def toonMadeFriend(self, avId, otherAvId):
        pass
    
    