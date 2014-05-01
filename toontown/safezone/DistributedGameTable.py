import math

from direct.fsm import ClassicFSM, State
from pandac.PandaModules import *
from direct.distributed import DistributedObject
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownTimer import ToontownTimer


class DistributedGameTable(DistributedObject.DistributedObject):
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.tableModelPath = 'phase_6/models/golf/game_table.bam'
        self.numSeats = 6
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedGameTable',
            [
                State.State(
                    'off', self.enterOff, self.exitOff,
                    ['chooseMode', 'observing']
                ),
                State.State(
                    'chooseMode', self.enterChooseMode, self.exitChooseMode,
                    ['sitting', 'off', 'observing']
                ),
                State.State(
                    'sitting', self.enterSitting, self.exitSitting,
                    ['off']
                ),
                State.State(
                    'observing', self.enterObserving, self.exitObserving,
                    ['off']
                )
            ], 'off', 'off')
        self.fsm.enterInitialState()

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

        self.picnicTableNode = render.attachNewNode('gameTable')
        self.picnicTable = loader.loadModel(self.tableModelPath)
        self.picnicTable.reparentTo(self.picnicTableNode)
        self.loader = self.cr.playGame.hood.loader
        self.picnicTableNode.reparentTo(self.loader.geom)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)

        self.tableCloth = self.picnicTable.find('**/basket_locator')
        cn = CollisionNode('tableCloth_sphere')
        self.tableClothSphereNode = self.tableCloth.attachNewNode(cn)
        cs = CollisionSphere(0, 0, -2, 5.5)
        self.tableClothSphereNode.node().addSolid(cs)

        self.seats = []
        self.jumpOffsets = []
        self.picnicTableSphereNodes = []
        for i in xrange(self.numSeats):
            self.seats.append(self.picnicTable.find('**/*seat' + str(i+1)))
            self.jumpOffsets.append(self.picnicTable.find('**/*jumpOut' + str(i+1)))
            cn = CollisionNode('picnicTable_sphere_{0}_{1}'.format(self.doId, i))
            self.picnicTableSphereNodes.append(self.seats[i].attachNewNode(cn))
            cs = CollisionSphere(0, 0, 0, 2)
            self.picnicTableSphereNodes[i].node().addSolid(cs)

        self.clockNode = ToontownTimer()
        self.clockNode.setPos(1.16, 0, -0.83)
        self.clockNode.setScale(0.3)
        self.clockNode.hide()

        self.buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        self.upButton = self.buttonModels.find('**//InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')

        angle = self.picnicTable.getH()
        angle -= 90
        radAngle = math.radians(angle)
        unitVec = Vec3(math.cos(radAngle), math.sin(radAngle), 0)
        unitVec *= 30.0
        self.endPos = self.picnicTable.getPos() + unitVec

        self.enableCollisions()

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        self.fsm.request('off')
        self.clearToonTracks()
        # TODO: Disable choice buttons.
        # TODO: Stop sleep tracking.
        self.destroyGameMenu()
        del self.gameMenu
        if self.cameraBoardTrack:
            self.cameraBoardTrack.finish()
        del self.cameraBoardTrack
        del self.tableClothSphereNode
        del self.tableCloth
        del self.seats
        del self.jumpOffsets
        del self.picnicTableSphereNodes
        del self.clockNode
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.endPos
        self.disableCollisions()
        del self.loader
        self.picnicTable.removeNode()
        self.picnicTableNode.removeNode()

    def delete(self):
        DistributedObject.DistributedObject.delete(self)

        del self.fsm

    def enableCollisions(self):
        for i in range(self.numSeats):
            event = 'enterpicnicTable_sphere_{0}_{1}'.format(self.doId, i)
            self.accept(event, self.handleEnterPicnicTableSphere, [i])
            self.picnicTableSphereNodes[i].setCollideMask(ToontownGlobals.WallBitmask)
        self.tableClothSphereNode.setCollideMask(ToontownGlobals.WallBitmask)

    def disableCollisions(self):
        for i in range(self.numSeats):
            self.ignore('enterpicnicTable_sphere_{0}_{1}'.format(self.doId, i))
            self.ignore('enterPicnicTableOK_{0}_{1}'.format(self.doId, i))
        for i in range(self.numSeats):
            self.picnicTableSphereNodes[i].setCollideMask(BitMask32(0))
        self.tableClothSphereNode.setCollideMask(BitMask32(0))

    def handleEnterPicnicTableSphere(self, i, collEntry):
        self.fsm.request('chooseMode')

    def enterOff(self):
        base.setCellsAvailable(base.leftCells + base.bottomCells, 0)

    def exitOff(self):
        base.setCellsAvailable(base.bottomCells, 0)

    def enterChooseMode(self):
        pass

    def exitChooseMode(self):
        pass

    def enterObserving(self):
        pass

    def exitObserving(self):
        pass

    def enterSitting(self):
        pass

    def exitSitting(self):
        self.destroyGameMenu()

    def destroyGameMenu(self):
        if self.gameMenu:
            self.gameMenu.removeButtons()
            self.gameMenu.picnicFunction = None
            self.gameMenu = None

    def setPosHpr(self, x, y, z, h, p, r):
        self.picnicTable.setPosHpr(x, y, z, h, p, r)