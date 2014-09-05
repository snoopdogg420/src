import zlib

from toontown.dna import DNAAnimProp
from toontown.dna import DNABattleCell
from toontown.dna import DNACornice
from toontown.dna import DNADoor
from toontown.dna import DNAFlatBuilding
from toontown.dna import DNAFlatDoor
from toontown.dna import DNAGroup
from toontown.dna import DNAInteractiveProp
from toontown.dna import DNALandmarkBuilding
from toontown.dna import DNAProp
from toontown.dna import DNASign
from toontown.dna import DNASignBaseline
from toontown.dna import DNASignGraphic
from toontown.dna import DNASignText
from toontown.dna import DNAStreet
from toontown.dna import DNASuitPoint
from toontown.dna import DNAVisGroup
from toontown.dna import DNAWall
from toontown.dna import DNAWindows
from toontown.dna.DNAPacker import *


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
            suitPoint = DNASuitPoint.DNASuitPoint(
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
            cell = DNABattleCell.DNABattleCell(width, height, pos)
            self.storage.storeBattleCell(cell)

    def readComponent(self, ctor):
        component = ctor('')
        hasChildren = component.construct(self.dnaStore, self.packer)
        if self.topGroup is not None:
            self.topGroup.add(component)
            component.setParent(self.topGroup)
        if hasChildren:
            self.topGroup = component

    def readComponents(self):
        componentCode = self.packer.unpack(UINT8)
        if componentCode == DNAGroup.DNAGroup.COMPONENT_CODE:
            self.readComponent(DNAGroup.DNAGroup)
        elif componentCode == DNAVisGroup.DNAVisGroup.COMPONENT_CODE:
            self.readComponent(DNAVisGroup.DNAVisGroup)
        elif componentCode == DNAProp.DNAProp.COMPONENT_CODE:
            self.readComponent(DNAProp.DNAProp)
        elif componentCode == DNASign.DNASign.COMPONENT_CODE:
            self.readComponent(DNASign.DNASign)
        elif componentCode == DNASignBaseline.DNASignBaseline.COMPONENT_CODE:
            self.readComponent(DNASignBaseline.DNASignBaseline)
        elif componentCode == DNASignText.DNASignText.COMPONENT_CODE:
            self.readComponent(DNASignText.DNASignText)
        elif componentCode == DNASignGraphic.DNASignGraphic.COMPONENT_CODE:
            self.readComponent(DNASignGraphic.DNASignGraphic)
        elif componentCode == DNAFlatBuilding.DNAFlatBuilding.COMPONENT_CODE:
            self.readComponent(DNAFlatBuilding.DNAFlatBuilding)
        elif componentCode == DNAWall.DNAWall.COMPONENT_CODE:
            self.readComponent(DNAWall.DNAWall)
        elif componentCode == DNAWindows.DNAWindows.COMPONENT_CODE:
            self.readComponent(DNAWindows.DNAWindows)
        elif componentCode == DNACornice.DNACornice.COMPONENT_CODE:
            self.readComponent(DNACornice.DNACornice)
        elif componentCode == DNALandmarkBuilding.DNALandmarkBuilding.COMPONENT_CODE:
            self.readComponent(DNALandmarkBuilding.DNALandmarkBuilding)
        elif componentCode == DNAAnimProp.DNAAnimProp.COMPONENT_CODE:
            self.readComponent(DNAAnimProp.DNAAnimProp)
        elif componentCode == DNAInteractiveProp.DNAInteractiveProp.COMPONENT_CODE:
            self.readComponent(DNAInteractiveProp.DNAInteractiveProp)
        elif componentCode == DNADoor.DNADoor.COMPONENT_CODE:
            self.readComponent(DNADoor.DNADoor)
        elif componentCode == DNAFlatDoor.DNAFlatDoor.COMPONENT_CODE:
            self.readComponent(DNAFlatDoor.DNAFlatDoor)
        elif componentCode == DNAStreet.DNAStreet.COMPONENT_CODE:
            self.readComponent(DNAStreet.DNAStreet)
        else:
            self.topGroup = self.topGroup.getParent()
        if self.packer:
            self.readComponents()
