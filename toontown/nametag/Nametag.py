from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from pandac.PandaModules import *

from otp.otpbase import OTPGlobals
from toontown.chat.ChatBalloon import ChatBalloon
from toontown.nametag import NametagGlobals


class Nametag(FSM, PandaNode, DirectObject):
    TEXT_Y_OFFSET = -0.05

    NAMETAG_X_PADDING = 0.2
    NAMETAG_Z_PADDING = 0.2

    def __init__(self):
        FSM.__init__(self, 'nametag')
        PandaNode.__init__(self, 'nametag')
        DirectObject.__init__(self)

        self.active = True
        self.avatar = None

        self.lastClickState = NametagGlobals.NORMAL
        self.clickState = NametagGlobals.NORMAL
        self.pendingClickState = NametagGlobals.NORMAL

        self.nametagHidden = False
        self.chatHidden = False
        self.thoughtHidden = False

        self.nametagColor = NametagGlobals.NametagColors[NametagGlobals.CCNormal]
        self.chatColor = NametagGlobals.ChatColors[NametagGlobals.CCNormal]
        self.speedChatColor = VBase4(1, 1, 1, 1)

        self.chatType = NametagGlobals.CHAT
        self.chatBalloonType = NametagGlobals.CHAT_BALLOON

        # Create the container of our geometry:
        self.contents = NodePath.anyPath(self).attachNewNode('contents')

        self.button = None
        self.icon = None

        # Create our TextNodes:
        self.nameTextNode = TextNode('nameText')
        self.nameTextNode.setWordwrap(8)
        self.nameTextNode.setTextColor(self.nametagColor[self.clickState][0])
        self.nameTextNode.setAlign(TextNode.ACenter)

        self.chatTextNode = TextNode('chatText')
        self.chatTextNode.setWordwrap(12)
        self.chatTextNode.setTextColor(self.chatColor[self.clickState][0])
        self.chatTextNode.setGlyphScale(ChatBalloon.TEXT_GLYPH_SCALE)
        self.chatTextNode.setGlyphShift(ChatBalloon.TEXT_GLYPH_SHIFT)

        self.font = None
        self.nameFont = None
        self.chatFont = None

        self.chatBalloon = None
        self.namePanel = None

        # Add the tick task:
        self.tickTaskName = self.getUniqueName() + '-tick'
        self.tickTask = taskMgr.add(self.tick, self.tickTaskName, sort=45)

        # Accept the collision events:
        self.pickerName = self.getUniqueName() + '-picker'
        self.accept(
            base.nametagMouseWatcher.getIntoEventName() % self.pickerName,
            self.__handleMouseEnter)
        self.accept(
            base.nametagMouseWatcher.getOutEventName() % self.pickerName,
            self.__handleMouseLeave)
        self.accept('mouse1', self.__handleMouseDown)
        self.accept('mouse1-up', self.__handleMouseUp)

    def destroy(self):
        self.ignoreAll()

        if self.tickTask is not None:
            taskMgr.remove(self.tickTask)
            self.tickTask = None

        self.namePanel = None
        self.chatBalloon = None

        self.nameFont = None
        self.chatFont = None
        self.font = None

        if self.chatTextNode:
            self.chatTextNode = None

        if self.nameTextNode:
            self.nameTextNode = None

        if self.icon is not None:
            self.icon.removeAllChildren()
            self.icon = None

        if self.contents:
            self.contents.removeNode()
            self.contents = None

        self.avatar = None

    def getUniqueName(self):
        return 'Nametag-' + str(id(self))

    def getChatBalloonModel(self):
        pass  # Inheritors should override this method.

    def getChatBalloonWidth(self):
        pass  # Inheritors should override this method.

    def getChatBalloonHeight(self):
        pass  # Inheritors should override this method.

    def getThoughtBalloonModel(self):
        return NametagGlobals.thoughtBalloonModel

    def getThoughtBalloonWidth(self):
        return NametagGlobals.thoughtBalloonWidth

    def getThoughtBalloonHeight(self):
        return NametagGlobals.thoughtBalloonHeight

    def tick(self, task):
        return Task.done  # Inheritors should override this method.

    def setActive(self, active):
        self.active = active
        if self.active:
            self.setClickState(NametagGlobals.NORMAL)
        else:
            self.setClickState(NametagGlobals.DISABLED)

    def getActive(self):
        return self.active

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setLastClickState(self, lastClickState):
        self.lastClickState = lastClickState

    def getLastClickState(self):
        return self.lastClickState

    def setClickState(self, clickState):
        self.lastClickState = self.clickState
        self.clickState = clickState

        if self.chatBalloon is not None:
            foreground, background = self.chatColor[self.clickState]
            if self.chatType == NametagGlobals.SPEEDCHAT:
                background = self.speedChatColor
            self.chatBalloon.setForeground(foreground)
            self.chatBalloon.setBackground(background)
        elif self.namePanel is not None:
            foreground, background = self.nametagColor[self.clickState]
            self.setForeground(foreground)
            self.setBackground(background)

        if self.clickState == NametagGlobals.NORMAL:
            self.request('Normal')
        elif self.clickState == NametagGlobals.DOWN:
            self.request('Down')
        elif self.clickState == NametagGlobals.ROLLOVER:
            self.request('Rollover')
        elif self.clickState == NametagGlobals.DISABLED:
            self.request('Disabled')

    def getClickState(self):
        return self.clickState

    def setPendingClickState(self, pendingClickState):
        self.pendingClickState = pendingClickState

    def getPendingClickState(self):
        return self.pendingClickState

    def hideNametag(self):
        self.nametagHidden = True

    def showNametag(self):
        self.nametagHidden = False

    def hideChat(self):
        self.chatHidden = True

    def showChat(self):
        self.chatHidden = False

    def hideThought(self):
        self.thoughtHidden = True

    def showThought(self):
        self.thoughtHidden = False

    def setNametagColor(self, nametagColor):
        self.nametagColor = nametagColor

    def getNametagColor(self):
        return self.nametagColor

    def setChatColor(self, chatColor):
        self.chatColor = chatColor

    def getChatColor(self):
        return self.chatColor

    def setSpeedChatColor(self, speedChatColor):
        self.speedChatColor = speedChatColor

    def getSpeedChatColor(self):
        return self.speedChatColor

    def setChatType(self, chatType):
        self.chatType = chatType

    def getChatType(self):
        return self.chatType

    def setChatBalloonType(self, chatBalloonType):
        self.chatBalloonType = chatBalloonType

    def getChatBalloonType(self):
        return self.chatBalloonType

    def setButton(self, button):
        self.button = button

    def getButton(self):
        return self.button

    def setIcon(self, icon):
        self.icon = icon

    def getIcon(self):
        return self.icon

    def setWordWrap(self, wordWrap):
        self.nameTextNode.setWordwrap(wordWrap)

    def getWordWrap(self):
        return self.nameTextNode.getWordwrap()

    def setChatWordWrap(self, chatWordWrap):
        self.chatTextNode.setWordwrap(chatWordWrap)

    def getChatWordWrap(self):
        return self.chatTextNode.getWordwrap()

    def setShadow(self, shadow):
        self.nameTextNode.setShadow(shadow)

    def getShadow(self):
        return self.nameTextNode.getShadow()

    def clearShadow(self):
        self.nameTextNode.clearShadow()

    def setText(self, text):
        self.nameTextNode.setText(text)

    def getText(self):
        return self.nameTextNode.getText()

    def setChatText(self, chatText):
        self.chatTextNode.setText(chatText)

    def getChatText(self):
        return self.chatTextNode.getText()

    def setFont(self, font):
        self.font = font
        if self.font is not None:
            self.setNameFont(self.font)
            self.setChatFont(self.font)

    def getFont(self):
        return self.font

    def setNameFont(self, nameFont):
        self.nameFont = nameFont
        if self.nameFont is not None:
            self.nameTextNode.setFont(self.nameFont)

    def getNameFont(self):
        return self.nameFont

    def setChatFont(self, chatFont):
        self.chatFont = chatFont
        if self.chatFont is not None:
            self.chatTextNode.setFont(self.chatFont)

    def getChatFont(self):
        return self.chatFont

    def setForeground(self, foreground):
        self.nameTextNode.setTextColor(foreground)

    def setBackground(self, background):
        if self.namePanel is not None:
            self.namePanel.setColor(background)

    def update(self):
        """
        Redraw the contents that are visible.
        """
        self.contents.node().removeAllChildren()

        self.chatBalloon = None
        self.namePanel = None

        if self.getChatText():
            if self.chatBalloonType == NametagGlobals.CHAT_BALLOON:
                if not self.chatHidden:
                    self.drawChatBalloon()
                    return
            elif self.chatBalloonType == NametagGlobals.THOUGHT_BALLOON:
                if not self.thoughtHidden:
                    self.drawChatBalloon()
                    return

        if self.getText() and (not self.nametagHidden):
            self.drawNametag()

    def drawChatBalloon(self):
        if self.chatFont is None:
            # We can't draw this without a font.
            return

        if self.chatBalloonType == NametagGlobals.CHAT_BALLOON:
            model = self.getChatBalloonModel()
            modelWidth = self.getChatBalloonWidth()
            modelHeight = self.getChatBalloonHeight()
        elif self.chatBalloonType == NametagGlobals.THOUGHT_BALLOON:
            model = self.getThoughtBalloonModel()
            modelWidth = self.getThoughtBalloonWidth()
            modelHeight = self.getThoughtBalloonHeight()

        foreground, background = self.chatColor[self.clickState]
        if self.chatType == NametagGlobals.SPEEDCHAT:
            background = self.speedChatColor

        button = None
        if self.button is not None:
            button = self.button[self.clickState]

        self.chatBalloon = ChatBalloon(
            model, modelWidth, modelHeight, self.chatTextNode,
            foreground=foreground, background=background, button=button)
        self.chatBalloon.reparentTo(self.contents)

        # Finally, draw the collisions:
        self.drawCollisions()

    def drawNametag(self):
        if self.nameFont is None:
            # We can't draw this without a font.
            return

        # Attach the icon:
        if self.icon is not None:
            self.contents.attachNewNode(self.icon)

        foreground, background = self.nametagColor[self.clickState]

        # Set the color of the TextNode:
        self.nameTextNode.setTextColor(foreground)

        # Attach the TextNode:
        textNodePath = self.contents.attachNewNode(self.nameTextNode, 1)
        textNodePath.setTransparency(foreground[3] < 1)
        textNodePath.setAttrib(DepthWriteAttrib.make(0))
        textNodePath.setY(Nametag.TEXT_Y_OFFSET)

        # Attach a panel behind the TextNode:
        self.namePanel = NametagGlobals.cardModel.copyTo(self.contents, 0)
        x = (self.nameTextNode.getLeft()+self.nameTextNode.getRight()) / 2.0
        z = (self.nameTextNode.getTop()+self.nameTextNode.getBottom()) / 2.0
        self.namePanel.setPos(x, 0, z)
        sX = self.nameTextNode.getWidth() + Nametag.NAMETAG_X_PADDING
        sZ = self.nameTextNode.getHeight() + Nametag.NAMETAG_Z_PADDING
        self.namePanel.setScale(sX, 1, sZ)
        self.namePanel.setColor(background)
        self.namePanel.setTransparency(background[3] < 1)

        # Finally, draw the collisions:
        self.drawCollisions()

    def drawCollisions(self):
        if (self.chatBalloon is None) and (self.namePanel is None):
            return
        collNode = CollisionNode(self.pickerName)
        collNodePath = self.contents.attachNewNode(collNode)
        collNodePath.setCollideMask(OTPGlobals.PickerBitmask)
        if self.chatBalloon is not None:
            minPoint, maxPoint = self.chatBalloon.getTightBounds()
        else:
            minPoint, maxPoint = self.namePanel.getTightBounds()
        maxPoint.setY(0.05)
        collBox = CollisionBox(minPoint, maxPoint)
        collNode.addSolid(collBox)

    def enterNormal(self):
        if self.lastClickState == NametagGlobals.DOWN:
            pass  # TODO: Send a message.

    def enterDown(self):
        base.playSfx(NametagGlobals.clickSound)

    def enterRollover(self):
        if self.lastClickState == NametagGlobals.DOWN:
            pass  # TODO: Send a message.
        else:
            base.playSfx(NametagGlobals.rolloverSound)

    def enterDisabled(self):
        pass

    def __handleMouseEnter(self, collEntry=None):
        self.pendingClickState = NametagGlobals.ROLLOVER
        if self.clickState == NametagGlobals.NORMAL:
            self.setClickState(NametagGlobals.ROLLOVER)

    def __handleMouseLeave(self, collEntry=None):
        self.pendingClickState = NametagGlobals.NORMAL
        if self.clickState == NametagGlobals.ROLLOVER:
            self.setClickState(NametagGlobals.NORMAL)

    def __handleMouseDown(self):
        if self.clickState == NametagGlobals.ROLLOVER:
            self.setClickState(NametagGlobals.DOWN)

    def __handleMouseUp(self):
        if self.clickState == NametagGlobals.DOWN:
            self.setClickState(self.pendingClickState)
