from toontown.dna.DNALandmarkBuilding import DNALandmarkBuilding
from toontown.dna.DNAPacker import SHORT_STRING


class DNAAnimBuilding(DNALandmarkBuilding):
    COMPONENT_CODE = 16

    def __init__(self, name):
        DNALandmarkBuilding.__init__(self, name)

        self.animName = ''

    def setAnimName(self, animName):
        self.animName = animName

    def getAnimName(self):
        return self.animName

    def construct(self, storage, packer):
        DNALandmarkBuilding.construct(self, storage, packer)

        self.setAnimName(packer.unpack(SHORT_STRING))

        return True  # We can have children.

    def traverse(self, storage, parent, recursive=True):
        nodePath = DNALandmarkBuilding.traverse(storage, parent, recursive=False)

        nodePath.setTag('DNAAnim', self.animName)

        if recursive:
            self.traverseChildren(storage, nodePath)
        return nodePath
