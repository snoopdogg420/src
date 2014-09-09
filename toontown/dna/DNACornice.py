from pandac.PandaModules import  LVector4f, DecalEffect

from toontown.dna.DNAGroup import DNAGroup
from toontown.dna.DNAPacker import SHORT_STRING


class DNACornice(DNAGroup):
    COMPONENT_CODE = 12

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
        nodePath = DNAGroup.traverse(storage, parent, recursive=False)

        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNACornice code %d could not be found.' % self.code)

        scale = parent.getParent().getSx() / parent.getSz()

        _d = node.find('**/*_d').copyTo(nodePath, 0)
        _d.setScale(1, scale, scale)
        _d.setEffect(DecalEffect.make())

        _nd = node.find('**/*_nd').copyTo(nodePath, 1)
        _nd.setScale(1, scale, scale)

        nodePath.setZ(parent.getSz())
        nodePath.setColor(self.color)

        return nodePath
