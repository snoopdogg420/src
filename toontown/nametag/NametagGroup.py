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

        self.icon = PandaNode('icon')

        self.avatar = None
        self.font = None
        self.chatType = NametagGlobals.CHAT
        self.chatBalloonType = NametagGlobals.CHAT_BALLOON
        self.active = False
        self.objectCode = None
        self.shadow = None

        self.nametagColor = NametagGlobals.NametagColors[NametagGlobals.CCNormal]
        self.chatColor = NametagGlobals.ChatColors[NametagGlobals.CCNormal]
        self.speedChatColor = VBase4(1, 1, 1, 1)

        self.wordWrap = 8
        self.chatWordWrap = 12

        self.nameText = ''
        self.stompChatText = ''
        self.chatPages = []
        self.chatPageIndex = 0

        self.chatTimeoutTask = None
        self.chatTimeoutTaskName = self.getUniqueName() + '-timeout'
        self.stompTask = None
        self.stompTaskName = self.getUniqueName() + '-stomp'

        self.nametags = set()
        self.add(self.nametag2d)
        self.add(self.nametag3d)

    def destroy(self):
        self.clearChatText()

        for nametag in list(self.nametags):
            self.remove(nametag)

        if self.icon:
            self.icon.removeAllChildren()
            self.icon = None

        self.avatar = None
        self.font = None

        if self.nametag2d:
            self.nametag2d = None
        if self.nametag3d:
            self.nametag3d = None

    def getUniqueName(self):
        return 'NametagGroup-' + str(id(self))

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
        nametag.setWordWrap(self.wordWrap)
        nametag.setChatWordWrap(self.chatWordWrap)
        nametag.setNameText(self.nameText)
        nametag.setChatText(self.getChatText())
        nametag.setIcon(self.icon)
        nametag.update()

    def updateAll(self):
        for nametag in self.nametags:
            self.update(nametag)

    def manage(self, marginManager):
        pass

    def unmanage(self, marginManager):
        pass

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
            nametag.setActive(self.active)

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

    def setWordWrap(self, wordWrap):
        self.wordWrap = wordWrap
        for nametag in self.nametags:
            nametag.setWordWrap(self.wordWrap)

    def getWordWrap(self):
        return self.wordWrap

    def setChatWordWrap(self, chatWordWrap):
        self.chatWordWrap = chatWordWrap
        for nametag in self.nametags:
            nametag.setChatWordWrap(self.chatWordWrap)

    def getChatWordWrap(self):
        return self.chatWordWrap

    def setNameText(self, nameText):
        self.nameText = nameText
        for nametag in self.nametags:
            nametag.setNameText(self.nameText)

    def getNameText(self):
        return self.nameText

    def getStompChatText(self):
        return self.stompChatText

    def setChatText(self, chatText, timeout=False):
        # If we are currently displaying chat text, we need to "stomp" it. In
        # other words, we need to clear the current chat text, pause for a
        # short time, then display the new chat text:
        if self.getChatText():
            self.clearChatText()
            self.stompChatText = chatText
            self.stompTask = taskMgr.doMethodLater(
                NametagGroup.CHAT_STOMP_DELAY, self.__chatStomp,
                self.stompTaskName, extraArgs=[timeout], appendTask=True)
            return

        self.clearChatText()

        self.chatPages = chatText.split('\x07')
        self.setChatPageIndex(0)

        if timeout:
            delay = len(self.getChatText()) * 0.5
            if delay < NametagGroup.CHAT_TIMEOUT_MIN:
                delay = NametagGroup.CHAT_TIMEOUT_MIN
            elif delay > NametagGroup.CHAT_TIMEOUT_MAX:
                delay = NametagGroup.CHAT_TIMEOUT_MAX
            self.chatTimeoutTask = taskMgr.doMethodLater(
                delay, self.clearChatText, self.chatTimeoutTaskName)

    def getChatText(self):
        if self.chatPageIndex >= self.getNumChatPages():
            return ''
        return self.chatPages[self.chatPageIndex]

    def clearChatText(self, task=None):
        if self.stompTask is not None:
            taskMgr.remove(self.stompTask)
            self.stompTask = None

        self.stompChatText = ''

        if self.chatTimeoutTask is not None:
            taskMgr.remove(self.chatTimeoutTask)
            self.chatTimeoutTask = None

        self.chatPages = []
        self.chatPageIndex = 0

        for nametag in self.nametags:
            nametag.setChatText('')
            nametag.update()

        if task is not None:
            return Task.done

    def getNumChatPages(self):
        return len(self.chatPages)

    def setChatPageIndex(self, chatPageIndex):
        if chatPageIndex >= self.getNumChatPages():
            return

        self.chatPageIndex = chatPageIndex
        for nametag in self.nametags:
            nametag.setChatText(self.chatPages[self.chatPageIndex])
            nametag.update()

    def getChatPageIndex(self):
        return self.chatPageIndex

    def setIcon(self, icon):
        self.icon = icon
        for nametag in self.nametags:
            nametag.setIcon(self.icon)

    def getIcon(self):
        return self.icon

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

    def __chatStomp(self, timeout=False, task=None):
        self.setChatText(self.stompChatText, timeout=timeout)
        self.stompChatText = ''

        if task is not None:
            return Task.done
