from direct.directnotify import DirectNotifyGlobal
import DistributedLawOfficeAI
from toontown.toonbase import ToontownGlobals
from direct.showbase import DirectObject

class LawbotOfficeManagerAI(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('LawbotOfficeManagerAI')
    officeId = None

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)
        self.air = air

    def getDoId(self):
        return 0

    def createOffice(self, officeId, entranceId, players):
        officeZone = self.air.allocateZone()
        if LawbotOfficeManagerAI.officeId is not None:
            officeId = LawbotOfficeManagerAI.officeId
        office = DistributedLawOfficeAI.DistributedLawOfficeAI(self.air, officeId, officeZone, entranceId, players)
        office.generateWithRequired(officeZone)
        return officeZone
