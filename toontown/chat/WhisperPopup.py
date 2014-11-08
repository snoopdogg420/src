from panda3d.core import TextNode, PGButton

from toontown.chat import ChatGlobals
from toontown.chat.ChatBalloon import ChatBalloon
from toontown.margins import MarginGlobals
from toontown.margins.MarginVisible import MarginVisible
from toontown.nametag import NametagGlobals
from toontown.toontowngui.Clickable2d import Clickable2d


class WhisperPopup(Clickable2d, MarginVisible):
    CONTENTS_SCALE = 0.25

    TEXT_WORD_WRAP = 8

    QUIT_BUTTON_SCALE = 12
    QUIT_BUTTON_SHIFT = (0.035, 0, 0.035)

    def __init__(self, text, font, whisperType, timeout=10):
        Clickable2d.__init__(self, 'WhisperPopup')
        MarginVisible.__init__(self)

        self.text = text
        self.font = font
        self.whisperType = whisperType
        self.timeout = timeout

        self.active = False

        self.senderName = ''
        self.fromId = 0
        self.isPlayer = 0

        self.contents.setScale(self.CONTENTS_SCALE)

        self.whisperColor = ChatGlobals.WhisperColors[self.whisperType]

        self.textNode = TextNode('text')
        self.textNode.setWordwrap(self.TEXT_WORD_WRAP)
        self.textNode.setTextColor(self.whisperColor[PGButton.SInactive][0])
        self.textNode.setFont(self.font)
        self.textNode.setText(self.text)

        self.chatBalloon = None
        self.quitButton = None

        self.timeoutTaskName = self.getUniqueName() + '-timeout'
        self.timeoutTask = None

        self.setPriority(MarginGlobals.MP_high)
        self.setVisible(True)

        self.update()

        self.accept('MarginVisible-update', self.update)

    def destroy(self):
        self.ignoreAll()

        if self.timeoutTask is not None:
            taskMgr.remove(self.timeoutTask)
            self.timeoutTask = None

        if self.chatBalloon is not None:
            self.chatBalloon.removeNode()
            self.chatBalloon = None

        if self.quitButton is not None:
            self.quitButton.removeNode()
            self.quitButton = None

        self.textNode = None

        Clickable2d.destroy(self)

    def getUniqueName(self):
        return 'WhisperPopup-' + str(id(self))

    def update(self):
        if self.chatBalloon is not None:
            self.chatBalloon.removeNode()
            self.chatBalloon = None

        if self.quitButton is not None:
            self.quitButton.removeNode()
            self.quitButton = None

        self.contents.node().removeAllChildren()

        if self.isClickable():
            foreground, background = self.whisperColor[self.clickState]
        else:
            foreground, background = self.whisperColor[PGButton.SInactive]
        self.chatBalloon = ChatBalloon(
            NametagGlobals.chatBalloon2dModel,
            NametagGlobals.chatBalloon2dWidth,
            NametagGlobals.chatBalloon2dHeight, self.textNode,
            foreground=foreground, background=background
        )
        self.chatBalloon.reparentTo(self.contents)

        # Calculate the center of the TextNode:
        left, right, bottom, top = self.textNode.getFrameActual()
        center = self.contents.getRelativePoint(
            self.chatBalloon.textNodePath,
            ((left+right) / 2.0, 0, (bottom+top) / 2.0))

        # Translate the chat balloon along the inverse:
        self.chatBalloon.setPos(self.chatBalloon, -center)

        # Draw the quit button:
        quitButtonNode = NametagGlobals.quitButton[PGButton.SReady]
        self.quitButton = quitButtonNode.copyTo(self.contents)
        self.quitButton.setScale(self.QUIT_BUTTON_SCALE)

        # Move the quit button to the top right of the TextNode:
        self.quitButton.setPos(self.contents.getRelativePoint(
            self.chatBalloon.textNodePath, (right, 0, top)))

        # Apply the quit button shift:
        self.quitButton.setPos(self.quitButton, self.QUIT_BUTTON_SHIFT)

        # Update the click region if necessary:
        if self.getCell() is not None:
            self.updateClickRegion()
        else:
            if self.region is not None:
                self.region.setActive(False)

    def manage(self, marginManager):
        MarginVisible.manage(self, marginManager)

        self.timeoutTask = taskMgr.doMethodLater(
            self.timeout, self.unmanage, self.timeoutTaskName, [marginManager])

    def unmanage(self, marginManager):
        MarginVisible.unmanage(self, marginManager)

        self.destroy()

    def setClickable(self, senderName, fromId, isPlayer=0):
        self.senderName = senderName
        self.fromId = fromId
        self.isPlayer = isPlayer
        self.setClickEvent('clickedWhisper', extraArgs=[fromId, isPlayer])
        self.setActive(True)

    def applyClickState(self, clickState):
        if self.chatBalloon is not None:
            foreground, background = self.whisperColor[clickState]
            self.chatBalloon.setForeground(foreground)
            self.chatBalloon.setBackground(background)

    def setClickState(self, clickState):
        if self.isClickable():
            self.applyClickState(clickState)
        else:
            self.applyClickState(PGButton.SInactive)

        Clickable2d.setClickState(self, clickState)

    def enterDepressed(self):
        if self.isClickable():
            base.playSfx(NametagGlobals.clickSound)

    def enterRollover(self):
        if self.isClickable() and (self.lastClickState != PGButton.SDepressed):
            base.playSfx(NametagGlobals.rolloverSound)

    def updateClickRegion(self):
        if self.chatBalloon is not None:
            right = self.chatBalloon.width / 2.0
            left = -right
            top = self.chatBalloon.height / 2.0
            bottom = -top

            self.setClickRegionFrame(left, right, bottom, top)
            self.region.setActive(True)
        else:
            self.region.setActive(False)

    def marginVisibilityChanged(self):
        if self.getCell() is not None:
            self.updateClickRegion()
        else:
            if self.region is not None:
                self.region.setActive(False)
