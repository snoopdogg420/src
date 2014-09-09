import zlib

from toontown.dna.DNAAnimProp import DNAAnimProp
from toontown.dna.DNABattleCell import DNABattleCell
from toontown.dna.DNACornice import DNACornice
from toontown.dna.DNADoor import DNADoor
from toontown.dna.DNAFlatBuilding import DNAFlatBuilding
from toontown.dna.DNAFlatDoor import DNAFlatDoor
from toontown.dna.DNAGroup import DNAGroup
from toontown.dna.DNAInteractiveProp import DNAInteractiveProp
from toontown.dna.DNALandmarkBuilding import DNALandmarkBuilding
from toontown.dna.DNAPacker import DNAPacker, UINT16, SHORT_STRING, UINT8, INT8
from toontown.dna.DNAProp import DNAProp
from toontown.dna.DNASign import DNASign
from toontown.dna.DNASignBaseline import DNASignBaseline
from toontown.dna.DNASignGraphic import DNASignGraphic
from toontown.dna.DNASignText import DNASignText
from toontown.dna.DNAStreet import DNAStreet
from toontown.dna.DNASuitPoint import DNASuitPoint
from toontown.dna.DNAVisGroup import DNAVisGroup
from toontown.dna.DNAWall import DNAWall
from toontown.dna.DNAWindows import DNAWindows


class DNAError(Exception):
    pass


# We'll want to access DNAError in other parts of the application:
__builtins__['DNAError'] = DNAError


class DNALoader:
    def __init__(self):
        self.storage = None
        self.packer = DNAPacker()
        self.topGroup = None

    def destroy(self):
        self.storage = None
        self.packer = None
        self.topGroup = None

    def getStorage(self):
        return self.storage

    def getPacker(self):
        return self.packer

    def getTopGroup(self):
        return self.topGroup

    def load(self, storage, filepath):
        self.storage = storage

        # Load the PDNA file and parse the header:
        with open(filepath, 'rb') as f:
            data = f.read()
            if not data.startswith('PDNA\n'):
                raise DNAError('Invalid libpandadna header.')
            data = data[5:]

            # Is this PDNA file compressed? If it is, decompress it using ZLib:
            compressed = int(ord(data[0]))
            data = data[2:]
            if compressed:
                zlib.decompress(data)

        # Add the data to the DNAPacker:
        self.packer += data

        # Construct the storage and components:
        self.readStorage()
        self.readComponents()

    def readStorage(self):
        if self.storage is None:
            raise DNAError('Tried to read storage before one was present.')

        # Catalog codes...
        rootCount = self.packer.unpack(UINT16)
        for _ in xrange(rootCount):
            root = self.packer.unpack(SHORT_STRING)
            codeCount = self.packer.unpack(UINT8)
            for _ in xrange(codeCount):
                code = self.packer.unpack(SHORT_STRING)
                self.storage.storeCatalogCode(root, code)

        # Textures...
        textureCount = self.packer.unpack(UINT16)
        for _ in xrange(textureCount):
            code = self.packer.unpack(SHORT_STRING)
            filename = self.packer.unpack(SHORT_STRING)
            self.storage.storeTexture(code, filename)

        # Fonts...
        fontCount = self.packer.unpack(UINT16)
        for _ in xrange(fontCount):
            code = self.packer.unpack(SHORT_STRING)
            filename = self.packer.unpack(SHORT_STRING)
            self.storage.storeFont(code, filename)

        # Nodes...
        nodeCount = self.packer.unpack(UINT16)
        for _ in xrange(nodeCount):
            code = self.packer.unpack(SHORT_STRING)
            filename = self.packer.unpack(SHORT_STRING)
            search = self.packer.unpack(SHORT_STRING)
            self.storage.storeNode(code, filename, search)

        # Blocks...
        blockNumberCount = self.packer.unpack(UINT16)
        for _ in xrange(blockNumberCount):
            number = self.packer.unpack(UINT8)
            zoneId = self.packer.unpack(UINT16)
            title = self.packer.unpack(SHORT_STRING)
            article = self.packer.unpack(SHORT_STRING)
            buildingType = self.packer.unpack(SHORT_STRING)
            self.storage.storeBlockNumber(number)
            self.storage.storeBlockZone(number, zoneId)
            if title:
                self.storage.storeBlockTitle(number, title)
            if article:
                self.storage.storeBlockArticle(number, article)
            if buildingType:
                self.storage.storeBlockBuildingType(number, buildingType)

        # Suit points...
        suitPointCount = self.packer.unpack(UINT16)
        for _ in xrange(suitPointCount):
            index = self.packer.unpack(UINT16)
            pointType = self.packer.unpack(UINT8)
            pos = self.packer.unpackPosition()
            landmarkBuildingIndex = self.packer.unpack(INT8)
            suitPoint = DNASuitPoint(
                index, pointType, pos,
                landmarkBuildingIndex=landmarkBuildingIndex)
            self.storage.storeSuitPoint(suitPoint)

        # Suit edges...
        suitEdgeCount = self.packer.unpack(UINT16)
        for _ in xrange(suitEdgeCount):
            startPointIndex = self.packer.unpack(UINT16)
            edgeCount = self.packer.unpack(UINT16)
            for _ in xrange(edgeCount):
                endPointIndex = self.packer.unpack(UINT16)
                zoneId = self.packer.unpack(UINT16)
                self.storage.storeSuitEdge(startPointIndex, endPointIndex, zoneId)

        # Battle cells...
        battleCellCount = self.packer.unpack(UINT16)
        for _ in xrange(battleCellCount):
            width = self.packer.unpack(UINT8)
            height = self.packer.unpack(UINT8)
            pos = self.packer.unpackPosition()
            cell = DNABattleCell(width, height, pos)
            self.storage.storeBattleCell(cell)

    def readComponent(self, ctor):
        component = ctor('')
        hasChildren = component.construct(self.storage, self.packer)
        if self.topGroup is not None:
            self.topGroup.add(component)
            component.setParent(self.topGroup)
        if hasChildren:
            self.topGroup = component

    def readComponents(self):
        componentCode = self.packer.unpack(UINT8)
        if componentCode == DNAGroup.COMPONENT_CODE:
            self.readComponent(DNAGroup)
        elif componentCode == DNAVisGroup.COMPONENT_CODE:
            self.readComponent(DNAVisGroup)
        elif componentCode == DNAProp.COMPONENT_CODE:
            self.readComponent(DNAProp)
        elif componentCode == DNASign.COMPONENT_CODE:
            self.readComponent(DNASign)
        elif componentCode == DNASignBaseline.COMPONENT_CODE:
            self.readComponent(DNASignBaseline)
        elif componentCode == DNASignText.COMPONENT_CODE:
            self.readComponent(DNASignText)
        elif componentCode == DNASignGraphic.COMPONENT_CODE:
            self.readComponent(DNASignGraphic)
        elif componentCode == DNAFlatBuilding.COMPONENT_CODE:
            self.readComponent(DNAFlatBuilding)
        elif componentCode == DNAWall.COMPONENT_CODE:
            self.readComponent(DNAWall)
        elif componentCode == DNAWindows.COMPONENT_CODE:
            self.readComponent(DNAWindows)
        elif componentCode == DNACornice.COMPONENT_CODE:
            self.readComponent(DNACornice)
        elif componentCode == DNALandmarkBuilding.COMPONENT_CODE:
            self.readComponent(DNALandmarkBuilding)
        elif componentCode == DNAAnimProp.COMPONENT_CODE:
            self.readComponent(DNAAnimProp)
        elif componentCode == DNAInteractiveProp.COMPONENT_CODE:
            self.readComponent(DNAInteractiveProp)
        elif componentCode == DNADoor.COMPONENT_CODE:
            self.readComponent(DNADoor)
        elif componentCode == DNAFlatDoor.COMPONENT_CODE:
            self.readComponent(DNAFlatDoor)
        elif componentCode == DNAStreet.COMPONENT_CODE:
            self.readComponent(DNAStreet)
        else:
            self.topGroup = self.topGroup.getParent()
        if self.packer:
            self.readComponents()
