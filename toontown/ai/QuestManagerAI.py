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
        
	for i in range(0, len(toonQuests), 5):
	    questDesc = toonQuests[i:i + 5]
	    questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc            
	    questClass = Quests.getQuest(questId)
	    
	    if questClass:
		completeStatus = questClass.getCompletionStatus(toon, questDesc, npc)
	    else:
		continue
	    
	    if completeStatus == Quests.COMPLETE:
		print 'QuestManager: %s (AvId: %s) Completed QuestId: %s'%(toon.getName(), toon.doId, questId)
		
		if Quests.getNextQuest(questId, npc, toon) != Quests.NA:
		    self.nextQuest(toon, npc, questId)
		else:
		    npc.completeQuest(avId, questId, rewardId)
		    self.completeQuest(toon, questId)
		
		break
	else:
	    if (len(toonQuests) == toonQuestPocketSize*5):
		npc.rejectAvatar(avId)
	    else:
		npc.presentQuestChoice(avId, self.avatarQuestChoice(toon, npc))

            
    def avatarQuestChoice(self, toon, npc):
        tasks = Quests.chooseBestQuests(Quests.DG_TIER, npc, toon)
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
    
    def completeQuest(self, toon, completeQuestId):
        toonQuests = toon.getQuests()
		
        for i in range(0, len(toonQuests), 5):
            questDesc = toonQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            questClass = Quests.getQuest(questId)
			
	    if questId == completeQuestId:
		toon.removeQuest(questId)
		break
	else:
	    #Completing a quest they dont have? :/
	    print 'QuestManager: Toon %s tried to complete a quest they don\'t have!'%(toon.doId)
	
    def incompleteQuest(self, toon, npc, incompleteQuestId, toNpcId):
	npc.incompleteQuest(toon.doId, incompleteQuestId, 0, toNpcId)
	    
    def nextQuest(self, toon, npc, questId):
	nextQuestId = Quests.getNextQuest(questId, npc, toon)
	toonQuests = toon.getQuests() #Flattened Quests.
	questList = [] #Unflattened Quests.
	
        for i in range(0, len(toonQuests), 5):
            questDesc = toonQuests[i:i + 5]
	    
	    if questDesc[0] == questId:
		questDesc[0] = nextQuestId[0]
		questDesc[2] = nextQuestId[1]
		questDesc[4] = 0
	    
	    questList.append(questDesc)
	
	npc.incompleteQuest(toon.doId, nextQuestId[0], Quests.QUEST, nextQuestId[1])
	toon.b_setQuests(questList)
        
    def toonMadeFriend(self, avId, otherAvId):
	pass
		    
    def toonDefeatedFactory(self, toon, factoryId, activeVictors):
	pass

    def recoverItems(self, toon, suitsKilled, taskZoneId):
        print suitsKilled
        print toon
	
	return []
        