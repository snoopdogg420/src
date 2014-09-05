from panda3d.core import PandaNode

from toontown.dna.DNAPacker import *


class DNAGroup:
    COMPONENT_CODE = 1

    def __init__(self, name):
        self.name = name

        self.parent = None
        self.visGroup = None
        self.children = []

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setParent(self, parent):
        self.parent = parent
        self.visGroup = parent.getVisGroup()

    def getParent(self):
        return self.parent

    def clearParent(self):
        self.parent = None
        self.visGroup = None

    def getVisGroup(self):
        return self.visGroup

    def getNumChildren(self):
        return len(self.children)

    def add(self, child):
        self.children.append(child)

    def remove(self, child):
        self.children.remove(child)

    def at(self, i):
        return self.children[i]

    def construct(self, storage, packer):
        self.setName(packer.unpack(SHORT_STRING))

        return True  # We can have children.

    def traverse(self, storage, parent, recursive=True):
        nodePath = parent.attachNewNode(self.name)

        if recursive:
            self.traverseChilren(storage, parent)

        return nodePath

    def traverseChildren(self, storage, parent):
        for child in self.children:
            child.traverse(storage, parent)
