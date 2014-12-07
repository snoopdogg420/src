from toontown.event.ExperimentSuitChallenge import ExperimentSuitChallenge
from toontown.event.ExperimentSuitItemChallenge import ExperimentSuitItemChallenge
from toontown.event.ExperimentFireReward import ExperimentFireReward
from toontown.event.ExperimentGagReward import ExperimentGagReward

import random


def initialChallengeCompletionBlock(challenge):
    challenge.experimentEvent.messageParticipants('You completed the challenge!')
    ExperimentFireReward(challenge, random.randint(1, 3)).handleReward()
    challenge.experimentEvent.setChallenge(6)


def gagTrackCompletionBlock(challenge):
    challenge.experimentEvent.messageParticipants('You completed the challenge!')
    ExperimentGagReward(challenge, 'any').handleReward()


DESCRIPTION_INDEX = 0
NEEDED_INDEX = 1
ICON_INDEX = 2


challengeInfo = {
  1: ['Defeat 2 Cogs', 2, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')],
  2: ['Defeat 4 Cogs', 4, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')],
  3: ['Defeat 6 Cogs', 6, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')],
  4: ['Defeat 8 Cogs', 8, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')],
  5: ['Defeat 10 Cogs', 10, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')],
  6: ['Collect 4 Cog gears', 4, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')]
}


challenges = {
  1: (ExperimentSuitChallenge, [initialChallengeCompletionBlock, 2, 1, 12, 'any']),
  2: (ExperimentSuitChallenge, [initialChallengeCompletionBlock, 4, 1, 12, 'any']),
  3: (ExperimentSuitChallenge, [initialChallengeCompletionBlock, 6, 1, 12, 'any']),
  4: (ExperimentSuitChallenge, [initialChallengeCompletionBlock, 8, 1, 12, 'any']),
  5: (ExperimentSuitChallenge, [initialChallengeCompletionBlock, 10, 1, 12, 'any']),
  6: (ExperimentSuitItemChallenge, [gagTrackCompletionBlock, 4, 1, 12, 'any'])
}


def getChallengeDescription(challengeId):
    return challengeInfo[challengeId][DESCRIPTION_INDEX]


def getChallengeNeeded(challengeId):
    return challengeInfo[challengeId][NEEDED_INDEX]


def getChallengeIcon(objectiveId):
    return challengeInfo[challengeId][ICON_INDEX]


def getChallengeInfo(challengeId):
    return challengeInfo[challengeId]


def makeChallenge(challengeId, experimentEvent):
    challengeData = challenges[challengeId]
    challenge = challengeData[0](experimentEvent, challengeId, *challengeData[1])
    challenge.registerHook()
    return challenge
