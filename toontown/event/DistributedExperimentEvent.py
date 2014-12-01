from pandac.PandaModules import Vec4
from toontown.event.DistributedEvent import DistributedEvent
from toontown.hood import ZoneUtil
from toontown.dna.DNAStorage import DNAStorage
from toontown.dna.DNAParser import loadDNAFileAI


class DistributedExperimentEvent(DistributedEvent):
    notify = directNotify.newCategory('DistributedExperimentEvent')

    def announceGenerate(self):
        DistributedEvent.announceGenerate(self)

        self.cr.playGame.hood.startSpookySky()
        render.setColorScale(Vec4(0.40, 0.40, 0.60, 1))
        aspect2d.setColorScale(Vec4(0.40, 0.40, 0.60, 1))

    def delete(self):
        DistributedEvent.delete(self)

        render.setColorScale(Vec4(1, 1, 1, 1))
        aspect2d.setColorScale(Vec4(1, 1, 1, 1))

    def setVisGroups(self, visGroups):
        self.cr.sendSetZoneMsg(self.zoneId, visGroups)
