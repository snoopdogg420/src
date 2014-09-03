from direct.fsm.FSM import FSM
from pandac.PandaModules import *

from toontown.chat import ChatGlobals
from toontown.chat.ChatBalloon import ChatBalloon
from toontown.margins.MarginVisible import MarginVisible
from toontown.nametag import NametagGlobals
from direct.showbase.DirectObject import DirectObject

class WhisperPopup(FSM, PandaNode, MarginVisible, DirectObject):
    CONTENTS_SCALE = 0.25

    TEXT_WORD_WRAP = 8

    def __init__(self, text, font, whisperType, timeout=10):
        FSM.__init__(self, 'whisper')
        PandaNode.__init__(self, 'whisper')
        MarginVisible.__init__(self)
        DirectObject.__init__(self)

        self.text = text
        self.font = font
        self.whisperType = whisperType
        self.timeout = timeout

        self.active = False
        self.senderName = ''
        self.fromId = 0
        self.isPlayer = 0

        self.lastClickState = PGButton.SInactive
        self.clickState = PGButton.SInactive
        self.pendingClickState = PGButton.SInactive

        self.clickEvent = ''
        self.clickExtraArgs = []

        self.contents = NodePath.anyPath(self).attachNewNode('contents')
        self.contents.setScale(self.CONTENTS_SCALE)

        self.whisperColor = ChatGlobals.WhisperColors[self.whisperType]

        self.textNode = TextNode('text')
        self.textNode.setWordwrap(self.TEXT_WORD_WRAP)
        self.textNode.setTextColor(self.whisperColor[self.clickState][0])
        self.textNode.setFont(self.font)
        self.textNode.setText(self.text)

        self.chatBalloon = None

        self.setPriority(2)
        self.setVisible(True)

        self.timeoutTaskName = self.getUniqueName() + '-timeout'
        self.timeoutTask = None

        # Create the click region:
        self.regionName = self.getUniqueName() + '-region'
        self.region = MouseWatcherRegion(self.regionName, 0, 0, 0, 0)
        base.mouseWatcherNode.addRegion(self.region)

        # Accept the mouse events:
        self.accept(base.mouseWatcherNode.getEnterPattern().replace('%r', self.regionName), self.__handleMouseEnter)
        self.accept(base.mouseWatcherNode.getLeavePattern().replace('%r', self.regionName), self.__handleMouseLeave)
        self.accept(base.mouseWatcherNode.getButtonDownPattern().replace('%r', self.regionName), self.__handleMouseDown)
        self.accept(base.mouseWatcherNode.getButtonUpPattern().replace('%r', self.regionName), self.__handleMouseUp)

        self.update()

    def destroy(self):
        if self.timeoutTask is not None:
            taskMgr.remove(self.timeoutTask)
            self.timeoutTask = None

        self.chatBalloon = None

        if self.textNode is not None:
            self.textNode = None

        if self.contents is not None:
            self.contents.removeNode()
            self.contents = None

    def getUniqueName(self):
        return 'WhisperPopup-' + str(id(self))

    def update(self):
        foreground, background = self.whisperColor[self.clickState]

        self.chatBalloon = ChatBalloon(
            NametagGlobals.chatBalloon2dModel,
            NametagGlobals.chatBalloon2dWidth,
            NametagGlobals.chatBalloon2dHeight, self.textNode,
            foreground=foreground, background=background
        )
        self.chatBalloon.reparentTo(self.contents)

        # Calculate the center of the TextNode:
        left, right, bottom, top = self.textNode.getFrameActual()
        center = self.contents.getRelativePoint(
            self.chatBalloon.textNodePath,
            ((left+right) / 2.0, 0, (bottom+top) / 2.0))

        # Translate the chat balloon along the inverse:
        self.chatBalloon.setPos(self.chatBalloon, -center)

        # Update the click region if necessary:
        self.considerUpdateClickRegion()

    def manage(self, marginManager):
        MarginVisible.manage(self, marginManager)

        self.timeoutTask = taskMgr.doMethodLater(
            self.timeout, self.unmanage, self.timeoutTaskName, [marginManager])

    def unmanage(self, marginManager):
        MarginVisible.unmanage(self, marginManager)

        self.destroy()

    def setClickable(self, senderName, fromId, isPlayer=0):
        self.senderName = senderName
        self.fromId = fromId
        self.isPlayer = isPlayer
        self.active = True
        self.clickEvent = 'clickedWhisper'
        self.clickExtraArgs = [self.fromId, self.isPlayer]
        self.region.setActive(True)
        self.setClickState(PGButton.SReady)

    def setLastClickState(self, lastClickState):
        self.lastClickState = lastClickState

    def getLastClickState(self):
        return self.lastClickState

    def setClickState(self, clickState):
        self.lastClickState = self.clickState
        self.clickState = clickState

        if self.chatBalloon is not None:
            foreground, background = self.whisperColor[self.clickState]
            self.chatBalloon.setForeground(foreground)
            self.chatBalloon.setBackground(background)

        if self.clickState == PGButton.SReady:
            self.request('Normal')
        elif self.clickState == PGButton.SDepressed:
            self.request('Down')
        elif self.clickState == PGButton.SRollover:
            self.request('Rollover')
        elif self.clickState == PGButton.SInactive:
            self.request('Disabled')

    def getClickState(self):
        return self.clickState

    def setPendingClickState(self, pendingClickState):
        self.pendingClickState = pendingClickState

    def getPendingClickState(self):
        return self.pendingClickState

    def enterNormal(self):
        if self.lastClickState == PGButton.SDepressed:
            messenger.send(self.clickEvent, self.clickExtraArgs)

    def enterDown(self):
        base.playSfx(NametagGlobals.clickSound)

    def enterRollover(self):
        if self.lastClickState == PGButton.SDepressed:
            messenger.send(self.clickEvent, self.clickExtraArgs)
        else:
            base.playSfx(NametagGlobals.rolloverSound)

    def enterDisabled(self):
        pass

    def __handleMouseEnter(self, region, extra):
        self.pendingClickState = PGButton.SRollover
        if self.clickState == PGButton.SReady:
            self.setClickState(PGButton.SRollover)

    def __handleMouseLeave(self, region, extra):
        self.pendingClickState = PGButton.SReady
        if self.clickState == PGButton.SRollover:
            self.setClickState(PGButton.SReady)

    def __handleMouseDown(self, region, button):
        if self.clickState == PGButton.SRollover:
            self.setClickState(PGButton.SDepressed)

    def __handleMouseUp(self, region, button):
        if self.clickState == PGButton.SDepressed:
            self.setClickState(self.pendingClickState)

    def updateClickRegion(self):
        if self.chatBalloon is not None:
            right = self.chatBalloon.width / 2
            left = -right
            top = self.chatBalloon.height / 2
            bottom = -top

            self.setClickRegion(left, right, bottom, top)

    def considerUpdateClickRegion(self):
        if self.active and (self.getCell() is not None):
            self.updateClickRegion()
        else:
            if self.region is not None:
                self.region.setActive(False)

    def setClickRegion(self, left, right, bottom, top):
        # Get a transform matrix to position the points correctly according to
        # the nametag node:
        transform = self.contents.getNetTransform()

        # Get the actual matrix of the transform above:
        mat = transform.getMat()

        # Transform the specified points to the new matrix:
        camSpaceTopLeft = mat.xformPoint(Point3(left, 0, top))
        camSpaceBottomRight = mat.xformPoint(Point3(right, 0, bottom))

        screenSpaceTopLeft = Point2(camSpaceTopLeft[0], camSpaceTopLeft[2])
        screenSpaceBottomRight = Point2(camSpaceBottomRight[0], camSpaceBottomRight[2])

        left, top = screenSpaceTopLeft
        right, bottom = screenSpaceBottomRight

        self.region.setFrame(left, right, bottom, top)
        self.region.setActive(True)

    def marginVisibilityChanged(self):
        self.considerUpdateClickRegion()
