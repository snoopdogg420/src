from direct.task.Task import Task
import math
from pandac.PandaModules import *
from direct.gui.DirectGui import *

from toontown.margins.MarginVisible import MarginVisible
from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals


class Nametag2d(Nametag.Nametag, MarginVisible):
    CONTENTS_SCALE = 0.25

    CHAT_TEXT_WORD_WRAP = 8

    CHAT_BALLOON_ALPHA = 0.4

    ARROW_OFFSET = -1.0
    ARROW_SCALE = 1.5

    def __init__(self):
        Nametag.Nametag.__init__(self)
        MarginVisible.__init__(self)

        self.arrow = None

        self.hideThought()
        self.contents.setScale(self.CONTENTS_SCALE)

        self.actualChatText = ''

    def destroy(self):
        Nametag.Nametag.destroy(self)

        if self.arrow is not None:
            self.arrow.removeNode()
            self.arrow = None

    def getUniqueName(self):
        return 'Nametag2d-' + str(id(self))

    def getChatBalloonModel(self):
        return NametagGlobals.chatBalloon2dModel

    def getChatBalloonWidth(self):
        return NametagGlobals.chatBalloon2dWidth

    def getChatBalloonHeight(self):
        return NametagGlobals.chatBalloon2dHeight

    def setChatText(self, chatText):
        Nametag.Nametag.setChatText(self, chatText)

        self.actualChatText = chatText

    def updateClickRegion(self):
        if self.chatBalloon is not None:
            width = self.chatBalloon.width
            height = self.chatBalloon.height

            left = -(width/2)
            right = width/2
            bottom = -(height/2)
            top = height/2

            self.setClickRegion(left, right, bottom, top)

        elif self.panel is not None:
            height = self.panelHeight
            width = self.panelWidth

            leftD = -width/2
            rightD = width/2
            bottomD = -height/2
            topD = height/2

            xCenter = (self.textNode.getLeft()+self.textNode.getRight())/2
            yCenter = (self.textNode.getTop()+self.textNode.getBottom())/2

            left = xCenter + leftD
            right = xCenter + rightD
            bottom = yCenter + bottomD
            top = yCenter + topD

            self.setClickRegion(left, right, bottom, top)

    def considerUpdateClickRegion(self):
        if (self.active or (self.getChatText() and (self.getChatButton() != NametagGlobals.noButton))) and (self.getCell() is not None):
            self.updateClickRegion()
        else:
            self.region.setActive(False)

    def update(self):
        Nametag.Nametag.update(self)

        self.considerUpdateClickRegion()

    def tick(self, task):
        if (self.avatar is None) or self.avatar.isEmpty():
            return Task.cont

        if (self.getCell() is None) or (self.arrow is None):
            return Task.cont

        location = self.avatar.getPos(NametagGlobals.me)
        rotation = NametagGlobals.me.getQuat(base.cam)

        camSpacePos = rotation.xform(location)
        arrowRadians = math.atan2(camSpacePos[0], camSpacePos[1])
        arrowDegrees = (arrowRadians/math.pi) * 180

        self.arrow.setR(arrowDegrees - 90)
        return Task.cont

    def drawChatBalloon(self, model, modelWidth, modelHeight):
        self.chatTextNode.setText(self.getText() + ': ' + self.actualChatText)

        # When a chat balloon is active, we need a slightly higher priority in
        # the margin system:
        self.setPriority(1)

        if self.arrow is not None:
            self.arrow.removeNode()
            self.arrow = None

        Nametag.Nametag.drawChatBalloon(self, model, modelWidth, modelHeight)

        # Calculate the center of the TextNode:
        left, right, bottom, top = self.chatTextNode.getFrameActual()
        center = self.contents.getRelativePoint(
            self.chatBalloon.textNodePath,
            ((left+right) / 2.0, 0, (bottom+top) / 2.0))

        # Translate the chat balloon along the inverse:
        self.chatBalloon.setPos(self.chatBalloon, -center)

    def drawNametag(self):
        Nametag.Nametag.drawNametag(self)

        self.setPriority(0)

        # Add an arrow:
        self.arrow = NametagGlobals.arrowModel.copyTo(self.contents)
        self.arrow.setZ(self.ARROW_OFFSET + self.textNode.getBottom())
        self.arrow.setScale(self.ARROW_SCALE)
        self.arrow.setColor(self.nametagColor[0][0])

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
