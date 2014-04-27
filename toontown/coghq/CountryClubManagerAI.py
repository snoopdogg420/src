from direct.directnotify import DirectNotifyGlobal
import DistributedCountryClubAI
from toontown.toonbase import ToontownGlobals
from direct.showbase import DirectObject

class CountryClubManagerAI(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('LawbotOfficeManagerAI')
    officeId = None

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)
        self.air = air

    def getDoId(self):
        return 0

    def createGolfCourse(self, officeId, entranceId, players):
        officeZone = self.air.allocateZone()
        if LawbotOfficeManagerAI.officeId is not None:
            officeId = CountryClubManagerAI.officeId
        office = DistributedCountryClubAI.DistributedCountryClubAI(self.air, officeId, officeZone, entranceId, players)
        office.generateWithRequired(officeZone)
        return officeZone
