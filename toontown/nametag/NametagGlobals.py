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
