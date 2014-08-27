from direct.task.Task import Task
import math
from pandac.PandaModules import *

from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals

from toontown.chat import ChatBalloon


class Nametag3d(Nametag.Nametag):
    SCALING_MIN_DISTANCE = 1
    SCALING_MAX_DISTANCE = 50
    SCALING_FACTOR = 0.06

    def __init__(self):
        Nametag.Nametag.__init__(self)

        self.distance = 0
        self.scale = 1

        self.type = '3d'

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
            width = self.panelWidth * self.scale
            height = self.panelHeight * self.scale

            left = -width/2
            right = width/2
            bottom = -height/2
            top = height/2

            self.setClickRegion(left, right, bottom, top)

        if self.chatBalloon is not None:
            width = self.chatBalloon.width * self.scale
            height = self.chatBalloon.height * self.scale

            left = 0
            right = width

            scaledModelHeight = self.chatBalloon.modelHeight*self.scale
            bottom = scaledModelHeight-(2.35*self.scale)
            top = bottom+height

            self.setClickRegion(left, right, bottom, top)

    def tick(self, task):
        distance = self.contents.getPos(base.cam).length()

        if distance < self.SCALING_MIN_DISTANCE:
            distance = self.SCALING_MIN_DISTANCE
        elif distance > self.SCALING_MAX_DISTANCE:
            distance = self.SCALING_MAX_DISTANCE

        if distance == self.distance:
            self.updateClickRegion()
            return Task.cont

        self.distance = distance

        self.scale = math.sqrt(distance) * self.SCALING_FACTOR
        self.contents.setScale(self.scale)

        self.updateClickRegion()

        return Task.cont
