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
