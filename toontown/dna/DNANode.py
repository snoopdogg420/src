from pandac.PandaModules import LVector3f

from toontown.dna.DNAGroup import DNAGroup


class DNANode(DNAGroup):
    COMPONENT_CODE = 3

    def __init__(self, name):
        DNAGroup.__init__(self, name)

        self.pos = LVector3f(0, 0, 0)
        self.hpr = LVector3f(0, 0, 0)
        self.scale = LVector3f(1, 1, 1)

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def getHpr(self):
        return self.hpr

    def setHpr(self, hpr):
        self.hpr = hpr

    def getScale(self):
        return self.scale

    def setScale(self, scale):
        self.scale = scale

    def construct(self, storage, packer):
        DNAGroup.construct(self, storage, packer)

        self.setPos(packer.unpackPosition())
        self.setHpr(packer.unpackRotation())
        self.setScale(packer.unpackScale())

        return True  # We can have children.

    def traverse(self, storage, parent, recursive=True):
        nodePath = DNANode.traverse(storage, parent, recursive=False)

        nodePath.setPosHprScale(self.pos, self.hpr, self.scale)

        if recursive:
            self.traverseChildren(storage, nodePath)
        return nodePath
