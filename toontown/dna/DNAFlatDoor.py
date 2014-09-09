from pandac.PandaModules import NodePath, DecalEffect

from toontown.dna.DNADoor import DNADoor


class DNAFlatDoor(DNADoor):
    COMPONENT_CODE = 18

    def traverse(self, storage, parent, recursive=True):
        node = storage.findNode(self.code)
        if node is None:
            raise DNAError('DNAFlatDoor code %s could not be found.' % self.code)

        nodePath = node.copyTo(parent, 0)
        nodePath.setScale(NodePath(), 1)
        nodePath.setX(0.5)
        nodePath.setColor(self.color)
        nodePath.getNode(0).setEffect(DecalEffect.make())
