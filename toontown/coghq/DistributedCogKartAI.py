from direct.directnotify.DirectNotifyGlobal import *
from toontown.building.DistributedElevatorAI import DistributedElevatorAI
from toontown.building.DistributedElevatorExtAI import DistributedElevatorExtAI
from toontown.safezone.TrolleyConstants import *
from toontown.coghq import CountryClubManagerAI


class DistributedCogKartAI(DistributedElevatorExtAI):
    notify = directNotify.newCategory('DistributedCogKartAI')

    def __init__(self, air):
        DistributedElevatorExtAI.__init__(self, air, air.countryClubMgr)
        self.pos = (0, 0, 0)
        self.hpr = (0, 0, 0)
        self.countryClubInteriorZone = 0
        self.countryClubId = 0
        self.countryClubInteriorZoneForce = 0

    def setCountryClubId(self, countryClubId):
        self.countryClubId = countryClubId

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

    def enterClosing(self):
        DistributedElevatorAI.enterClosing(self)
        taskMgr.doMethodLater(TROLLEY_EXIT_TIME, self.elevatorClosedTask,
                              self.uniqueName('closing-timer'))

    def enterClosed(self):
        self.d_setState('closed')
        self.fsm.request('opening')

    def elevatorClosed(self):
        numPlayers = self.countFullSeats()
        if numPlayers > 0:
            players = []
            for i in self.seats:
                if i not in [None, 0]:
                    players.append(i)
            countryClubZone = self.bldg.createCountryClub(self.countryClubId, players)
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    self.sendUpdateToAvatarId(avId, 'setCountryClubInteriorZone', [countryClubZone])
                    self.clearFullNow(seatIndex)
        self.fsm.request('closed')
