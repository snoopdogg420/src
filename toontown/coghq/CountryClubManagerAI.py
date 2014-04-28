from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase import DirectObject
from toontown.coghq.DistributedCountryClubAI import DistributedCountryClubAI


class CountryClubManagerAI(DirectObject.DirectObject):
    notify = directNotify.newCategory('CountryClubManagerAI')

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)

        self.air = air

    def getDoId(self):
        return 0

    def createCountryClub(self, countryClubId, players):
        countryClubZone = self.air.allocateZone()
        countryClub = DistributedCountryClubAI(
            self.air, countryClubId, countryClubZone, 0, players)
        countryClub.generateWithRequired(countryClubZone)
        return countryClubZone
