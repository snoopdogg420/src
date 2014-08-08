from pandac.PandaModules import *

from toontown.nametag import NametagGlobals
from toontown.nametag.Nametag2d import Nametag2d
from toontown.nametag.Nametag3d import Nametag3d


class NametagGroup:
    def __init__(self):
        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()

        self.avatar = None
        self.font = None
        self.chatType = NametagGlobals.CHAT
        self.chatBalloonType = NametagGlobals.CHAT_BALLOON

        # Foreground, background:
        self.nametagColor = NametagGlobals.NametagColors[NametagGlobals.CCNormal]
        self.chatColor = NametagGlobals.ChatColors[NametagGlobals.CCNormal]
        self.speedChatColor = VBase4(1, 1, 1, 1)

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

    def getUniqueName(self):
        return 'NametagGroup-' + str(id(self))

    def setNametag2d(self, nametag2d):
        if self.nametag2d:
            self.remove(self.nametag2d)
            self.nametag2d = None

        self.nametag2d = nametag2d
        self.add(self.nametag2d)

    def getNametag2d(self):
        return self.nametag2d

    def setNametag3d(self, nametag3d):
        if self.nametag3d:
            self.remove(self.nametag3d)
            self.nametag3d = None

        self.nametag3d = nametag3d
        self.add(self.nametag3d)

    def getNametag3d(self):
        return self.nametag3d

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
            nametag.setChatBalloonType(self.chatBalloonType)

    def getChatBalloonType(self):
        return self.chatBalloonType

    def setNametagColor(self, nametagColor):
        self.nametagColor = nametagColor
        for nametag in self.nametags:
            nametag.setNametagColor(self.nametagColor)

    def getNametagColor(self):
        return self.nametagColor

    def setChatColor(self, chatColor):
        self.chatColor = chatColor
        for nametag in self.nametags:
            nametag.setChatColor(self.chatColor)

    def getChatColor(self):
        return self.chatColor

    def setSpeedChatColor(self, speedChatColor):
        self.speedChatColor = speedChatColor
        for nametag in self.nametags:
            nametag.setSpeedChatColor(self.speedChatColor)

    def getSpeedChatColor(self):
        return self.speedChatColor

    def setNameText(self, nameText):
        self.nameText = nameText
        for nametag in self.nametags:
            nametag.setNameText(self.nameText)

    def getNameText(self):
        return self.nameText

    def setChatText(self, chatText, timeout=False):
        self.chatText = chatText
        for nametag in self.nametags:
            nametag.setChatText(self.chatText)

        if timeout:
            pass  # TODO: Add a timeout task.

    def getChatText(self):
        return self.chatText

    def clearChatText(self):
        self.setChatText('')
        for nametag in self.nametags:
            nametag.update()

    def getNumChatPages(self):
        return len(self.chatPages)

    def setChatPageIndex(self, chatPageIndex):
        self.chatPageIndex = chatPageIndex
        self.setChatText(self.chatPages[self.chatPageIndex])

    def getChatPageIndex(self):
        return self.chatPageIndex

    def setIcon(self, icon):
        self.icon = icon
        for nametag in self.nametags:
            nametag.setIcon(self.icon)

    def getIcon(self):
        return self.icon

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

    def manage(self, marginManager):
        pass

    def unmanage(self, marginManager):
        pass
