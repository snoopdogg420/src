from toontown.dna.DNABattleCell import DNABattleCell
from toontown.dna.DNAGroup import DNAGroup
from toontown.dna.DNAPacker import UINT16, SHORT_STRING, UINT8


class DNAVisGroup(DNAGroup):
    COMPONENT_CODE = 2

    def __init__(self, name):
        DNAGroup.__init__(self, name)

        self.visibles = []
        self.suitEdges = []
        self.battleCells = []

    def getVisGroup(self):
        return self

    def getNumVisibles(self):
        return len(self.visibles)

    def addVisible(self, visible):
        self.visibles.append(visible)

    def removeVisible(self, visible):
        self.visibles.remove(visible)

    def getVisibleName(self, i):
        return self.visibles[i]

    def getNumSuitEdges(self):
        return len(self.suitEdges)

    def addSuitEdge(self, suitEdge):
        self.suitEdges.append(suitEdge)

    def removeSuitEdge(self, edge):
        self.suitEdges.remove(edge)

    def getSuitEdge(self, i):
        return self.suitEdges[i]

    def getNumBattleCells(self):
        return len(self.battleCells)

    def addBattleCell(self, battleCell):
        self.battleCells.append(battleCell)

    def removeBattleCell(self, cell):
        self.battleCells.remove(cell)

    def getBattleCell(self, i):
        return self.battleCells[i]

    def construct(self, storage, packer):
        DNAGroup.construct(self, storage, packer)

        edgeCount = packer.unpack(UINT16)
        for _ in xrange(edgeCount):
            startPointIndex = packer.unpack(UINT16)
            endPointIndex = packer.unpack(UINT16)
            edge = storage.getSuitEdge(startPointIndex, endPointIndex)
            self.addSuitEdge(edge)

        visibleCount = packer.unpack(UINT16)
        for _ in xrange(visibleCount):
            self.addVisible(packer.unpack(SHORT_STRING))

        battleCellCount = packer.unpack(UINT16)
        for _ in xrange(battleCellCount):
            width = packer.unpack(UINT8)
            height = packer.unpack(UINT8)
            pos = packer.unpackPosition()
            self.addBattleCell(DNABattleCell(width, height, pos))

        return True # We can have children.
