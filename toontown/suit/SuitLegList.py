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
        TFromCogHQ: 'FromCogHQ',
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
        elif self.getType() == SuitLeg.TFromSuitBuilding:
            return SuitTimings.fromSuitBuilding
        elif self.getType() == SuitLeg.TToSuitBuilding:
            return SuitTimings.toSuitBuilding
        elif self.getType() == SuitLeg.TToToonBuilding:
            return SuitTimings.toToonBuilding
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
        posA = self.getPosA()
        posB = self.getPosB()
        return posA + ((posB-posA) * (time/self.getLegTime()))

    def getType(self):
        return self.type

    @staticmethod
    def getTypeName(type):
        if type in SuitLeg.TypeToName:
            return SuitLeg.TypeToName[type]
        else:
            return '**invalid**'


class SuitLegList:
    def __init__(self, path, dnaStore, suitWalkSpeed, fromSky, toSky,
            fromSuitBuilding, toSuitBuilding, toToonBuilding):
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
        # TODO: What is blockNumber used for?
        startPoint = self.path.getPoint(0)
        startEdge = self.dnaStore.suitEdges[startPoint.getIndex()][0]
        zoneId = startEdge.getZoneId()
        startLeg = SuitLeg(
            self.getStartTime(0), zoneId, 0, startPoint, startPoint,
            SuitLeg.TFromSky)
        self.legs.append(startLeg)
        for i in range(self.path.getNumPoints()):
            if not 0 < i < (self.path.getNumPoints()-1):
                continue
            pointA = self.path.getPoint(i)
            pointB = self.path.getPoint(i + 1)
            zoneId = self.dnaStore.getSuitEdgeZone(
                pointA.getIndex(), pointB.getIndex())
            leg = SuitLeg(
                self.getStartTime(i), zoneId, 0, pointA, pointB, SuitLeg.TWalk)
            self.legs.append(leg)
        endIndex = self.path.getNumPoints() - 1
        endPoint = self.path.getPoint()
        endEdge = self.dnaStore.suitEdges[endIndex][0]
        zoneId = endEdge.getZoneId()
        endLeg = SuitLeg(
            self.getStartTime(endIndex), zoneId, 0, endPoint, endPoint,
            SuitLeg.TToSky)
        self.legs.append(endLeg)

    def getNumLegs(self):
        return len(self.legs)

    def getLeg(self, i):
        return self.legs[i]

    def getType(self, i):
        return self.legs[i].getType()

    def getLegTime(self, i):
        return self.legs[i].getLegTime()

    def getZoneId(self, i):
        return self.legs[i].getZoneId()

    def getBlockNumber(self, i):
        return self.legs[i].getBlockNumber()

    def getPointA(self, i):
        return self.legs[i].getPointA()

    def getPointB(self, i):
        return self.legs[i].getPointB()

    def getStartTime(self, i):
        # Accumulate the leg times until we find the leg time for this leg
        # index.
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
            endTime += self.getLegTime(i)
            i += 1
        while i < self.getNumLegs():
            endTime += self.getLegTime(i)
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
