from direct.task.Task import Task
import math
from pandac.PandaModules import *

from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals


class Nametag3d(Nametag.Nametag):
    SCALING_MIN_DISTANCE = 1
    SCALING_MAX_DISTANCE = 50
    SCALING_FACTOR = 0.055

    def __init__(self):
        Nametag.Nametag.__init__(self)

        self.billboardOffset = 3
        self.doBillboardEffect()

    def getChatBalloonModel(self):
        return NametagGlobals.chatBalloon3dModel

    def getChatBalloonWidth(self):
        return NametagGlobals.chatBalloon3dWidth

    def getChatBalloonHeight(self):
        return NametagGlobals.chatBalloon3dHeight

    def getThoughtBalloonModel(self):
        return NametagGlobals.thoughtBalloonModel

    def getThoughtBalloonWidth(self):
        return NametagGlobals.thoughtBalloonWidth

    def getThoughtBalloonHeight(self):
        return NametagGlobals.thoughtBalloonHeight

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
        distance = self.contents.getPos(base.cam).length()

        if distance < Nametag3d.SCALING_MIN_DISTANCE:
            distance = Nametag3d.SCALING_MIN_DISTANCE
        elif distance > Nametag3d.SCALING_MAX_DISTANCE:
            distance = Nametag3d.SCALING_MAX_DISTANCE

        self.contents.setScale(math.sqrt(distance) * Nametag3d.SCALING_FACTOR)
        return Task.cont
