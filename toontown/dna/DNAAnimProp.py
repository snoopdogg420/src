from toontown.dna.DNAPacker import SHORT_STRING
from toontown.dna.DNAProp import DNAProp


class DNAAnimProp(DNAProp):
    COMPONENT_CODE = 14

    def __init__(self, name):
        DNAProp.__init__(self, name)

        self.animName = ''

    def setAnimName(self, animName):
        self.animName = animName

    def getAnimName(self):
        return self.animName

    def construct(self, storage, packer):
        DNAProp.construct(self, storage, packer)

        self.setAnimName(packer.unpack(SHORT_STRING))

        return True  # We can have children.

    def traverse(self, storage, parent, recursive=True):
        nodePath = DNAProp.traverse(storage, parent, recursive=False)

        nodePath.setTag('DNAAnim', self.animName)

        if recursive:
            self.traverseChildren(storage, nodePath)
        return nodePath
