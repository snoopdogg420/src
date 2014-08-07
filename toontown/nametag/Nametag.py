from direct.task.Task import Task
from pandac.PandaModules import *

from toontown.nametag import ChatBalloon
from toontown.nametag import NametagGlobals


class Nametag(PandaNode):
    NAMETAG_X_PADDING = 0.2
    NAMETAG_Z_PADDING = 0.2

    def __init__(self):
        PandaNode.__init__(self, 'nametag')

        self.contents = NodePath.anyPath(self).attachNewNode('contents')

        self.avatar = None
        self.font = None
        self.chatType = NametagGlobals.CHAT
        self.chatBalloonType = NametagGlobals.CHAT_BALLOON
        self.hidden = False

        # Foreground, background:
        self.nametagColor = NametagGlobals.NametagColors[NametagGlobals.CCNormal]
        self.chatColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 1))
        self.speedChatColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 1))

        # Create our TextNodes:
        self.nameTextNode = TextNode('nameText')
        self.nameTextNode.setWordwrap(8)
        self.nameTextNode.setTextColor(self.nametagColor[0])
        self.nameTextNode.setAlign(TextNode.ACenter)

        self.chatTextNode = TextNode('chatText')
        self.chatTextNode.setWordwrap(10)
        self.chatTextNode.setTextColor(self.chatColor[0])
        self.chatTextNode.setGlyphScale(1.1)

        self.icon = None

        # Add the tick task:
        self.tickTask = taskMgr.add(self.tick, self.getUniqueName() + '-tick')

    def getChatBalloonModel(self):
        pass  # Inheritors should override this method.

    def getChatBalloonWidth(self):
        pass  # Inheritors should override this method.

    def getChatBalloonHeight(self):
        pass  # Inheritors should override this method.

    def getThoughtBalloonModel(self):
        pass  # Inheritors should override this method.

    def getThoughtBalloonWidth(self):
        pass  # Inheritors should override this method.

    def getThoughtBalloonHeight(self):
        pass  # Inheritors should override this method.

    def tick(self, task):
        return Task.cont  # Inheritors should override this method.

    def destroy(self):
        taskMgr.remove(self.tickTask)

        if self.contents:
            self.contents.removeNode()
            self.contents = None

        if self.chatTextNode:
            self.chatTextNode = None

        if self.nameTextNode:
            self.nameTextNode = None

    def getUniqueName(self):
        return 'Nametag-' + str(id(self))

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setFont(self, font):
        self.font = font
        self.nameTextNode.setFont(self.font)
        self.chatTextNode.setFont(self.font)

    def getFont(self):
        return self.font

    def setChatType(self, chatType):
        self.chatType = chatType

    def getChatType(self):
        return self.chatType

    def setChatBalloonType(self, chatBalloonType):
        self.chatBalloonType = chatBalloonType

    def getChatBalloonType(self):
        return self.chatBalloonType

    def setNametagColor(self, foreground, background):
        self.nametagColor = (foreground, background)
        if not self.chatTextNode.getText():
            self.update()

    def getNametagColor(self):
        return self.nametagColor

    def setChatColor(self, foreground, background):
        self.chatColor = (foreground, background)
        if self.chatTextNode.getText() and (self.chatType == NametagGlobals.CHAT):
            self.update()

    def getChatColor(self):
        return self.chatColor

    def setSpeedChatColor(self, foreground, background):
        self.speedChatColor = (foreground, background)
        if self.chatTextNode.getText() and (self.chatType == NametagGlobals.SPEEDCHAT):
            self.update()

    def getSpeedChatColor(self):
        return self.speedChatColor

    def setWordWrap(self, wordWrap):
        self.nameTextNode.setWordwrap(wordWrap)

    def getWordWrap(self):
        return self.nameTextNode.getWordwrap()

    def setChatWordWrap(self, chatWordWrap):
        self.chatTextNode.setWordwrap(chatWordWrap)

    def getChatWordWrap(self):
        return self.chatTextNode.getWordwrap()

    def setNameText(self, nameText):
        self.nameTextNode.setText(nameText)

    def getNameText(self):
        return self.nameTextNode.getText()

    def setChatText(self, chatText):
        self.chatTextNode.setText(chatText)

    def getChatText(self, chatText):
        return self.chatTextNode.getText()

    def setIcon(self, icon):
        self.icon = icon
        if not self.chatTextNode.getText():
            self.update()

    def getIcon(self):
        return self.icon

    def update(self):
        """
        Redraw the contents.
        """
        self.contents.node().removeAllChildren()
        if self.chatTextNode.getText():
            self.drawChatBalloon()
        else:
            self.drawNametag()

    def drawChatBalloon(self):
        if self.chatBalloonType == NametagGlobals.CHAT_BALLOON:
            model = self.getChatBalloonModel()
            modelWidth = self.getChatBalloonWidth()
            modelHeight = self.getChatBalloonHeight()
        elif self.chatBalloonType == NametagGlobals.THOUGHT_BALLOON:
            model = self.getThoughtBalloonModel()
            modelWidth = self.getThoughtBalloonWidth()
            modelHeight = self.getThoughtBalloonHeight()
        else:
            return

        if self.chatType == NametagGlobals.CHAT:
            foreground, background = self.chatColor
        elif self.chatType == NametagGlobals.SPEEDCHAT:
            foreground, background = self.speedChatColor
        else:
            return

        chatBalloon = ChatBalloon.ChatBalloon(
            model, modelWidth, modelHeight, self.chatTextNode,
            foreground=foreground, background=background)
        chatBalloon.reparentTo(self.contents)

    def drawNametag(self):
        if self.hidden:
            return

        foreground, background = self.nametagColor[0]  # Normal

        # Attach the icon:
        if self.icon:
            self.contents.attachNewNode(self.icon)

        # Set the color of the TextNode:
        self.nameTextNode.setColor(foreground)

        # Attach the TextNode:
        nameText = self.contents.attachNewNode(self.nameTextNode, 1)
        nameText.setTransparency(foreground[3] < 1)
        nameText.setDepthOffset(1)

        # Attach a panel behind the TextNode:
        namePanel = NametagGlobals.cardModel.copyTo(self.contents, 0)
        x = (self.nameTextNode.getLeft()+self.nameTextNode.getRight()) / 2.0
        z = (self.nameTextNode.getTop()+self.nameTextNode.getBottom()) / 2.0
        namePanel.setPos(x, 0, z)
        sX = self.nameTextNode.getWidth() + Nametag.NAMETAG_X_PADDING
        sZ = self.nameTextNode.getHeight() + Nametag.NAMETAG_Z_PADDING
        namePanel.setScale(sX, 1, sZ)
        namePanel.setColor(background)
        namePanel.setTransparency(background[3] < 1)

    def hide(self):
        self.hidden = True
        self.update()

    def show(self):
        self.hidden = False
        self.update()
