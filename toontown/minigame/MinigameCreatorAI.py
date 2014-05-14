import copy
import random
import time

import DistributedCannonGameAI
import DistributedCatchGameAI
import DistributedCogThiefGameAI
import DistributedDivingGameAI
import DistributedIceGameAI
import DistributedMazeGameAI
import DistributedMinigameTemplateAI
import DistributedPairingGameAI
import DistributedPatternGameAI
import DistributedPhotoGameAI
import DistributedRaceGameAI
import DistributedRingGameAI
import DistributedTagGameAI
import DistributedTargetGameAI
import DistributedTravelGameAI
import DistributedTugOfWarGameAI
import DistributedTwoDGameAI
import DistributedVineGameAI
import TravelGameGlobals
from otp.ai.MagicWordGlobal import *
from toontown.minigame.TempMinigameAI import *
from toontown.toonbase import ToontownGlobals


simbase.forcedMinigameId = simbase.config.GetInt('force-minigame', 0)
RequestMinigame = {}
MinigameZoneRefs = {}
DisabledMinigames = []


def getDisabledMinigames():
    if not DisabledMinigames:
        for name, minigameId in ToontownGlobals.MinigameNames.items():
            if not simbase.config.GetBool('want-{0}-game'.format(name), True):
                if minigameId not in DisabledMinigames:
                    DisabledMinigames.append(minigameId)
    return DisabledMinigames[:]


def createMinigame(air, playerArray, trolleyZone, minigameZone=None,
        previousGameId=ToontownGlobals.NoPreviousGameId, newbieIds=[],
        startingVotes=None, metagameRound=-1, desiredNextGame=None):
    if minigameZone is None:
        minigameZone = air.allocateZone()
    acquireMinigameZone(minigameZone)
    mgId = None
    mgDiff = None
    mgSzId = None
    for avId in playerArray:
        request = RequestMinigame.get(avId)
        if request is not None:
            mgId, mgKeep, mgDiff, mgSzId = request
            if not mgKeep:
                del RequestMinigame[avId]
            break
    if mgId is not None:
        pass
    elif simbase.forcedMinigameId:
        mgId = simbase.forcedMinigameId
    else:
        randomList = list(copy.copy(ToontownGlobals.MinigamePlayerMatrix[len(playerArray)]))
        if len(playerArray) > 1:
            randomList = list(copy.copy(ToontownGlobals.MinigameIDs))
        for gameId in [ToontownGlobals.TravelGameId] + getDisabledMinigames():
            if gameId in randomList:
                randomList.remove(gameId)
        if previousGameId != ToontownGlobals.NoPreviousGameId:
            if randomList.count(previousGameId) != 0 and len(randomList) > 1:
                randomList.remove(previousGameId)
        mgId = random.choice(randomList)
        if metagameRound > -1:
            if (metagameRound%2) == 0:
                mgId = ToontownGlobals.TravelGameId
            elif desiredNextGame:
                mgId = desiredNextGame
    mgCtors = {
        ToontownGlobals.RaceGameId: DistributedRaceGameAI.DistributedRaceGameAI,
        ToontownGlobals.CannonGameId: DistributedCannonGameAI.DistributedCannonGameAI,
        ToontownGlobals.TagGameId: DistributedTagGameAI.DistributedTagGameAI,
        ToontownGlobals.PatternGameId: DistributedPatternGameAI.DistributedPatternGameAI,
        ToontownGlobals.RingGameId: DistributedRingGameAI.DistributedRingGameAI,
        ToontownGlobals.MazeGameId: DistributedMazeGameAI.DistributedMazeGameAI,
        ToontownGlobals.TugOfWarGameId: DistributedTugOfWarGameAI.DistributedTugOfWarGameAI,
        ToontownGlobals.CatchGameId: DistributedCatchGameAI.DistributedCatchGameAI,
        ToontownGlobals.DivingGameId: DistributedDivingGameAI.DistributedDivingGameAI,
        ToontownGlobals.TargetGameId: DistributedTargetGameAI.DistributedTargetGameAI,
        ToontownGlobals.MinigameTemplateId: DistributedMinigameTemplateAI.DistributedMinigameTemplateAI,
        ToontownGlobals.PairingGameId: DistributedPairingGameAI.DistributedPairingGameAI,
        ToontownGlobals.VineGameId: DistributedVineGameAI.DistributedVineGameAI,
        ToontownGlobals.IceGameId: DistributedIceGameAI.DistributedIceGameAI,
        ToontownGlobals.CogThiefGameId: DistributedCogThiefGameAI.DistributedCogThiefGameAI,
        ToontownGlobals.TwoDGameId: DistributedTwoDGameAI.DistributedTwoDGameAI,
        ToontownGlobals.TravelGameId: DistributedTravelGameAI.DistributedTravelGameAI,
        ToontownGlobals.PhotoGameId: DistributedPhotoGameAI.DistributedPhotoGameAI
    }
    from TempMinigameAI import TempMgCtors
    for key, value in TempMgCtors.items():
        mgCtors[key] = value
    try:
        mg = mgCtors[mgId](air, mgId)
    except KeyError:
        raise Exception, 'unknown minigame ID: %s' % mgId
    mg.setExpectedAvatars(playerArray)
    mg.setNewbieIds(newbieIds)
    mg.setTrolleyZone(trolleyZone)
    mg.setDifficultyOverrides(mgDiff, mgSzId)
    if startingVotes == None:
        for avId in playerArray:
            mg.setStartingVote(avId, TravelGameGlobals.DefaultStartingVotes)
    else:
        for index in range(len(startingVotes)):
            avId = playerArray[index]
            votes = startingVotes[index]
            if votes < 0:
                print 'createMinigame negative votes, avId=%s votes=%s' % (avId, votes)
                votes = 0
            mg.setStartingVote(avId, votes)
    mg.setMetagameRound(metagameRound)
    mg.generateWithRequired(minigameZone)
    toons = []
    for doId in playerArray:
        toon = simbase.air.doId2do.get(doId)
        if toon is not None:
            toons.append(toon)
    for toon in toons:
        simbase.air.questManager.toonPlayedMinigame(toon, toons)
    retVal = {}
    retVal['minigameZone'] = minigameZone
    retVal['minigameId'] = mgId
    return retVal


def acquireMinigameZone(zoneId):
    if zoneId not in MinigameZoneRefs:
        MinigameZoneRefs[zoneId] = 0
    MinigameZoneRefs[zoneId] += 1


def releaseMinigameZone(zoneId):
    MinigameZoneRefs[zoneId] -= 1
    if MinigameZoneRefs[zoneId] <= 0:
        del MinigameZoneRefs[zoneId]
        simbase.air.deallocateZone(zoneId)


@magicWord(category=CATEGORY_OVERRIDE, types=[str, str])
def minigame(command, arg0):
    """A command set for Trolley minigames."""
    invoker = spellbook.getInvoker()
    if command.lower() == 'request':
        for name in ToontownGlobals.MinigameNames:
            if arg0.lower() == name:
                RequestMinigame[invoker.doId] = (
                    ToontownGlobals.MinigameNames[name], False, None, None)
                return 'Your request for {0} was added.'.format(arg0)
        return 'Your request for {0} could not be added.'.format(arg0)
    if command.lower() == 'force':
        for name in ToontownGlobals.MinigameNames:
            if arg0.lower() == name:
                RequestMinigame[invoker.doId] = (
                    ToontownGlobals.MinigameNames[name], True, None, None)
                return 'The minigame {0} is not being forced.'.format(arg0)
        return "Couldn't force minigame: {0}".format(arg0)
    if command.lower() == 'remove':
        if invoker.doId in RequestMinigame:
            del RequestMinigame[invoker.doId]
            return 'Your trolley game request has been removed.'
        return 'You have no trolley game requests!'
    if command.lower() == 'difficulty':
        if invoker.doId not in RequestMinigame:
            return 'You have no trolley game requests!'
        try:
            arg0 = int(arg0)
        except:
            return 'Argument 0 must be an integer, got type: {0}'.format(type(arg0))
        request = RequestMinigame[invoker.doId]
        newRequest = request[:2] + arg0 + request[3:]
        RequestMinigame[invoker.doId] = newRequest
        return 'You request for minigame difficulty {0} was added.'.format(arg0)
    if command.lower() == 'safezone':
        if invoker.doId not in RequestMinigame:
            return 'You have no trolley game requests!'
        try:
            arg0 = int(arg0)
        except:
            return 'Argument 0 must be an integer, got type: {0}'.format(type(arg0))
        request = RequestMinigame[invoker.doId]
        newRequest = request[:3] + arg0 + request[4:]
        RequestMinigame[invoker.doId] = newRequest
        return 'You request for minigame safezone {0} was added.'.format(arg0)
    return 'Invalid command.'