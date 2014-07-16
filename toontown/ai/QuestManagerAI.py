from otp.ai.MagicWordGlobal import *
from toontown.building import FADoorCodes
from toontown.hood import ZoneUtil
from toontown.quest import Quests
from toontown.toon.DistributedNPCSpecialQuestGiverAI import DistributedNPCSpecialQuestGiverAI
import random

class QuestManagerAI:
    def __init__(self, air):
        self.air = air

    def requestInteract(self, avId, npc):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        avQuestPocketSize = av.getQuestCarryLimit()
        avQuests = av.getQuests()
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            questClass = Quests.getQuest(questId)
            if questClass:
                completeStatus = questClass.getCompletionStatus(av, questDesc, npc)
            else:
                continue
            if isinstance(questClass, Quests.TrackChoiceQuest):
                npc.presentTrackChoice(avId, questId, questClass.getChoices())
                break
            elif isinstance(questClass, Quests.DeliverGagQuest):
                if npc.npcId == toNpcId:
                    questList = []
                    progress = questClass.removeGags(av)
                    for i in xrange(0, len(avQuests), 5):
                        questDesc = avQuests[i:i + 5]
                        if questDesc[0] == questId:
                            questDesc[4] += progress
                            if questDesc[4] >= questClass.getNumGags():
                                completeStatus = Quests.COMPLETE
                        questList.append(questDesc)
                    av.b_setQuests(questList)
                    if completeStatus != Quests.COMPLETE:
                        continue
            if completeStatus == Quests.COMPLETE:
                av.toonUp(av.maxHp)
                if Quests.getNextQuest(questId, npc, av)[0] != Quests.NA:
                    self.nextQuest(av, npc, questId)
                else:
                    npc.completeQuest(avId, questId, rewardId)
                    self.completeQuest(av, questId)
                if isinstance(npc, DistributedNPCSpecialQuestGiverAI):
                    if npc.tutorial and (npc.npcId == 20002):
                        messenger.send('intHqDoor0-{0}'.format(npc.zoneId), [FADoorCodes.WRONG_DOOR_HQ])
                        messenger.send('intHqDoor1-{0}'.format(npc.zoneId), [FADoorCodes.UNLOCKED])
                        streetZone = self.air.tutorialManager.currentAllocatedZones[avId][0]
                        messenger.send('extHqDoor0-{0}'.format(streetZone), [FADoorCodes.GO_TO_PLAYGROUND])
                        messenger.send('extHqDoor1-{0}'.format(streetZone), [FADoorCodes.GO_TO_PLAYGROUND])
                        messenger.send('extShopDoor-{0}'.format(streetZone), [FADoorCodes.GO_TO_PLAYGROUND])
                break
        else:
            if (len(avQuests) == avQuestPocketSize*5):
                #Full quests!
                npc.rejectAvatar(avId)
                return
            elif isinstance(npc, DistributedNPCSpecialQuestGiverAI):
                #Tutorial
                choices = self.avatarQuestChoice(av, npc)
                quest = choices[0]
                self.avatarChoseQuest(avId, npc, quest[0], quest[1], 0)
                if npc.tutorial:
                    if npc.npcId == 20000:
                        messenger.send('intShopDoor-{0}'.format(npc.zoneId), [FADoorCodes.UNLOCKED])
                return
            else:
                #Present quest choices.
                choices = self.avatarQuestChoice(av, npc)
                if choices != []:
                    npc.presentQuestChoice(avId, choices)
                    return
                else:
                    npc.rejectAvatar(avId)
                    return

    def avatarQuestChoice(self, av, npc):
        return Quests.chooseBestQuests(av.getRewardTier(), npc, av)

    def avatarChoseQuest(self, avId, npc, questId, rewardId, toNpcId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        fromNpcId = npc.getDoId()
        if toNpcId == 0:
            toNpcId = Quests.getQuestToNpcId(questId)
        av.addQuest([questId, fromNpcId, toNpcId, rewardId, 0],
                      Quests.Quest2RemainingStepsDict[questId] == 1,
                      recordHistory = 0)
        npc.assignQuest(avId, questId, rewardId, toNpcId)
        taskMgr.remove(npc.uniqueName('clearMovie'))

    def avatarChoseTrack(self, avId, npc, pendingTrackQuest, trackId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        npc.completeQuest(avId, pendingTrackQuest, Quests.getRewardIdFromTrackId(trackId))
        self.completeQuest(av, pendingTrackQuest)
        av.b_setTrackProgress(trackId, 0)

    def avatarCancelled(self, npcId):
        npc = self.air.doId2do.get(npcId)
        if not npc:
            return
        taskMgr.remove(npc.uniqueName('clearMovie'))

    def nextQuest(self, av, npc, questId):
        nextQuestId = Quests.getNextQuest(questId, npc, av)
        avQuests = av.getQuests() #Flattened Quests.
        questList = [] #Unflattened Quests.
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            if questDesc[0] == questId:
                questDesc[0] = nextQuestId[0]
                questDesc[2] = nextQuestId[1]
                questDesc[4] = 0
            questList.append(questDesc)
        npc.incompleteQuest(av.doId, nextQuestId[0], Quests.QUEST, nextQuestId[1])
        av.b_setQuests(questList)

    def completeQuest(self, av, completeQuestId):
        avQuests = av.getQuests()
        for i in xrange(0, len(avQuests), 5):
            questDesc = avQuests[i:i + 5]
            questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
            questClass = Quests.getQuest(questId)
            if questId == completeQuestId:
                av.removeQuest(questId)
                self.giveReward(av, questId, rewardId)
                self.avatarProgressTier(av)
                break

    def giveReward(self, av, questId, rewardId):
        #Actual reward giving.
        rewardClass = Quests.getReward(rewardId)
        rewardClass.sendRewardAI(av)
        #Add it to reward history.
        realRewardId = Quests.transformReward(rewardId, av)
        tier, rewardList = av.getRewardHistory()
        rewardList.append(rewardId)
        if realRewardId != rewardId:
            rewardList.append(realRewardId)
        av.b_setRewardHistory(tier, rewardList)

    def avatarProgressTier(self, av):
        currentTier = av.getRewardHistory()[0]
        if Quests.avatarHasAllRequiredRewards(av, currentTier):
            if currentTier != Quests.ELDER_TIER:
                currentTier += 1
            av.b_setRewardHistory(currentTier, [])

    def toonRodeTrolleyFirstTime(self, av):
        self.toonPlayedMinigame(av, [])

    def toonPlayedMinigame(self, av, toons):
        flattenedQuests = av.getQuests()
        questList = [] #unflattened
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if isinstance(questClass, Quests.TrolleyQuest):
                questDesc[4] = 1
            questList.append(questDesc)
        av.b_setQuests(questList)

    def toonMadeFriend(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        flattenedQuests = av.getQuests()
        questList = [] #unflattened
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if isinstance(questClass, Quests.FriendQuest):
                questDesc[4] = 1
            questList.append(questDesc)
        av.b_setQuests(questList)

    def toonUsedPhone(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        flattenedQuests = av.getQuests()
        questList = [] #unflattened
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if isinstance(questClass, Quests.PhoneQuest):
                questDesc[4] += 1
            questList.append(questDesc)
        av.b_setQuests(questList)

    def toonCaughtFishingItem(self, av):
        flattenedQuests = av.getQuests()
        questList = []
        fishingItem = -1
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if fishingItem:
                questList.append(questDesc)
                continue
            if isinstance(questClass, Quests.RecoverItemQuest):
                if not hasattr(questClass, 'getItem'):
                    questList.append(questDesc)
                    continue
                if questClass.getHolder() == Quests.AnyFish:
                    if not questClass.getCompletionStatus(av, questDesc) == Quests.COMPLETE:
                        baseChance = questClass.getPercentChance()
                        amountRemaining = questClass.getNumItems() - questDesc[4]
                        chance = Quests.calcRecoverChance(amountRemaining, baseChance)
                        if chance >= baseChance:
                            questDesc[4] += 1
                            fishingItem = questClass.getItem()
            questList.append(questDesc)
        av.b_setQuests(questList)
        return fishingItem

    def hasTailorClothingTicket(self, av, npc):
        flattenedQuests = av.getQuests()
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if isinstance(questClass, Quests.DeliverItemQuest):
                if questClass.getCompletionStatus(av, questDesc, npc) == Quests.COMPLETE:
                    return 1
        return 0

    def removeClothingTicket(self, av, npc):
        flattenedQuests = av.getQuests()
        questList = []
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if isinstance(questClass, Quests.DeliverItemQuest):
                if questClass.getCompletionStatus(av, questDesc, npc) == Quests.COMPLETE:
                    av.removeQuest(questDesc[0])
                    break

    def recoverItems(self, av, suitsKilled, taskZoneId):
        flattenedQuests = av.getQuests()
        questList = [] #unflattened
        recoveredItems = []
        unrecoveredItems = []
        taskZoneId = ZoneUtil.getBranchZone(taskZoneId)
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if questClass.getCompletionStatus(av, questDesc) == Quests.INCOMPLETE:
                if isinstance(questClass, Quests.CogQuest):
                    for suit in suitsKilled:
                        if questClass.doesCogCount(av.doId, suit, taskZoneId, suit['activeToons']):
                            questDesc[4] += 1
                elif isinstance(questClass, Quests.RecoverItemQuest):
                    if questClass.getHolder() != Quests.AnyFish:
                        for suit in suitsKilled:
                            if questClass.doesCogCount(av.doId, suit, taskZoneId, suit['activeToons']):
                                baseChance = questClass.getPercentChance()
                                amountRemaining = questClass.getNumItems() - questDesc[4]
                                chance = Quests.calcRecoverChance(amountRemaining, baseChance)
                                if chance >= baseChance:
                                    questDesc[4] += 1
                                    recoveredItems.append(questClass.getItem())
                                else:
                                    unrecoveredItems.append(questClass.getItem())
            questList.append(questDesc)
        av.b_setQuests(questList)
        return (recoveredItems, unrecoveredItems)

    def toonKilledBuilding(self, av, type, difficulty, floors, zoneId, activeToons):
        flattenedQuests = av.getQuests()
        questList = [] #unflattened
        zoneId = ZoneUtil.getBranchZone(zoneId)
        recoveredItems = []
        unrecoveredItems = []
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if questClass.getCompletionStatus(av, questDesc) == Quests.INCOMPLETE:
                if isinstance(questClass, Quests.BuildingQuest):
                    if questClass.isLocationMatch(zoneId):
                        if questClass.doesBuildingTypeCount(type):
                            if questClass.doesBuildingCount(av, activeToons):
                                if floors >= questClass.getNumFloors():
                                    questDesc[4] += 1
            questList.append(questDesc)
        av.b_setQuests(questList)

    def toonDefeatedFactory(self, av, factoryId, activeVictors):
        flattenedQuests = av.getQuests()
        questList = [] #unflattened
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if isinstance(questClass, Quests.FactoryQuest):
                if questClass.doesFactoryCount(av, factoryId, activeVictors):
                    questDesc[4] += 1
            questList.append(questDesc)
        av.b_setQuests(questList)

    def toonDefeatedMint(self, av, mintId, activeVictors):
        flattenedQuests = av.getQuests()
        questList = [] #unflattened
        for i in xrange(0, len(flattenedQuests), 5):
            questDesc = flattenedQuests[i : i + 5]
            questClass = Quests.getQuest(questDesc[0])
            if isinstance(questClass, Quests.MintQuest):
                if questClass.doesMintCount(av, mintId, activeVictors):
                    questDesc[4] += 1
            questList.append(questDesc)
        av.b_setQuests(questList)

    def toonDefeatedStage(self, av, stageId, activeVictors):
        pass

    def toonKilledCogs(self, av, suitsKilled, zoneId, activeToonList):
        pass

@magicWord(category=CATEGORY_ADMINISTRATOR, types=[str, int, int])
def quests(command, arg0=0, arg1=0):
    target = spellbook.getTarget()
    currQuests = target.getQuests()
    currentQuestIds = []

    for i in xrange(0, len(currQuests), 5):
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

                for i in xrange(0, len(currQuests), 5):
                    questDesc = currQuests[i : i + 5]

                    if questDesc[0] == wantedQuestId:
                        questDesc[4] = arg1

                    questList.append(questDesc)

                target.b_setQuests(questList)
                return 'Set quest slot %s progress to %s'%(arg0, arg1)
            elif arg0 in Quests.QuestDict.keys():
                if arg0 in currentQuestIds:
                    questList = []

                    for i in xrange(0, len(currQuests), 5):
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
    elif command == 'tier':
        if arg0:
            target.b_setRewardHistory(arg0, target.getRewardHistory()[1])
            return 'Set tier to %s'%(arg0)
        else:
            return 'tier needs 1 argument.'
    else:
        return 'Invalid first argument.'
