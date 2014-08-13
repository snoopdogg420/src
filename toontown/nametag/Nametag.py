from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from pandac.PandaModules import *

from otp.otpbase import OTPGlobals
from toontown.chat.ChatBalloon import ChatBalloon
from toontown.nametag import NametagGlobals


class Nametag(FSM, PandaNode, DirectObject):
    TEXT_Y_OFFSET = -0.05

    CHAT_TEXT_GLYPH_SCALE = 1.05
    CHAT_TEXT_GLYPH_SHIFT = -0.05

    NAMETAG_X_PADDING = 0.2
    NAMETAG_Z_PADDING = 0.2

    def __init__(self):
        FSM.__init__(self, 'nametag')
        PandaNode.__init__(self, 'nametag')
        DirectObject.__init__(self)

        self.active = True
        self.lastClickState = NametagGlobals.NORMAL
        self.clickState = NametagGlobals.NORMAL
        self.pendingClickState = NametagGlobals.NORMAL
        self.avatar = None

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

        self.icon = None

        # Create our TextNodes:
        self.nameTextNode = TextNode('nameText')
        self.nameTextNode.setWordwrap(8.0)
        self.nameTextNode.setTextColor(self.nametagColor[self.clickState][0])
        self.nameTextNode.setAlign(TextNode.ACenter)

        self.chatTextNode = TextNode('chatText')
        self.chatTextNode.setWordwrap(12.0)
        self.chatTextNode.setTextColor(self.chatColor[self.clickState][0])
        self.chatTextNode.setGlyphScale(ChatBalloon.TEXT_GLYPH_SCALE)
        self.chatTextNode.setGlyphShift(ChatBalloon.TEXT_GLYPH_SHIFT)

        self.font = None
        self.nameFont = None
        self.chatFont = None

        # Add the tick task:
        self.tickTaskName = self.getUniqueName() + '-tick'
        self.tickTask = taskMgr.add(self.tick, self.tickTaskName)

        # Accept the collision events:
        self.pickerName = self.getUniqueName() + '-picker'
        self.accept(
            base.nametagMouseWatcher.getIntoEventName() % self.pickerName,
            self.__handleMouseEnter)
        self.accept(
            base.nametagMouseWatcher.getOutEventName() % self.pickerName,
            self.__handleMouseLeave)
        self.accept('mouse1-down', self.__handleMouseDown)
        self.accept('mouse1-up', self.__handleMouseUp)

    def destroy(self):
        self.ignoreAll()

        if self.tickTask is not None:
            taskMgr.remove(self.tickTask)
            self.tickTask = None

        self.font = None
        self.chatFont = None
        self.nameFont = None

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
        pass  # Inheritors should override this method.

    def getThoughtBalloonWidth(self):
        pass  # Inheritors should override this method.

    def getThoughtBalloonHeight(self):
        pass  # Inheritors should override this method.

    def tick(self, task):
        return Task.cont  # Inheritors should override this method.

    def setActive(self, active):
        self.active = active
        if self.active:
            self.setClickState(NametagGlobals.NORMAL)
        else:
            self.setClickState(NametagGlobals.DISABLED)

    def getActive(self):
        return self.active

    def setLastClickState(self, lastClickState):
        self.lastClickState = lastClickState

    def getLastClickState(self):
        return self.lastClickState

    def setClickState(self, clickState):
        self.lastClickState = self.clickState
        self.clickState = clickState
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

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

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
        if not self.getChatText():
            self.update()

    def getNametagColor(self):
        return self.nametagColor

    def setChatColor(self, chatColor):
        self.chatColor = chatColor
        if self.getChatText() and (self.chatType == NametagGlobals.CHAT):
            self.update()

    def getChatColor(self):
        return self.chatColor

    def setSpeedChatColor(self, speedChatColor):
        self.speedChatColor = speedChatColor
        if self.getChatText() and (self.chatType == NametagGlobals.SPEEDCHAT):
            self.update()

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

    def setIcon(self, icon):
        self.icon = icon
        if not self.getChatText():
            self.update()

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

    def setNameText(self, nameText):
        self.nameTextNode.setText(nameText)

    def getNameText(self):
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

    def update(self):
        """
        Redraw the contents that are visible.
        """
        self.contents.node().removeAllChildren()

        if self.getChatText():
            if self.chatBalloonType == NametagGlobals.CHAT_BALLOON:
                if not self.chatHidden:
                    self.drawChatBalloon()
                    return
            elif self.chatBalloonType == NametagGlobals.THOUGHT_BALLOON:
                if not self.thoughtHidden:
                    self.drawChatBalloon()
                    return

        if self.getNameText() and (not self.nametagHidden):
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

        chatBalloon = ChatBalloon(
            model, modelWidth, modelHeight, self.chatTextNode,
            foreground=foreground, background=background)
        chatBalloon.reparentTo(self.contents)

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
        nameText = self.contents.attachNewNode(self.nameTextNode, 1)
        nameText.setTransparency(foreground[3] < 1)
        nameText.setAttrib(DepthWriteAttrib.make(0))
        nameText.setY(Nametag.TEXT_Y_OFFSET)

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

        # Finally, draw the collisions:
        self.drawCollisions()

    def drawCollisions(self):
        collNode = CollisionNode(self.pickerName)
        collNodePath = self.contents.attachNewNode(collNode)
        collNodePath.setCollideMask(OTPGlobals.PickerBitmask)
        collBox = CollisionBox(*self.contents.getTightBounds())
        collNode.addSolid(collBox)

    def enterNormal(self):
        if self.lastClickState == NametagGlobals.DOWN:
            pass  # TODO: Send a message.
        # TODO: Set the normal colors.

    def enterDown(self):
        base.playSfx(NametagGlobals.clickSound)
        # TODO: Set the down colors.

    def enterRollover(self):
        if self.lastClickState == NametagGlobals.DOWN:
            pass  # TODO: Send a message.
        else:
            base.playSfx(NametagGlobals.rolloverSound)
        # TODO: Set the rollover colors.

    def enterDisabled(self):
        pass  # TODO: Set the disabled colors.

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
            self.setClickState(self.pendingClickSate)
