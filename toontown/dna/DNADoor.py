from pandac.PandaModules import LVector4f, DecalEffect, ModelNode

from toontown.dna.DNAGroup import DNAGroup
from toontown.dna.DNAPacker import SHORT_STRING


class DNADoor(DNAGroup):
    COMPONENT_CODE = 17

    def __init__(self, name):
        DNAGroup.__init__(self, name)

        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def construct(self, storage, packer):
        DNAGroup.construct(self, storage, packer)

        self.setCode(packer.unpack(SHORT_STRING))
        self.setColor(packer.unpackColor())

        return False  # We can't have children.

    def traverse(self, storage, parent, recursive=True):
        frontNode = parent.find('**/*building*_front')
        if frontNode.isEmpty():
            frontNode = parent.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())

        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNADoor code %s could not be found.' % self.code)

        doorNodePath = node.copyTo(frontNode, 0)
        origin = parent.find('**/*door_origin')
        origin.node().setPreserveTransform(ModelNode.PTNet)
        self.setupDoor(doorNodePath, parent, origin, storage,
                       storage.getBlock(parent.getName()), self.color)

        return doorNodePath

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        doorNodePath.setColor(color, 0)

        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.setName('doorFrameHoleLeft')

        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.setName('doorFrameHoleRight')

        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.setName('leftDoor')

        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.setName('rightDoor')

        doorFlat = doorNodePath.find('door_*_flat')

        leftHole.wrtReparentTo(doorFlat, 0)
        rightHole.wrtReparentTo(doorFlat, 0)
        doorFlat.setEffect(DecalEffect.make())
        rightDoor.wrtReparentTo(parentNode, 0)
        leftDoor.wrtReparentTo(parentNode, 0)

        rightDoor.setColor(color, 0)
        leftDoor.setColor(color, 0)
        leftHole.setColor((0, 0, 0, 1), 0)
        rightHole.setColor((0, 0, 0, 1), 0)

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_' + block)
