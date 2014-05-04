from toontown.toonbase import ToontownGlobals
import SuitTimings

class SuitLeg:
    TWalkFromStreet = 0
    TWalkToStreet = 1
    TWalk = 2
    TFromSky = 3
    TToSky = 4
    TFromSuitBuilding = 5
    TToSuitBuilding = 6
    TToToonBuilding = 7
    TFromCogHQ = 8
    TToCogHQ = 9
    TOff = 10
    TypeToName = {
        TWalkFromStreet: 'WalkFromStreet',
        TWalkToStreet: 'WalkToStreet',
        TWalk: 'Walk',
        TFromSky: 'FromSky',
        TToSky: 'ToSky',
        TFromSuitBuilding: 'FromSuitBuilding',
        TToSuitBuilding: 'ToSuitBuilding',
        TToToonBuilding: 'ToToonBuilding',
        TToToonBuilding: 'FromCogHQ',
        TToCogHQ: 'ToCogHQ',
        TOff: 'Off'
    }

    def __init__(self, startTime, zoneId, blockNumber, pointA, pointB, type):
        self.startTime = startTime
        self.zoneId = zoneId
        self.blockNumber = blockNumber
        self.pointA = pointA
        self.pointB = pointB
        self.type = type

    def getZoneId(self):
        return self.zoneId

    def getStartTime(self):
        return self.startTime

    def getLegTime(self):
        if self.getType() == SuitLeg.TFromSky:
            return SuitTimings.fromSky
        elif self.getType() == SuitLeg.TToSky:
            return SuitTimings.toSky
        else:
            return (self.getPosA()-self.getPosB()).length() / ToontownGlobals.SuitWalkSpeed

    def getBlockNumber(self):
        return self.blockNumber

    def getPointA(self):
        return self.pointA

    def getPointB(self):
        return self.pointB

    def getPosA(self):
        return self.pointA.getPos()

    def getPosB(self):
        return self.pointB.getPos()

    def getPosAtTime(self, time):
        pos = self.getPosB() - self.getPosA()
        return self.getPosA() + (pos*(time/self.getLegTime()))

    def getType(self):
        return self.type

    @staticmethod
    def getTypeName(type):
        if type in SuitLeg.TypeToName:
            return SuitLeg.TypeToName[type]
        else:
            return '**invalid**'


class SuitLegList:
    def __init__(self, path, dnaStore, suitWalkSpeed, fromSky, toSky, fromSuitBuilding, toSuitBuilding, toToonBuilding):
        self.path = path
        self.dnaStore = dnaStore
        self.suitWalkSpeed = suitWalkSpeed
        self.fromSky = fromSky
        self.toSky = toSky
        self.fromSuitBuilding = fromSuitBuilding
        self.toSuitBuilding = toSuitBuilding
        self.toToonBuilding = toToonBuilding
        self.legs = []
        # startTime, zoneId, blockNumber, pointA, pointB, type
        # TODO: Use suit edges to get zoneId
        startPoint = path.getPoint(0)
        self.legs.append(SuitLeg(0, 0, 0, startPoint, startPoint, SuitLeg.TFromSky))
        for i in range(path.getNumPoints()):
            if not 0 < i < (path.getNumPoints()-1):
                continue
            pointA = path.getPoint(i)
            pointB = path.getPoint(i + 1)
            self.legs.append(SuitLeg(0, 0, 0, pointA, pointB, SuitLeg.TWalk))
        endPoint = path.getPoint(path.getNumPoints() - 1)
        self.legs.append(SuitLeg(0, 0, 0, endPoint, endPoint, SuitLeg.TToSky))

    def getNumLegs(self):
        return len(self.legs)

    def getLeg(self, i):
        if i < self.getNumLegs():
            return self.legs[i]

    def getType(self, i):
        if i < self.getNumLegs():
            return self.legs[i].getType()

    def getLegTime(self, i):
        if i < self.getNumLegs():
            return self.legs[i].getLegTime()

    def getZoneId(self, i):
        if i < self.getNumLegs():
            return self.legs[i].getZoneId()

    def getBlockNumber(self, i):
        if i < self.getNumLegs():
            return self.legs[i].getBlockNumber()

    def getPointA(self, i):
        if i < self.getNumLegs():
            return self.legs[i].getPointA()

    def getPointB(self, i):
        if i < self.getNumLegs():
            return self.legs[i].getPointB()

    def getStartTime(self, i):
        time = 0
        legIndex = 0
        while (legIndex < self.getNumLegs()) and (legIndex < i):
            time += self.getLegTime(legIndex)
            legIndex += 1
        return time

    def getLegIndexAtTime(self, time, startLeg):
        endTime = 0
        i = 0
        while i < startLeg:
            try:
                endTime += self.getLegTime(i)
            except:
                pass
            i += 1
        while i < self.getNumLegs():
            try:
                endTime += self.getLegTime(i)
            except:
                pass
            if endTime > time:
                return i
            i += 1
        return self.getNumLegs() - 1

    def isPointInRange(self, point, lo, hi):
        pointIndex = point.getIndex()
        if self.getLegIndexAtTime(lo, 0) > self.getLegIndexAtTime(hi, pointIndex):
            return 0
        return 1

    def getFirstLegType(self):
        return self.getType(0)

    def getLastLegType(self):
        return self.getType(self.getNumLegs() - 1)

    def __getitem__(self, key):
        return self.legs[key]
