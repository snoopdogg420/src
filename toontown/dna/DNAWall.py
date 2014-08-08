import DNANode
import DNAFlatBuilding
from DNAUtil import *

class DNAWall(DNANode.DNANode):
    COMPONENT_CODE = 10

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.height = 10
        self.color = (1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setHeight(self, height):
        self.height = height

    def getHeight(self):
        return self.height

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = dgiExtractString8(dgi)
        self.height = dgi.getInt16() / 100.0
        self.color = dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNAWall code ' + self.code + ' not found in DNAStorage')
        node = node.copyTo(nodePath)
        pos = Point3(self.pos)
        pos.setZ(DNAFlatBuilding.DNAFlatBuilding.currentWallHeight)
        scale = Point3(self.scale)
        scale.setZ(self.height)
        node.setPosHprScale(pos, self.hpr, scale)
        node.setColor(self.color)
        for child in self.children:
            child.traverse(node, dnaStorage)
        DNAFlatBuilding.DNAFlatBuilding.currentWallHeight += self.height