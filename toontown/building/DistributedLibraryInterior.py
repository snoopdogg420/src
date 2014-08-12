from direct.distributed.DistributedObject import DistributedObject

from toontown.building import  ToonInteriorColors
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase


class DistributedLibraryInterior(DistributedObject):
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        self.interior = loader.loadModel('phase_4/models/modules/ttc_bank_interior.bam')
        self.interior.reparentTo(render)

        doorOrigin = self.interior.find('**/door_origin;+s')
        doorOrigin.setScale(0.8)
        doorOrigin.setY(doorOrigin, -0.025)

        door = self.cr.playGame.dnaStore.findNode('door_double_round_ur')
        doorNodePath = door.copyTo(doorOrigin)

        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        doorColor = ToonInteriorColors.colors[hoodId]['TI_door'][0]
        DNADoor.setupDoor(
            doorNodePath, self.interior, doorOrigin, self.cr.playGame.dnaStore,
            str(self.block), doorColor)

        doorFrame = doorNodePath.find('door_double_round_ur_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)

        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()


    def disable(self):
        self.interior.removeNode()
        del self.interior

        DistributedObject.disable(self)

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block
