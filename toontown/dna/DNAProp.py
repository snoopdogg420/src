from pandac.PandaModules import  LVector4f

from toontown.dna.DNANode import DNANode
from toontown.dna.DNAPacker import SHORT_STRING


class DNAProp(DNANode):
    COMPONENT_CODE = 4

    def __init__(self, name):
        DNANode.__init__(self, name)

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
        DNANode.construct(self, storage, packer)

        self.setCode(packer.unpack(SHORT_STRING))
        self.setColor(packer.unpackColor())

        return True  # We can have children.

    def traverse(self, storage, parent, recursive=True):
        nodePath = DNANode.traverse(storage, parent, recursive=False)

        node = storage.findNode(self.code)
        if node is not None:
            node.reparentTo(nodePath)

        nodePath.setName(self.name)
        nodePath.setColorScale(self.color, 0)

        if recursive:
            self.traverseChildren(storage, nodePath)
        return nodePath
