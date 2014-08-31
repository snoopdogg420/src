from direct.gui.DirectGui import *
from direct.task.Task import Task
import math
from pandac.PandaModules import *

from toontown.chat import ChatBalloon
from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals


class Nametag3d(Nametag.Nametag):
    SCALING_MIN_DISTANCE = 1
    SCALING_MAX_DISTANCE = 50
    SCALING_FACTOR = 0.065

    def __init__(self):
        Nametag.Nametag.__init__(self)

        self.distance = 0
        self.scale = 1

        self.billboardOffset = 3
        self.doBillboardEffect()

    def getUniqueName(self):
        return 'Nametag3d-' + str(id(self))

    def getChatBalloonModel(self):
        return NametagGlobals.chatBalloon3dModel

    def getChatBalloonWidth(self):
        return NametagGlobals.chatBalloon3dWidth

    def getChatBalloonHeight(self):
        return NametagGlobals.chatBalloon3dHeight

    def setBillboardOffset(self, billboardOffset):
        self.billboardOffset = billboardOffset
        self.doBillboardEffect()

    def getBillboardOffset(self):
        return self.billboardOffset

    def doBillboardEffect(self):
        billboardEffect = BillboardEffect.make(
            Vec3(0, 0, 1), True, False, self.billboardOffset, base.cam,
            Point3(0, 0, 0))
        self.contents.setEffect(billboardEffect)

    def updateClickRegion(self):
        if self.panel is not None:
            width = self.panelWidth
            height = self.panelHeight

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

        if self.chatBalloon is not None:
            width = self.chatBalloon.width
            height = self.chatBalloon.height

            left = self.chatBalloon.center[0]-(width/2)
            right = left+width

            # Calculate the bottom of the region based on constants:
            # 2.4 is equal to the padded height of a one line message
            bottom = self.chatBalloon.modelHeight-2.4
            top = bottom+height

            self.setClickRegion(left, right, bottom, top)

    def tick(self, task):
        distance = self.contents.getPos(base.cam).length()

        if distance < self.SCALING_MIN_DISTANCE:
            distance = self.SCALING_MIN_DISTANCE
        elif distance > self.SCALING_MAX_DISTANCE:
            distance = self.SCALING_MAX_DISTANCE

        if distance == self.distance:
            if self.active or (self.getChatButton() != NametagGlobals.noButton):
                self.updateClickRegion()
            return Task.cont

        self.distance = distance

        self.scale = math.sqrt(distance) * self.SCALING_FACTOR
        self.contents.setScale(self.scale)

        if self.active or (self.getChatButton() != NametagGlobals.noButton):
            self.updateClickRegion()

        return Task.cont

    def setClickRegion(self, left, right, bottom, top):
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
        camSpaceTopLeft = mat.xformPoint(Point3(float(left), 0, float(top)))
        camSpaceBottomRight = mat.xformPoint(Point3(float(right), 0, float(bottom)))

        screenSpaceTopLeft = Point2()
        screenSpaceBottomRight = Point2()

        # Project the converted points onto the lens:
        lens = base.camLens
        if not (lens.project(Point3(camSpaceTopLeft), screenSpaceTopLeft) and
                lens.project(Point3(camSpaceBottomRight), screenSpaceBottomRight)):
            self.region.setActive(False)
            return
        left, top = screenSpaceTopLeft
        right, bottom = screenSpaceBottomRight

        self.region.setFrame(left, right, bottom, top)
        self.region.setActive(True)
