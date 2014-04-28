import random

from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.coghq import CountryClubLayout
from toontown.coghq.BattleExperienceAggregatorAI import BattleExperienceAggregatorAI
from toontown.coghq.DistributedCountryClubRoomAI import DistributedCountryClubRoomAI
from toontown.toonbase import ToontownGlobals


class DistributedCountryClubAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedCountryClubAI')

    def __init__(self, air, countryClubId, zoneId, floorNum, avIds):
        DistributedObjectAI.__init__(self, air)

        self.countryClubId = countryClubId
        self.zoneId = zoneId
        self.floorNum = floorNum
        self.avIds = avIds
        if self.countryClubId == ToontownGlobals.BossbotCountryClubIntA:
            layouts = CountryClubLayout.countryClubLayouts[0:3]
        elif self.countryClubId == ToontownGlobals.BossbotCountryClubIntB:
            layouts = CountryClubLayout.countryClubLayouts[3:6]
        else:
            layouts = CountryClubLayout.countryClubLayouts[6:9]
        layout = random.choice(layouts)
        self.layoutIndex = CountryClubLayout.countryClubLayouts.index(layout)

    def generate(self):
        DistributedObjectAI.generate(self)
        self.layout = CountryClubLayout.CountryClubLayout(
            self.countryClubId, self.floorNum, self.layoutIndex)

        self.battleExpAggreg = BattleExperienceAggregatorAI()

        self.rooms = []
        for i in range(self.layout.getNumRooms()):
            room = DistributedCountryClubRoomAI(
                self.air, self.countryClubId, self.doId, self.zoneId,
                self.layout.getRoomId(i), i * 2, self.avIds,
                self.battleExpAggreg)
            room.generateWithRequired(self.zoneId)
            self.rooms.append(room)

        self.roomDoIds = []
        for room in self.rooms:
            self.roomDoIds.append(room.doId)
        self.sendUpdate('setRoomDoIds', [self.roomDoIds])

    def delete(self):
        del self.rooms
        del self.roomDoIds
        del self.layout
        del self.battleExpAggreg
        DistributedObjectAI.delete(self)

    def requestDelete(self):
        for room in self.rooms:
            self.roomDoIds.remove(room.doId)
            room.requestDelete()
        DistributedObjectAI.requestDelete(self)

    def allToonsGone(self):
        self.requestDelete()

    def getZoneId(self):
        return self.zoneId

    def getCountryClubId(self):
        return self.countryClubId

    def getFloorNum(self):
        return self.floorNum

    def getLayoutIndex(self):
        return self.layoutIndex

    def getBlockedRooms(self):
        return []

    def setCountryClubZone(self, todo0):
        pass

    def elevatorAlert(self, todo0):
        pass
