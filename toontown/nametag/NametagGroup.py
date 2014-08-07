from pandac.PandaModules import *

from toontown.nametag import Nametag2d
from toontown.nametag import Nametag3d
from toontown.nametag import NametagGlobals


class NametagGroup:
    def __init__(self):
        self.nametag2d = Nametag3d.Nametag2d()
        self.nametag3d = Nametag2d.Nametag3d()

        self.avatar = None
        self.font = None
        self.chatType = NametagGlobals.CHAT
        self.chatBalloonType = NametagGlobals.CHAT_BALLOON

        # Foreground, background:
        self.nametagColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 0.1))
        self.chatColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 1))
        self.speedChatColor = (VBase4(0, 0, 0, 1), VBase4(1, 1, 1, 1))

        self.nameText = ''
        self.chatText = ''

        self.chatPages = []
        self.chatPageIndex = 0

        self.icon = PandaNode('icon')

        self.nametags = set()
        self.add(self.nametag2d)
        self.add(self.nametag3d)

    def destroy(self):
        for nametag in self.nametags:
            self.remove(nametag)
        if self.icon:
            self.icon.removeAllChildren()
            self.icon = None
        if self.nametag2d:
            self.nametag2d = None
        if self.nametag3d:
            self.nametag3d = None

    def add(self, nametag):
        self.nametags.add(nametag)
        self.update(nametag)

    def remove(self, nametag):
        nametag.destroy()
        self.nametags.remove(nametag)

    def update(self, nametag):
        nametag.setAvatar(self.avatar)
        nametag.setFont(self.font)
        nametag.setChatType(self.chatType)
        nametag.setChatBalloonType(self.chatBalloonType)
        nametag.setNametagColor(self.nametagColor)
        nametag.setChatColor(self.chatColor)
        nametag.setSpeedChatColor(self.speedChatColor)
        nametag.setNameText(self.nameText)
        nametag.setChatText(self.chatText)
        nametag.setIcon(self.icon)
        nametag.update()

    def setAvatar(self, avatar):
        self.avatar = avatar
        for nametag in self.nametags:
            nametag.setAvatar(self.avatar)

    def getAvatar(self):
        return self.avatar

    def setFont(self, font):
        self.font = font
        for nametag in self.nametags:
            nametag.setFont(self.font)

    def getFont(self):
        return self.font

    def setChatType(self, chatType):
        self.chatType = chatType
        for nametag in self.nametags:
            nametag.setChatType(self.chatType)

    def getChatType(self):
        return self.chatType

    def setChatBalloonType(self, chatBalloonType):
        self.chatBalloonType = chatBalloonType
        for nametag in self.nametags:
            nametag.setChatBalloonType(chatBalloonType)

    def getChatBalloonType(self):
        return self.chatBalloonType

    def setNametagColor(self, foreground, background):
        self.nametagColor = (foreground, background)
        for nametag in self.nametags:
            nametag.setNametagColor(foreground, background)

    def getNametagColor(self):
        return self.nametagColor

    def setChatColor(self, foreground, background):
        self.chatColor = (foreground, background)
        for nametag in self.nametags:
            nametag.setChatColor(foreground, background)

    def getChatColor(self):
        return self.chatColor

    def setSpeedChatColor(self, foreground, background):
        self.speedChatColor = (foreground, background)
        for nametag in self.nametags:
            nametag.setSpeedChatColor(foreground, background)

    def getSpeedChatColor(self):
        return self.speedChatColor

    def setNameText(self, nameText):
        self.nameText = nameText
        for nametag in self.nametags:
            nametag.setNameText(nameText)

    def getNameText(self):
        return self.nameText

    def setChatText(self, chatText):
        self.chatText = chatText
        for nametag in self.nametags:
            nametag.setChatText(chatText)

    def getChatText(self):
        return self.chatText

    def getNumChatPages(self):
        return len(self.chatPages)

    def getChatPageIndex(self):
        return self.chatPageIndex
