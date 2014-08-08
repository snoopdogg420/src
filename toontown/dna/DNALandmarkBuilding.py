import DNANode
from DNAUtil import *

class DNALandmarkBuilding(DNANode.DNANode):
    COMPONENT_CODE = 13

    def __init__(self, name):
        DNANode.DNANode.__init__(self, name)
        self.code = ''
        self.wallColor = LVector4f(1, 1, 1, 1)
        self.title = ''
        self.article = ''
        self.buildingType = ''
        self.door = None

    def setArticle(self, article):
        self.article = article

    def getArticle(self):
        return self.article

    def setBuildingType(self, buildingType):
        self.buildingType = buildingType

    def getBuildingType(self):
        return self.buildingType

    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code

    def setWallColor(self, color):
        self.wallColor = color

    def getWallColor(self):
        return self.wallColor

    def setupSuitBuildingOrigin(self, nodePathA, nodePathB):
        if (self.getName()[:2] == 'tb') and (self.getName()[3].isdigit()) and (self.getName().find(':') != -1):
            name = self.getName()
            name = 's' + name[1:]
            node = nodePathB.find('**/*suit_building_origin')
            if node.isEmpty():
                node = nodePathA.attachNewNode(name)
                node.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
            else:
                node.wrtReparentTo(nodePathA)
                node.setName(name)

    def makeFromDGI(self, dgi):
        DNANode.DNANode.makeFromDGI(self, dgi)
        self.code = dgiExtractString8(dgi)
        self.wallColor = dgiExtractColor(dgi)
        self.title = dgiExtractString8(dgi)
        self.article = dgiExtractString8(dgi)
        self.buildingType = dgiExtractString8(dgi)

    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError('DNALandmarkBuilding code ' + self.code + ' not found in DNAStorage')
        npA = nodePath
        nodePath = node.copyTo(nodePath)
        nodePath.setName(self.getName())
        nodePath.setPosHprScale(self.getPos(), self.getHpr(), self.getScale())
        self.setupSuitBuildingOrigin(npA, nodePath)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)
        nodePath.flattenStrong()