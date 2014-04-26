from direct.directnotify import DirectNotifyGlobal
from toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI

class DistributedCogKartAI(DistributedElevatorExtAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogKartAI")

    def __init__(self, air):
        DistributedElevatorExtAI.__init__(self, air)

        self.pos = (0, 0, 0)
        self.hpr = (0, 0, 0)

    def setCountryClubId(self, countryClubId):
        self.countryClubId = countryClub

    def getCountryClubId(self):
        return self.countryClubId

    def setPosHpr(self, x, y, z, h, p, r):
        self.pos = (x, y, z)
        self.hpr = (h, p, r)

    def getPosHpr(self):
        return self.pos + self.hpr

    def setCountryClubInteriorZone(self, zoneId):
        self.countryClubInteriorZone = zoneId

    def getCountryClubInteriorZone(self):
        return self.countryClubInteriorZone

    def setCountryClubInteriorZoneForce(self, zoneId):
        self.countryClubInteriorZoneForce = zoneId

    def getCountryClubInteriorZoneForce(self):
        return self.countryClubInteriorZoneForce
