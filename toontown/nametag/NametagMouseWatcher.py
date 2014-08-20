from direct.task.Task import Task
from pandac.PandaModules import *

from otp.otpbase import OTPGlobals


class NametagMouseWatcher:
    def __init__(self):
        self.cTrav = CollisionTraverser('NametagMouseWatcher.cTrav')

        self.pickerNode = CollisionNode('NametagMouseWatcher-mouseRay')
        self.pickerNode.setFromCollideMask(OTPGlobals.PickerBitmask)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.pickerNodePath = base.camera.attachNewNode(self.pickerNode)

        self.pickerHandler = CollisionHandlerEvent()
        self.pickerHandler.addInPattern('%fn-into-%in')
        self.pickerHandler.addOutPattern('%fn-out-%in')
        self.cTrav.addCollider(self.pickerNodePath, self.pickerHandler)

        self.updateRayTask = taskMgr.add(
            self.updateRay, 'NametagMouseWatcher-updateRayTask', sort=0)

    def updateRay(self, task):
        if base.mouseWatcherNode.hasMouse():
            mouse = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mouse.getX(), mouse.getY())
            self.cTrav.traverse(render)
        return Task.cont

    def getIntoEventName(self):
        return self.getUniqueName() + '-mouseRay-into-%s'

    def getOutEventName(self):
        return self.getUniqueName() + '-mouseRay-out-%s'
