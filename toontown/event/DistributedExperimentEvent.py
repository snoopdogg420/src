from pandac.PandaModules import Vec4
from toontown.event.DistributedEvent import DistributedEvent
from toontown.dna.DNAStorage import DNAStorage
from toontown.dna.DNAParser import loadDNAFileAI
from toontown.hood import ZoneUtil
from toontown.town.TownBattle import TownBattle
from direct.fsm import ClassicFSM, State


class DistributedExperimentEvent(DistributedEvent):
    notify = directNotify.newCategory('DistributedExperimentEvent')

    def announceGenerate(self):
        self.cr.event = self

        dnaStore = DNAStorage()
        dnaFileName = ZoneUtil.genDNAFileName(self.zoneId)
        loadDNAFileAI(dnaStore, dnaFileName)

        zoneVisDict = {}
        for i in xrange(dnaStore.getNumDNAVisGroupsAI()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            visGroup = dnaStore.getDNAVisGroupAI(i)
            visZoneId = int(base.cr.hoodMgr.extractGroupName(groupFullName))
            visZoneId = ZoneUtil.getTrueZoneId(visZoneId, self.zoneId)
            visibles = []
            for i in xrange(visGroup.getNumVisibles()):
                visibles.append(int(visGroup.visibles[i]))
            visibles.append(ZoneUtil.getBranchZone(visZoneId))

        self.cr.playGame.hood.startSpookySky()
        render.setColorScale(Vec4(0.40, 0.40, 0.60, 1))
        aspect2d.setColorScale(Vec4(0.40, 0.40, 0.60, 1))

    def delete(self):
        render.setColorScale(Vec4(1, 1, 1, 1))
        aspect2d.setColorScale(Vec4(1, 1, 1, 1))
