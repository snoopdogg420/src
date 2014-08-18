from direct.task.Task import Task
from pandac.PandaModules import *

from otp.otpbase import OTPGlobals


class NametagMouseWatcher:
    def __init__(self):
        self.cTrav = CollisionTraverser('NametagMouseWatcher.cTrav')

        self.pickerNode = CollisionNode(self.getUniqueName() + '-mouseRay')
        self.pickerNodePath = base.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(OTPGlobals.PickerBitmask)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)

        self.pickerHandler = CollisionHandlerEvent()
        self.pickerHandler.addInPattern('%fn-into-%in')
        self.pickerHandler.addOutPattern('%fn-out-%in')
        self.cTrav.addCollider(self.pickerNodePath, self.pickerHandler)

        self.updateRayTask = taskMgr.add(
            self.updateRay, self.getUniqueName() + '-updateRayTask', sort=0)

    def getUniqueName(self):
        return 'NametagMouseWatcher-' + str(id(self))

    def updateRay(self, task):
        if base.mouseWatcherNode.hasMouse():
            self.cTrav.traverse(render)
            mouse = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mouse.getX(), mouse.getY())
        return Task.cont

    def getIntoEventName(self):
        return self.getUniqueName() + '-mouseRay-into-%s'

    def getOutEventName(self):
        return self.getUniqueName() + '-mouseRay-out-%s'
