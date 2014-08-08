import DNAAnimProp
from DNAUtil import *

class DNAInteractiveProp(DNAAnimProp.DNAAnimProp):
    COMPONENT_CODE = 15

    def __init__(self, name):
        DNAAnimProp.DNAAnimProp.__init__(self, name)
        self.cellId = -1

    def setCellId(self, id):
        self.cellId = id

    def getCellId(self):
        return cellId

    def makeFromDGI(self, dgi):
        DNAAnimProp.DNAAnimProp.makeFromDGI(self, dgi)
        self.cellId = dgi.getInt16()

    def traverse(self, nodePath, dnaStorage):
        node = None
        if self.getCode() == "DCS":
            node = ModelNode(self.getName())
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node)
        else:
            node = dnaStorage.findNode(self.getCode())
            node = node.copyTo(nodePath)
            node.setName(self.getName())
        node.setTag('DNAAnim', self.getAnim())
        node.setTag('DNACellIndex', str(self.cellId))
        node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        node.setColorScale(self.getColor())
        for child in self.children:
            child.traverse(node, dnaStorage)