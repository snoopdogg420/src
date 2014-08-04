cardModel = None
arrowModel = None
chatBalloon3dModel = None
chatBalloon2dModel = None
thoughtBalloonModel = None

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
    chatBalloon3dModel = loader.loadModel(model)


def setChatBalloon2dModel(model):
    global chatBalloon2dModel
    chatBalloon2dModel = loader.loadModel(model)


def setThoughtBalloonModel(model):
    global thoughtBalloonModel
    thoughtBalloonModel = loader.loadModel(model)


def setRolloverSound(sound):
    global rolloverSound
    rolloverSound = sound


def setClickSound(sound):
    global clickSound
    clickSound = sound
