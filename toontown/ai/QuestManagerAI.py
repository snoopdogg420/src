from toontown.quest import Quests

# Magic Word imports
from otp.ai.MagicWordGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
import shlex

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
		
		if Quests.getNextQuest(questId, npc, toon)[0] != Quests.NA:
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
		self.giveReward(toon, rewardId)
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
	
    def giveReward(self, toon, rewardId):
	rewardClass = Quests.getReward(rewardId)
	rewardClass.sendRewardAI(toon)
        
    def toonMadeFriend(self, avId, otherAvId):
	pass
		    
    def toonDefeatedFactory(self, toon, factoryId, activeVictors):
	pass

    def recoverItems(self, toon, suitsKilled, taskZoneId):
	print 'QuestManager: %s (AvId: %s) is recovering Items'%(toon.getName(), toon.doId)
	
	flattenedQuests = toon.getQuests()
	questList = [] #unflattened
	
	recoveredItems = []
	unrecoveredItems = []
	
	for i in range(0, len(flattenedQuests), 5):
	    questDesc = flattenedQuests[i : i + 5]
	    questClass = Quests.getQuest(questDesc[0])

	    if isinstance(questClass, Quests.CogQuest):
		for suit in suitsKilled:
		    if questClass.doesCogCount(toon.doId, suit, Quests.Anywhere, [toon.doId]):
			questDesc[4] += 1
	    elif isinstance(questClass, Quests.RecoverItemQuest):
		chance = questClass.getPercentChance()
		recoveredItems.append(questClass.getItem())
	    
	    questList.append(questDesc)
	
	toon.b_setQuests(questList)
	return [recoveredItems, unrecoveredItems]
    
    def hasTailorClothingTicket(self, avId, npc):
	toon = self.air.doId2do.get(avId)
        if not toon:
            return
	
	flattenedQuests = toon.getQuests()
	
	for i in range(0, len(flattenedQuests), 5):
	    questDesc = flattenedQuests[i : i + 5]
	    questClass = Quests.getQuest(questDesc[0])
	    
	    if isinstance(questClass, Quests.DeliverItemQuest):
		if questClass.getItem() == 1000:
		    return 1
		
	return 0
    
    def removeClothingTicket(self, toon, npc):
	flattenedQuests = toon.getQuests()
	questList = []
	
	for i in range(0, len(flattenedQuests), 5):
	    questDesc = flattenedQuests[i : i + 5]
	    
	    if isinstance(questClass, Quests.DeliverItemQuest):
		if questClass.getItem() == 1000:
		    nextQuest = Quests.getNextQuest(questDesc[0], npc, toon)
		    questDesc[4] = 1
		    
	    questList.append(questDesc)
	    
	toon.b_setQuests(questList)
	
@magicWord(category=CATEGORY_CHARACTERSTATS, types=[str, int, int])
def quests(command, arg0=0, arg1=0):
    target = spellbook.getTarget()
    currQuests = target.getQuests()
    currentQuestIds = []
    
    for i in range(0, len(currQuests), 5):
        currentQuestIds.append(currQuests[i])
    
    pocketSize = target.getQuestCarryLimit()
    carrying = len(currQuests) / 5
    canCarry = False
    
    if (carrying < pocketSize):
        canCarry = True
    
    if command == 'clear':
        target.b_setQuests([])
        return 'Cleared quests'
    elif command == 'clearHistory':
        target.d_setQuestHistory([])
        return 'Cleared quests history'
    elif command == 'add':
        if arg0:
            if canCarry:
                if arg0 in Quests.QuestDict.keys():
                    return 'Added QuestID %s'%(arg0)
                else:
                    return 'Invalid QuestID %s'%(arg0)
            else:
                return 'Cannot take anymore quests'
        else:
            return 'add needs 1 argument.'
    elif command == 'remove':
        if arg0:
            if arg0 in currentQuestIds:
                target.removeQuest(arg0)
                return 'Removed QuestID %s'%(arg0)
            elif arg0 < pocketSize and arg0 > 0:
		if len(currentQuestIds) <= arg0:
		    questIdToRemove = currentQuestIds[arg0 - 1]
		    target.removeQuest(questIdToRemove)
		    return 'Removed quest from slot %s'%(arg0)
		else:
		    return 'Invalid quest slot'
            else:
                return 'Cannot remove quest %s'%(arg0)
        else:
            return 'remove needs 1 argument.'
    elif command == 'list':
        if arg0:
            if arg0 > 0 and arg0 <= pocketSize:
                start = (arg0 -1) * 5
                questDesc = currQuests[start : start + 5]
                return 'QuestDesc in slot %s: %s.'%(arg0, questDesc)
            else:
                return 'Invalid quest slot %s.'%(arg0)
        else:
            return 'CurrentQuests: %s'%(currentQuestIds)
    elif command == 'bagSize':
	if arg0 > 0 and arg0 < 5:
	    target.b_setQuestCarryLimit(arg0)
	    return 'Set carry limit to %s'%(arg0)
	else:
	    return 'Argument 0 must be between 1 and 4.'
    elif command == 'progress':
        if arg0 and arg1:
	    if arg0 > 0 and arg0 <= pocketSize:
		questList = []
		wantedQuestId = currentQuestIds[arg0 - 1]
		
		for i in range(0, len(currQuests), 5):
		    questDesc = currQuests[i : i + 5]
		    
		    if questDesc[0] == wantedQuestId:
			questDesc[4] = arg1
			
		    questList.append(questDesc)
		
		target.b_setQuests(questList)
		return 'Set quest slot %s progress to %s'%(arg0, arg1)
	    elif arg0 in Quests.QuestDict.keys():
		if arg0 in currentQuestIds:
		    questList = []
		    
		    for i in range(0, len(currQuests), 5):
			questDesc = currQuests[i : i + 5]
		    
			if questDesc[0] == arg0:
			    questDesc[4] = arg1
			
			questList.append(questDesc)
		    
		    target.b_setQuests(questList)
		    return 'Set QuestID %s progress to %s'%(arg0, arg1)
		else:
		    return 'Cannot progress QuestID: %s.'%(arg0)
	    else:
		return 'Invalid quest or slot id'
	else:
	    return 'progress needs 2 arguments.'
    else:
        return 'Invalid first argument.'
