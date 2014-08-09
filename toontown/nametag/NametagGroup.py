from direct.task.Task import Task
from pandac.PandaModules import *

from toontown.nametag import NametagGlobals
from toontown.nametag.Nametag2d import Nametag2d
from toontown.nametag.Nametag3d import Nametag3d


class NametagGroup:
    CHAT_TIMEOUT_MIN = 4.0
    CHAT_TIMEOUT_MAX = 12.0

    CHAT_STOMP_DELAY = 0.2

    def __init__(self):
        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()

        self.avatar = None
        self.font = None
        self.chatType = NametagGlobals.CHAT
        self.chatBalloonType = NametagGlobals.CHAT_BALLOON
        self.active = False
        self.objectCode = None
        self.shadow = None

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

        self.stompText = ''
        self.stompTimeout = False

        self.chatTimeoutTask = None
        self.stompTask = None

    def destroy(self):
        if self.chatTimeoutTask is not None:
            taskMgr.remove(self.chatTimeoutTask)
            self.chatTimeoutTask = None
        if self.stompTask is not None:
            taskMgr.remove(self.stompTask)
            self.stompText = ''
            self.stompTimeout = False
            self.stompTask = None
        for nametag in list(self.nametags):
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

    def setActive(self, active):
        self.active = active
        for nametag in self.nametags:
            nametag.setActive(False)

    def getActive(self):
        return self.active

    def setObjectCode(self, objectCode):
        self.objectCode = objectCode

    def getObjectCode(self):
        return self.objectCode

    def setShadow(self, shadow):
        self.shadow = shadow
        for nametag in self.nametags:
            nametag.setShadow(self.shadow)

    def getShadow(self):
        return self.shadow

    def clearShadow(self):
        self.shadow = None
        for nametag in self.nametags:
            nametag.clearShadow()

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
        if self.chatTimeoutTask is not None:
            taskMgr.remove(self.chatTimeoutTask)
            self.chatTimeoutTask = None

        if self.stompTask is not None:
            taskMgr.remove(self.stompTask)
            self.stompText = ''
            self.stompTimeout = False
            self.stompTask = None

        if not self.chatText:
            self.chatText = chatText
            for nametag in self.nametags:
                nametag.setChatText(self.chatText)

            if timeout:
                delay = len(self.chatText) * 0.5
                if delay < NametagGroup.CHAT_TIMEOUT_MIN:
                    delay = NametagGroup.CHAT_TIMEOUT_MIN
                elif delay > NametagGroup.CHAT_TIMEOUT_MAX:
                    delay = NametagGroup.CHAT_TIMEOUT_MAX

                taskMgr.doMethodLater(
                    delay, self.__chatTimeout,
                    self.getUniqueName() + '-timeout')
        else:
            self.stompText = chatText
            self.stompTimeout = timeout
            taskMgr.doMethodLater(
                NametagGroup.CHAT_STOMP_DELAY, self.__chatStomp,
                self.getUniqueName() + '-stomp')

    def getChatText(self):
        return self.chatText

    def clearChatText(self):
        self.setChatText('')
        self.updateAll()

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

    def getStompText(self):
        return self.stompText

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

    def updateAll(self):
        for nametag in self.nametags:
            self.update(nametag)

    def manage(self, marginManager):
        pass

    def unmanage(self, marginManager):
        pass

    def hideNametag(self):
        for nametag in self.nametags:
            nametag.hideNametag()

    def showNametag(self):
        for nametag in self.nametags:
            nametag.showNametag()

    def hideChat(self):
        for nametag in self.nametags:
            nametag.hideChat()

    def showChat(self):
        for nametag in self.nametags:
            nametag.showChat()

    def hideThought(self):
        for nametag in self.nametags:
            nametag.hideThought()

    def showThought(self):
        for nametag in self.nametags:
            nametag.showThought()

    def __chatTimeout(self, task=None):
        self.clearChatText()

        if task is not None:
            return Task.done

    def __chatStomp(self, task=None):
        self.setChatText(self.stompText, timeout=self.stompTimeout)

        self.stompText = ''
        self.stompTimeout = False

        if task is not None:
            return Task.done
