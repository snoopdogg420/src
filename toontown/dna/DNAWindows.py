from panda3d.core import LVector4f, NodePath
from pandac.PandaModules import *
import DNAGroup
import DNAError
import DNAUtil

import random

class DNAWindows(DNAGroup.DNAGroup):
    COMPONENT_CODE = 11

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)
        self.windowCount = 0

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setWindowCount(self, windowCount):
        self.windowCount = windowCount

    def getWindowCount(self):
        return self.windowCount

    def makeWindow(self, x, y, parentNode, scale, dnaStorage, flip):
        code = self.code[:-1]
        if flip:
            code += 'l'
        else:
            code += 'r'
        node = dnaStorage.findNode(code)
        window = node.copyTo(parentNode, 0)
        window.setColor(self.color)
        window.setScale(NodePath(), scale)
        window.setHpr(0, 0, 0)
        window.setPos(x, 0, y)
        window.setPos(window, 0, -0.01, 0)

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)
        self.windowCount = dgi.getUint8()

    def traverse(self, nodePath, dnaStorage):
        if self.windowCount == 0:
            return
        parentX = nodePath.getParent().getScale().getX()
        scale = random.random() % 0.0375
        if parentX <= 5.0:
            scale += 1.0
        elif parentX <= 10.0:
            scale += 1.15
        else:
            scale += 1.3
        offset = lambda: random.random() % 0.0375
        if self.windowCount == 1:
            self.makeWindow(offset() + 0.5, offset() + 0.5, nodePath, scale,
                            dnaStorage, False)
        elif self.windowCount == 2:
            self.makeWindow(offset() + 0.33, offset() + 0.5, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset() + 0.66, offset() + 0.5, nodePath, scale,
                            dnaStorage, True)
        elif self.windowCount == 3:
            self.makeWindow(offset() + 0.33, offset() + 0.66, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset() + 0.66, offset() + 0.66, nodePath, scale,
                            dnaStorage, True)
            self.makeWindow(offset() + 0.5, offset() + 0.66, nodePath, scale,
                            dnaStorage, False)
        elif self.windowCount == 4:
            self.makeWindow(offset() + 0.33, offset() + 0.25, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset() + 0.66, offset() + 0.25, nodePath, scale,
                            dnaStorage, True)
            self.makeWindow(offset() + 0.33, offset() + 0.66, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset() + 0.66, offset() + 0.66, nodePath, scale,
                            dnaStorage, True)
        else:
            raise DNAError.DNAError('Invalid window count: %s' % (self.windowCount))