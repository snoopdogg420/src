import DNAGroup
import DNAError
from DNAUtil import *

import random

class DNAWindows(DNAGroup.DNAGroup):
    COMPONENT_CODE = 11

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code - ''
        self.color = (1, 1, 1, 1)
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
        window = node.copyTo(parentNode)
        window.setColor(self.color)
        window.setScale(scale)
        window.setHpr(0, 0, 0)
        window.setPos(x, 0, y)

    def makeFromDGI(self, dgi, dnaStorage):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi, dnaStorage)
        self.code = dgiExtractString8(dgi)
        self.color = dgiExtractColor(dgi)
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
        offset = random.random() % 0.0375
        if self.windowCount == 1:
            self.makeWindow(offset + 0.5, offset + 0.5, nodePath, scale,
                            dnaStorage, False)
        elif self.windowCount == 2:
            self.makeWindow(offset + 0.33, offset + 0.5, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset + 0.66, offset + 0.5, nodePath, scale,
                            dnaStorage, True)
        elif self.windowCount == 3:
            self.makeWindow(offset + 0.33, offset + 0.66, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset + 0.66, offset + 0.66, nodePath, scale,
                            dnaStorage, True)
            self.makeWindow(offset + 0.5, offset + 0.66, nodePath, scale,
                            dnaStorage, False)
        elif self.windowCount == 4:
            self.makeWindow(offset + 0.33, offset + 0.25, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset + 0.66, offset + 0.25, nodePath, scale,
                            dnaStorage, True)
            self.makeWindow(offset + 0.33, offset + 0.66, nodePath, scale,
                            dnaStorage, False)
            self.makeWindow(offset + 0.66, offset + 0.66, nodePath, scale,
                            dnaStorage, True)
        else:
            raise DNAError.DNAError('Invalid window count: %s' % (self.windowCount))