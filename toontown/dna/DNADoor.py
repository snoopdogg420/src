import DNAGroup
from DNAUtil import *

class DNADoor(DNAGroup.DNAGroup):
    COMPONENT_CODE = 17

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code = ''
        self.color = (1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        doorNodePath.setColor(color)
        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.setName('doorFrameHoleLeft')
        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.setName('doorFrameHoleRight')
        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.setName('leftDoor')
        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.setName('rightDoor')
        doorFlat = doorNodePath.find('door_*_flat')
        leftHole.wrtReparentTo(doorFlat)
        rightHole.wrtReparentTo(doorFlat)
        doorFlat.setEffect(DecalEffect.make())
        rightDoor.wrtReparentTo(parentNode)
        leftDoor.wrtReparentTo(parentNode)

        rightDoor.setColor(color)
        leftDoor.setColor(color)
        leftHole.setColor((0, 0, 0, 1))
        rightHole.setColor((0, 0, 0, 1))

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode)
        doorTrigger.setName('door_trigger_' + block)

        if not dnaStore.getDoorPosHprFromBlockNumber(block):
            store = NodePath('door-%s' % block)
            store.setPosHprScale(doorNodePath, (0, 0, 0), (0, 0, 0), (1, 1, 1))
            dnaStore.storeBlockDoor(block, store)

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)
        self.code = dgiExtractString8(dgi)
        self.color = dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        frontNode = nodePath.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNADoor code ' + self.code + ' not found in DNAStorage')
        doorNode = node.copyTo(frontNode)
        block = dnaStorage.getBlock(nodePath.getName())
        DNADoor.setupDoor(doorNode, nodePath, nodePath.find('**/*door_origin'), dnaStorage, block, self.color)
