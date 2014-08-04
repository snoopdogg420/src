from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from pandac.PandaModules import *

from otp.otpbase import OTPGlobals


class NametagManager(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNodePath = base.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(OTPGlobals.WallBitmask)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(self.pickerNodePath, self.pickerHandler)

        self.accept('mouse1', self.__handleMouseClick)

    def pick(self):
        if not base.mouseWatcherNode:
            return
        if not base.mouseWatcherNode.hasMouse():
            return
        mouse = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mouse.getX(), mouse.getY())
        base.cTrav.traverse(render)
        if self.pickerHandler.getNumEntries() > 0:
            self.pickerHandler.sortEntries()
            nodePath = self.pickerHandler.getEntry(0).getIntoNodePath()
            return nodePath

    def rolloverTask(self, task):
        nodePath = self.pick()
        if not nodePath:
            return
        return Task.cont

    def __handleMouseClick(self):
        nodePath = self.pick()
        if not nodePath:
            return
