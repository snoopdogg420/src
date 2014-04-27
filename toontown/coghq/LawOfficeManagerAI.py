from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase import DirectObject
from toontown.coghq import DistributedLawOfficeAI


class LawOfficeManagerAI(DirectObject.DirectObject):
    notify = directNotify.newCategory('LawOfficeManagerAI')

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)
        self.air = air

    def getDoId(self):
        return 0

    def createLawOffice(self, lawOfficeId, players):
        lawOfficeZone = self.air.allocateZone()
        lawOffice = DistributedLawOfficeAI.DistributedLawOfficeAI(
            self.air, lawOfficeId, lawOfficeZone, players)
        lawOffice.generateWithRequired(lawOfficeZone)
        return lawOfficeZone
