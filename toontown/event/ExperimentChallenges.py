from toontown.event.ExperimentSuitChallenge import ExperimentSuitChallenge


def exampleCompleteBlock(challenge):
    challenge.experimentEvent.messageParticipants('You completed the challenge!')


DESCRIPTION_INDEX = 0
NEEDED_INDEX = 1
ICON_INDEX = 2


challengeInfo = {
  1: ['Defeat 5 Cogs', 5, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')]
}


challenges = {
  1: (ExperimentSuitChallenge, [exampleCompleteBlock, 5, 1, 12, 'any'])
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
