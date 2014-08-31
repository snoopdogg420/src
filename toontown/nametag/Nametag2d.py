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

    def destroy(self):
        Nametag.Nametag.destroy(self)

        if self.arrow:
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

    def updateClickRegion(self):
        self.setClickRegion(-0.1, 0.1, -0.1, 0.1)

    def tick(self, task):
        if (self.getCell() is None) or (self.arrow is None):
            return Task.cont

        if (self.avatar is None) or self.avatar.isEmpty():
            return Task.cont

        location = self.avatar.getPos(NametagGlobals.me)
        rotation = NametagGlobals.me.getQuat(base.cam)

        camSpacePos = rotation.xform(location)
        arrowRadians = math.atan2(camSpacePos[0], camSpacePos[1])
        arrowDegrees = (arrowRadians/math.pi) * 180

        self.arrow.setR(arrowDegrees - 90)
        return Task.cont

    def drawChatBalloon(self, model, modelWidth, modelHeight):
        self.setChatText(self.getText() + ': ' + self.getChatText())

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

        # Set the click region:
        self.updateClickRegion()

    def drawNametag(self):
        Nametag.Nametag.drawNametag(self)

        self.setPriority(0)

        # Add an arrow:
        self.arrow = NametagGlobals.arrowModel.copyTo(self.contents)
        self.arrow.setZ(self.ARROW_OFFSET + self.textNode.getBottom())
        self.arrow.setScale(self.ARROW_SCALE)
        self.arrow.setColor(self.nametagColor[0][0])

        left, right, bottom, top =  self.textNode.getFrameActual()
        self.updateClickRegion()

    def setClickRegion(self, left, right, bottom, top):
        return
        if not self.active:
            if self.frame is not None:
                self.frame.destroy()
                self.frame = None
            return

        # Get a transform matrix to position the points correctly according to
        # the nametag node:
        transform = self.contents.getNetTransform()

        # Get the inverse of the camera transform matrix:
        # Needed so that the camera transform will not be applied to the region
        # points twice.
        camTransform = base.cam.getNetTransform()
        camTransform = camTransform.getInverse()

        # Compose the inverse of the camera transform and the nametag node
        # transform:
        transform = camTransform.compose(transform)
        transform = transform.setQuat(Quat())

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

        if self.frame is not None:
            self.frame.destroy()
            self.frame = None
        self.frame = DirectFrame(frameColor=(1, 0, 0, 0.25), parent=render2d, frameSize=(left, right, bottom, top))
