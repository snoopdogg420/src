from pandac.PandaModules import *

from otp.chat import ChatGlobals
from toontown.nametag import NametagGlobals


class Nametag(PandaNode):
    def __init__(self):
        PandaNode.__init__(self, 'nametag')

        self.contents = NodePath.anyPath(self).attachNewNode('contents')

        self.avatar = None
        self.nameText = ''
        self.chatText = ''
        self.font = None
        self.wordWrap = 7.5
        self.chatWordWrap = 10
        self.chatType = NametagGlobals.CHAT

        self.icon = NodePath('icon')

        # Foreground, background:
        self.nametagColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 1))
        self.chatColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 1))
        self.speedChatColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 1))

    def getThoughtBalloon(self):
        pass  # Inheritors should override this method.

    def getChatBalloon(self):
        pass  # Inheritors should override this method.

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setNameText(self, nameText):
        self.nameText = nameText
        if not self.chatText:
            self.update()

    def getNameText(self):
        return self.nameText

    def setChatText(self, chatText):
        self.chatText = chatText
        self.update()

    def getChatText(self):
        return self.chatText

    def setFont(self, font):
        self.font = font
        if not self.chatText:
            self.update()

    def getFont(self):
        return self.font

    def setWordWrap(self, wordWrap):
        self.wordWrap = wordWrap
        if not self.chatText:
            self.update()

    def getWordWrap(self):
        return self.wordWrap

    def setChatWordWrap(self, chatWordWrap):
        self.chatWordWrap = chatWordWrap
        if self.chatText:
            self.update()

    def getChatWordWrap(self):
        return self.chatWordWrap

    def setChatType(self, chatType):
        self.chatType = chatType
        if self.chatText:
            self.update()

    def getChatType(self):
        return self.chatType

    def destroy(self):
        if self.contents:
            self.contents.removeNode()
            self.contents = None

    def update(self):
        """
        Redraw the contents.
        """
        self.contents.node().removeAllChildren()
        if self.chatText:
            if self.chatText[0] == ChatGlobals.ThoughtPrefix:
                self.drawChatBalloon(self.getThoughtBalloon(), self.chatText[1:])
            else:
                self.drawChatBalloon(self.getChatBalloon(), self.chatText)
        else:
            self.drawNametag()

    def drawChatBalloon(self, chatBalloon, chatText):
        if self.chatType == NametagGlobals.SPEEDCHAT:
            foreground, background = self.speedChatColor
        else:
            foreground, background = self.chatColor

        chatBalloon = chatBalloon.create(
            chatText, self.font, foreground=foreground, background=background,
            wordWrap=self.chatWordWrap)  # TODO: Define a button.
        chatBalloon.reparentTo(self.contents)

    def drawNametag(self):
        if not self.font:
            # We can't draw this without a font.
            return

        foreground, background = self.nametagColor

        # Attach the icon:
        self.contents.attachNewNode(self.icon)

        # Create a TextNode:
        nameTextNode = TextNode('nameText')
        nameTextNode.setFont(self.font)
        nameTextNode.setAlign(TextNode.ACenter)
        nameTextNode.setWordwrap(self.wordWrap)
        nameTextNode.setText(self.nameText)
        nameText = self.contents.attachNewNode(nameTextNode, 1)
        nameText.setColor(foreground)
        nameText.setTransparency(foreground[3] < 1)
        nameText.setY(-0.05)
        nameText.setAttrib(DepthWriteAttrib.make(0))

        # Apply a panel behind the TextNode:
        namePanel = NametagGlobals.nametagCardModel.copyTo(self.contents, 0)
        namePanel.setPos((nameTextNode.getLeft()+nameTextNode.getRight()) / 2.0, 0,
                         (nameTextNode.getTop()+nameTextNode.getBottom()) / 2.0)
        namePanel.setScale(nameTextNode.getWidth() + 0.2, 1, nameTextNode.getHeight() + 0.2)
        namePanel.setColor(background)
        namePanel.setTransparency(background[3] < 1)
