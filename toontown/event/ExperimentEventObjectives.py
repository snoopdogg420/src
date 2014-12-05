from toontown.event.ExperimentEventSuitObjective import ExperimentEventSuitObjective


DESCRIPTION_INDEX = 0
NEEDED_INDEX = 1
ICON_INDEX = 2


objectiveInfo = {
  1: ['Defeat 5 Cogs', 5, loader.loadModel('phase_3/models/gui/cog_icons').find('**/*cog')]
}


objectives = {
  1: (ExperimentEventSuitObjective, [5, 1, 12, 'any'])
}


def getObjectiveDescription(objectiveId):
    return objectiveInfo[objectiveId][DESCRIPTION_INDEX]


def getObjectiveNeeded(objectiveId):
    return objectiveInfo[objectiveId][NEEDED_INDEX]


def getObjectiveIcon(objectiveId):
    return objectiveInfo[objectiveId][ICON_INDEX]


def getObjectiveInfo(objectiveId):
    return objectiveInfo[objectiveId]


def makeObjective(objectiveId, experimentEvent):
    objectiveData = objectives[objectiveId]
    objective = objectiveData[0](experimentEvent, objectiveId, *objectiveData[1])
    objective.registerHook()
    return objective
