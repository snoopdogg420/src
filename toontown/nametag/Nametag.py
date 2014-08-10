from direct.fsm import ClassicFSM, State
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from pandac.PandaModules import *

from otp.otpbase import OTPGlobals
from toontown.chat import ChatBalloon
from toontown.nametag import NametagGlobals


class Nametag(PandaNode, DirectObject):
    TEXT_Y_OFFSET = -0.05
    NAMETAG_X_PADDING = 0.2
    NAMETAG_Z_PADDING = 0.2

    def __init__(self):
        PandaNode.__init__(self, 'nametag')
        DirectObject.__init__(self)

        self.contents = NodePath.anyPath(self).attachNewNode('contents')

        self.avatar = None
        self.font = None
        self.chatType = NametagGlobals.CHAT
        self.chatBalloonType = NametagGlobals.CHAT_BALLOON
        self.active = False
        self.clickState = NametagGlobals.DISABLED
        self.lastClickState = NametagGlobals.DISABLED
        self.nametagHidden = False
        self.chatHidden = False
        self.thoughtHidden = False

        # Foreground, background:
        self.nametagColor = NametagGlobals.NametagColors[NametagGlobals.CCNormal]
        self.chatColor = NametagGlobals.ChatColors[NametagGlobals.CCNormal]
        self.speedChatColor = VBase4(1, 1, 1, 1)

        # Create our TextNodes:
        self.nameTextNode = TextNode('nameText')
        self.nameTextNode.setWordwrap(8)
        self.nameTextNode.setTextColor(self.nametagColor[self.clickState][0])
        self.nameTextNode.setAlign(TextNode.ACenter)

        self.chatTextNode = TextNode('chatText')
        self.chatTextNode.setWordwrap(12)
        self.chatTextNode.setTextColor(self.chatColor[self.clickState][0])
        self.chatTextNode.setGlyphScale(1.05)
        self.chatTextNode.setGlyphShift(-0.05)

        self.icon = None

        # Add the tick task:
        self.tickTask = taskMgr.add(self.tick, self.getUniqueName() + '-tick')

        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedBankInterior',
            [
                State.State('disabled', self.enterDisabled, self.exitDisabled,
                            ['normal', 'down', 'rollover']),
                State.State('normal', self.enterNormal, self.exitNormal,
                            ['down', 'rollover', 'disabled']),
                State.State('down', self.enterDown, self.exitDown,
                            ['rollover', 'disabled', 'normal']),
                State.State('rollover', self.enterRollover, self.exitRollover,
                            ['disabled', 'normal', 'down'])
            ], 'disabled', 'disabled')
        self.fsm.enterInitialState()

        self.pickerName = self.getUniqueName() + '-picker'
        self.accept(
            base.nametagMouseWatcher.getIntoEventName() % self.pickerName,
            self.__handleMouseEnter)
        base.accept(
            base.nametagMouseWatcher.getOutEventName() % self.pickerName,
            self.__handleMouseLeave)

    def destroy(self):
        if self.tickTask is not None:
            taskMgr.remove(self.tickTask)
            self.tickTask = None

        if self.icon is not None:
            self.icon.removeAllChildren()
            self.icon = None

        if self.contents:
            self.contents.removeNode()
            self.contents = None

        if self.chatTextNode:
            self.chatTextNode = None

        if self.nameTextNode:
            self.nameTextNode = None

        self.avatar = None
        self.font = None

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

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setFont(self, font):
        self.font = font
        if self.font:
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

    def setActive(self, active):
        self.active = active
        if self.active:
            self.setClickState(NametagGlobals.NORMAL)
        else:
            self.setClickState(NametagGlobals.DISABLED)

    def getActive(self):
        return self.active

    def setClickState(self, clickState):
        self.lastClickState = self.clickState
        self.clickState = clickState
        if self.clickState == NametagGlobals.NORMAL:
            self.fsm.request('normal')
        elif self.clickState == NametagGlobals.DOWN:
            self.fsm.request('down')
        elif self.clickState == NametagGlobals.ROLLOVER:
            self.fsm.request('rollover')
        elif self.clickState == NametagGlobals.DISABLED:
            self.fsm.request('disable')
        self.update()

    def getClickState(self):
        return self.clickState

    def getLastClickState(self):
        return self.lastClickState

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

    def setWordWrap(self, wordWrap):
        self.nameTextNode.setWordwrap(wordWrap)

    def getWordWrap(self):
        return self.nameTextNode.getWordwrap()

    def setChatWordWrap(self, chatWordWrap):
        self.chatTextNode.setWordwrap(chatWordWrap)

    def getChatWordWrap(self):
        return self.chatTextNode.getWordwrap()

    def setIcon(self, icon):
        self.icon = icon
        if not self.getChatText():
            self.update()

    def getIcon(self):
        return self.icon

    def setNameText(self, nameText):
        self.nameTextNode.setText(nameText)
        if not self.getChatText():
            self.update()

    def getNameText(self):
        return self.nameTextNode.getText()

    def setChatText(self, chatText):
        self.chatTextNode.setText(chatText)

    def getChatText(self):
        return self.chatTextNode.getText()

    def setShadow(self, shadow):
        self.nameTextNode.setShadow(shadow)

    def getShadow(self):
        return self.nameTextNode.getShadow()

    def clearShadow(self):
        self.nameTextNode.clearShadow()

    def update(self):
        """
        Redraw the contents that are visible.
        """
        self.contents.node().removeAllChildren()

        if self.getChatText():
            if self.chatBalloonType == NametagGlobals.CHAT_BALLOON:
                if self.chatHidden:
                    return
            elif self.chatBalloonType == NametagGlobals.THOUGHT_BALLOON:
                if self.thoughtHidden:
                    return

            self.drawChatBalloon()
            return

        if self.getNameText() and (not self.nametagHidden):
            self.drawNametag()

    def drawChatBalloon(self):
        if self.font is None:
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

        chatBalloon = ChatBalloon.ChatBalloon(
            model, modelWidth, modelHeight, self.chatTextNode,
            foreground=foreground, background=background)
        chatBalloon.reparentTo(self.contents)

        # Finally, draw the collisions:
        self.drawCollisions()

    def drawNametag(self):
        if self.font is None:
            # We can't draw this without a font.
            return

        foreground, background = self.nametagColor[self.clickState]

        # Attach the icon:
        if self.icon:
            self.contents.attachNewNode(self.icon)

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
        collNodePath.setCollideMask(OTPGlobals.WallBitmask)
        collBox = CollisionBox(*self.contents.getTightBounds())
        collNode.addSolid(collBox)

    def enterNormal(self):
        if self.lastClickState == NametagGlobals.DOWN:
            pass  # TODO: Send a message.

    def exitNormal(self):
        pass

    def enterDown(self):
        base.playSfx(NametagGlobals.clickSound)

    def exitDown(self):
        pass

    def enterRollover(self):
        base.playSfx(NametagGlobals.rolloverSound)

    def exitRollover(self):
        pass

    def enterDisabled(self):
        pass

    def exitDisabled(self):
        pass

    def __handleMouseEnter(self, collEntry=None):
        if self.clickState == NametagGlobals.DISABLED:
            return
        self.setClickState(NametagGlobals.ROLLOVER)

    def __handleMouseLeave(self, collEntry=None):
        if self.clickState == NametagGlobals.DISABLED:
            return
        self.setClickState(NametagGlobals.NORMAL)
