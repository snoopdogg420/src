from direct.task.Task import Task
import math
from pandac.PandaModules import *

from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals


class Nametag3d(Nametag.Nametag):
    SCALING_MIN_DISTANCE = 1
    SCALING_MAX_DISTANCE = 50
    SCALING_FACTOR = 0.06

    def __init__(self):
        Nametag.Nametag.__init__(self)

        self.distance = 0

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

    def tick(self, task):
        if not base.cam.node().isInView(self.avatar.getPos(base.cam)):
            return Task.cont

        distance = self.contents.getPos(base.cam).length()

        if distance < self.SCALING_MIN_DISTANCE:
            distance = self.SCALING_MIN_DISTANCE
        elif distance > self.SCALING_MAX_DISTANCE:
            distance = self.SCALING_MAX_DISTANCE

        if distance == self.distance:
            return Task.cont

        self.distance = distance

        self.contents.setScale(math.sqrt(distance) * self.SCALING_FACTOR)
        return Task.cont
