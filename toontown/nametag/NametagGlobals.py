from pandac.PandaModules import *


CCNormal = 0
CCNoChat = 1
CCNonPlayer = 2
CCSuit = 3
CCToonBuilding = 4
CCSuitBuilding = 5
CCHouseBuilding = 6
CCSpeedChat = 7
CCFreeChat = 8

CHAT = 0
SPEEDCHAT = 1

CHAT_BALLOON = 0
THOUGHT_BALLOON = 1

cardModel = None
arrowModel = None
chatBalloon3dModel = None
chatBalloon3dWidth = 0
chatBalloon3dHeight = 0
chatBalloon2dModel = None
chatBalloon2dWidth = 0
chatBalloon2dHeight = 0
thoughtBalloonModel = None
thoughtBalloonWidth = 0
thoughtBalloonHeight = 0

rolloverSound = None
clickSound = None


def setCardModel(model):
    global cardModel
    cardModel = loader.loadModel(model)


def setArrowModel(model):
    global arrowModel
    arrowModel = loader.loadModel(model)


def setChatBalloon3dModel(model):
    global chatBalloon3dModel
    global chatBalloon3dWidth
    global chatBalloon3dHeight
    chatBalloon3dModel = loader.loadModel(model)
    chatBalloon3dWidth, chatBalloon3dHeight = getModelWidthHeight(chatBalloon3dModel)


def setChatBalloon2dModel(model):
    global chatBalloon2dModel
    global chatBalloon2dWidth
    global chatBalloon2dHeight
    chatBalloon2dModel = loader.loadModel(model)
    chatBalloon2dWidth, chatBalloon2dHeight = getModelWidthHeight(chatBalloon2dModel)


def setThoughtBalloonModel(model):
    global thoughtBalloonModel
    global thoughtBalloonWidth
    global thoughtBalloonHeight
    thoughtBalloonModel = loader.loadModel(model)
    thoughtBalloonWidth, thoughtBalloonHeight = getModelWidthHeight(thoughtBalloonModel)


def setRolloverSound(sound):
    global rolloverSound
    rolloverSound = sound


def setClickSound(sound):
    global clickSound
    clickSound = sound


def getModelWidthHeight(model):
    pointA, pointB = model.getTightBounds()
    width = pointB.getX() - pointA.getX()
    height = pointB.getZ() - pointA.getZ()
    return (width, height)


NametagColors = {
    CCNormal: (
        (VBase4(0.3, 0.3, 0.7, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(0.3, 0.3, 0.7, 1.0), VBase4(0.2, 0.2, 0.2, 0.1)),  # Down
        (VBase4(0.5, 0.5, 1.0, 1.0), VBase4(1.0, 1.0, 1.0, 0.3)),  # Rollover
        (VBase4(0.3, 0.3, 0.7, 1.0), VBase4(1.0, 1.0, 1.0, 0.2))   # Disabled
    ),
    CCNoChat: (
        (VBase4(0.8, 0.4, 0.0, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(1.0, 0.5, 0.5, 1.0), VBase4(0.2, 0.2, 0.2, 0.1)),  # Click
        (VBase4(1.0, 0.5, 0.0, 1.0), VBase4(1.0, 1.0, 1.0, 0.3)),  # Rollover
        (VBase4(0.8, 0.4, 0.0, 1.0), VBase4(0.8, 0.8, 0.8, 0.2))   # Disabled
    ),
    CCNonPlayer: (
        (VBase4(0.8, 0.4, 0.0, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(0.8, 0.4, 0.0, 1.0), VBase4(0.8, 0.8, 0.8, 0.1)),  # Down
        (VBase4(0.8, 0.4, 0.0, 1.0), VBase4(0.8, 0.8, 0.8, 0.3)),  # Rollover
        (VBase4(0.8, 0.4, 0.0, 1.0), VBase4(0.8, 0.8, 0.8, 0.2))   # Disabled
    ),
    CCSuit: (
        (VBase4(0.2, 0.2, 0.2, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(0.2, 0.2, 0.2, 1.0), VBase4(0.2, 0.2, 0.2, 0.1)),  # Down
        (VBase4(0.4, 0.4, 0.4, 1.0), VBase4(1.0, 1.0, 1.0, 0.3)),  # Rollover
        (VBase4(0.2, 0.2, 0.2, 1.0), VBase4(0.8, 0.8, 0.8, 0.2))   # Disabled
    ),
    CCSuitBuilding: (
        (VBase4(0.5, 0.5, 0.5, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(0.5, 0.5, 0.5, 1.0), VBase4(0.8, 0.8, 0.8, 0.1)),  # Down
        (VBase4(0.5, 0.5, 0.5, 1.0), VBase4(0.8, 0.8, 0.8, 0.3)),  # Rollover
        (VBase4(0.5, 0.5, 0.5, 1.0), VBase4(0.8, 0.8, 0.8, 0.2))   # Disabled
    ),
    CCToonBuilding: (
        (VBase4(0.2, 0.6, 0.9, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(0.2, 0.6, 0.9, 1.0), VBase4(0.8, 0.8, 0.8, 0.1)),  # Down
        (VBase4(0.2, 0.6, 0.9, 1.0), VBase4(0.8, 0.8, 0.8, 0.3)),  # Rollover
        (VBase4(0.2, 0.6, 0.9, 1.0), VBase4(0.8, 0.8, 0.8, 0.2))   # Disabled
    ),
    CCHouseBuilding: (
        (VBase4(0.2, 0.6, 0.9, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(0.2, 0.2, 0.5, 1.0), VBase4(0.2, 0.2, 0.2, 0.1)),  # Down
        (VBase4(0.5, 0.5, 1.0, 1.0), VBase4(1.0, 1.0, 1.0, 1.3)),  # Rollover
        (VBase4(0.0, 0.6, 0.2, 1.0), VBase4(0.8, 0.8, 0.8, 0.2))   # Disabled
    ),
    CCSpeedChat: (
        (VBase4(0.0, 0.6, 0.2, 1.0), VBase4(0.8, 0.8, 0.8, 0.2)),  # Normal
        (VBase4(0.0, 0.5, 0.0, 1.0), VBase4(0.5, 0.5, 0.5, 0.1)),  # Down
        (VBase4(0.0, 0.7, 0.2, 1.0), VBase4(1.0, 1.0, 1.0, 0.3)),  # Rollover
        (VBase4(0.0, 0.6, 0.2, 1.0), VBase4(0.8, 0.8, 0.8, 0.2))   # Disabled
    ),
    CCFreeChat: (
        (VBase4(0.3, 0.3, 0.7, 1.0), VBase4(0.8, 0.8, 0.8, 0.5)),  # Normal
        (VBase4(0.2, 0.2, 0.5, 1.0), VBase4(0.2, 0.2, 0.2, 0.6)),  # Down
        (VBase4(0.5, 0.5, 1.0, 1.0), VBase4(1.0, 1.0, 1.0, 1.0)),  # Rollover
        (VBase4(0.3, 0.3, 0.7, 1.0), VBase4(0.8, 0.8, 0.8, 0.5))   # Disabled
    )
}
