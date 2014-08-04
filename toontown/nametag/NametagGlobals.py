from toontown.nametag import ChatBalloon


# Button states:
BUTTON_UP = 0
BUTTON_DOWN = 1
BUTTON_ROLLOVER = 2

# Chat types:
CHAT = 0
SPEEDCHAT = 1

# Graphical:
nametagCardModel = None
nametagCardDimensions = None
arrowModel = None
chatBalloon3d = None
chatBalloon2d = None
thoughtBalloon = None
pageButtons = {}
quitButtons = {}

# Sound:
clickSound = None
rolloverSound = None


# Setters:
def setNametagCard(model, dimensions):
    global nametagCardModel
    global nametagCardDimensions
    nametagCardModel = loader.loadModel(model)
    nametagCardDimensions = dimensions


def setArrowModel(model):
    global arrowModel
    arrowModel = loader.loadModel(model)


def setChatBalloon3d(model):
    global chatBalloon3d
    chatBalloon3d = ChatBalloon.ChatBalloon(loader.loadModel(model))


def setChatBalloon2d(model):
    global chatBalloon2d
    chatBalloon2d = ChatBalloon.ChatBalloon(loader.loadModel(model))


def setThoughtBalloon(model):
    global thoughtBalloon
    thoughtBalloon = ChatBalloon.ChatBalloon(loader.loadModel(model))


def setPageButton(state, model):
    pageButtons[state] = model


def setQuitButton(state, model):
    pageButtons[state] = model


def setClickSound(sound):
    global clickSound
    clickSound = sound


def setRolloverSound(sound):
    global rolloverSound
    rolloverSound = sound
