from pandac.PandaModules import *

from toontown.chat import ChatGlobals
from toontown.chat.ChatBalloon import ChatBalloon
from toontown.margins.MarginVisible import MarginVisible
from toontown.nametag import NametagGlobals


class WhisperPopup(PandaNode, MarginVisible):
    CONTENTS_SCALE = 0.25

    TEXT_WORD_WRAP = 8

    def __init__(self, text, font, whisperType, timeout=10):
        PandaNode.__init__(self, 'whisper')
        MarginVisible.__init__(self)

        self.text = text
        self.font = font
        self.whisperType = whisperType
        self.timeout = timeout

        self.active = False

        self.lastClickState = NametagGlobals.NORMAL
        self.clickState = NametagGlobals.NORMAL
        self.pendingClickState = NametagGlobals.NORMAL

        self.contents = NodePath.anyPath(self).attachNewNode('contents')
        self.contents.setScale(self.CONTENTS_SCALE)

        self.whisperColor = ChatGlobals.WhisperColors[self.whisperType]

        self.textNode = TextNode('text')
        self.textNode.setWordwrap(self.TEXT_WORD_WRAP)
        self.textNode.setTextColor(self.whisperColor[self.clickState][0])
        self.textNode.setFont(self.font)
        self.textNode.setText(self.text)

        self.chatBalloon = None

        self.setPriority(2)
        self.setVisible(True)

        self.timeoutTaskName = self.getUniqueName() + '-timeout'
        self.timeoutTask = None

        self.update()

    def destroy(self):
        if self.timeoutTask is not None:
            taskMgr.remove(self.timeoutTask)
            self.timeoutTask = None

        self.chatBalloon = None

        if self.textNode is not None:
            self.textNode = None

        if self.contents is not None:
            self.contents.removeNode()
            self.contents = None

    def getUniqueName(self):
        return 'WhisperPopup-' + str(id(self))

    def update(self):
        foreground, background = self.whisperColor[self.clickState]

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

    def manage(self, marginManager):
        MarginVisible.manage(self, marginManager)

        self.timeoutTask = taskMgr.doMethodLater(
            self.timeout, self.unmanage, self.timeoutTaskName, [marginManager])

    def unmanage(self, marginManager):
        MarginVisible.unmanage(self, marginManager)

        self.destroy()

    def setClickable(self, senderName, fromId, isPlayer=0):
        pass  # NAMETAG TODO
