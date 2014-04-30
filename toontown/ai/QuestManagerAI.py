from toontown.quest import Quests

class QuestManagerAI():
    
    def __init__(self, air):
        self.air = air

    def requestInteract(self, avId, npc):
        toon = self.air.doId2do.get(avId)
        if not toon:
            return
        toonQuestPocketSize = toon.getQuestCarryLimit()
        
        toonQuests = toon.getQuests()
        
        if (len(toonQuests) >= 5*toonQuestPocketSize):
            npc.rejectAvatar(avId)
        else:
            for i in range(0, len(toonQuests), 5):
                questDesc = toonQuests[i:i + 5]
                questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc            
                questClass = Quests.getQuest(questId)
                
                #Completed Quest?
                if questClass.getCompletionStatus(toon, questDesc, npc):
                    if isinstance(questClass, Quests.TrackChoiceQuest):
                        npc.presentTrackChoice(avId, questId, 0)
                    else:
                        npc.completeQuest(avId, questId, rewardId)
                    break
                #Needed NPC?
                elif npc.npcId == toNpcId:
                    break
            else:
                npc.presentQuestChoice(avId, self.avatarQuestChoice(toon, npc))

            
    def avatarQuestChoice(self, toon, npc):
        tasks = Quests.chooseBestQuests(toon.getRewardTier(), npc, toon)
        return tasks
    
    def avatarCancelled(self, avId):
        pass
    
    def avatarChoseQuest(self, avId, npc, questId, rewardId, building):
        toon = self.air.doId2do.get(avId)
        if not toon:
            return
        
        fromNpc = Quests.QuestDict[questId][Quests.QuestDictFromNpcIndex]
        toNpc = Quests.QuestDict[questId][Quests.QuestDictToNpcIndex]
        
        toon.addQuest([questId, fromNpc, toNpc, rewardId, 0], Quests.getFinalRewardId(questId))
        npc.assignQuest(avId, questId, rewardId, toNpc)
            
    def avatarChoseTrack(self, avId, pendingTrackQuest, trackId):
        pass
    
    def completeQuest(self, toon, questId):
        toonQuests = toon.getQuests()
		
        for i in range(0, len(toonQuests), 5):
            questDesc = toonQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc            
            questClass = Quests.getQuest(questId)
			
			if questId == questId:
			    break
		else:
		    #Completing a quest they dont have? :/
			print 'QuestManager: Toon %s tried to complete a quest they don\'t have!'%(toon.doId)
			pass
        
    def toonMadeFriend(self, avId, otherAvId):
        toon = self.air.doId2do.get(avId)
        if not toon:
            return
        toonQuests = toon.getQuests()
        
        for i in range(0, len(toonQuests), 5):
            questDesc = toonQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            
            questClass = Quests.getQuest(questId)
            
            if isinstance(questClass, Quests.FriendNewbieQuest):
                toonQuests[i + 5] += 1
                
                if not questClass.getCompletionStatus(toon, questDesc):
                    toon.b_setQuests(toonQuests)
                    
    def recoverItems(self, toon, suitsKilled, taskZoneId):
        print suitsKilled
        print toon
        