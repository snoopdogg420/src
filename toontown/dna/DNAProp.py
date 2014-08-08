import DNANode
from DNAUtil import *

class DNAProp(DNANode.DNANode):
    COMPONENT_CODE = 4

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.color = (1, 1, 1, 1)

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = dgiExtractString8(dgi)
        self.color = dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        if self.code == 'DCS':
            node = ModelNode(self.name)
            node.setPreserveTransform(ModelNode.PTNet)
            node = nodePath.attachNewNode(node)
        else:
            node = dnaStorage.findNode(self.code)
            if node is None:
                return
            node = node.copyTo(nodePath)
        node.setPos(self.pos)
        node.setHpr(self.hpr)
        node.setScale(self.scale)
        node.setName(self.name)
        node.setColorScale(self.color)
        for child in self.children:
            child.traverse(node, dnaStorage)