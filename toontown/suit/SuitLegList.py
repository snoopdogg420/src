from toontown.dna.DNAParser import DNASuitPoint
from toontown.suit import SuitTimings
from toontown.toonbase import ToontownGlobals


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

        distance = (self.getPosB() - self.getPosA()).length()
        self.legTime = distance / ToontownGlobals.SuitWalkSpeed
        self.endTime = self.startTime + self.legTime

    def getZoneId(self):
        return self.zoneId

    def getStartTime(self):
        return self.startTime

    def getLegTime(self):
        if self.getType() == SuitLeg.TWalk:  # Most common.
            return self.legTime
        if self.getType() == SuitLeg.TFromSky:
            return SuitTimings.fromSky
        if self.getType() == SuitLeg.TToSky:
            return SuitTimings.toSky
        if self.getType() == SuitLeg.TToToonBuilding:
            return SuitTimings.toToonBuilding
        return self.legTime

    def getEndTime(self):
        return self.endTime

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

    def getTypeName(self):
        if self.type in SuitLeg.TypeToName:
            return SuitLeg.TypeToName[self.type]
        return '**invalid**'


class SuitLegList:
    def __init__(self, path, dnaStore):
        self.path = path
        self.dnaStore = dnaStore

        self.legs = []

        # First, add the initial SuitLeg:
        self.add(self.path.getPoint(0), self.path.getPoint(1), self.getFirstLegType())

        # Next, connect each of the points in our path through SuitLegs:
        for i in xrange(self.path.getNumPoints() - 1):
            pointA = self.path.getPoint(i)
            pointB = self.path.getPoint(i + 1)
            legType = self.getLegType(
                pointA.getPointType(), pointB.getPointType())
            self.add(pointA, pointB, legType)

        # Finally, add the last SuitLeg:
        endPoint = self.path.getPoint(self.path.getNumPoints() - 1)
        self.add(endPoint, endPoint, SuitLeg.TToSky)

    def add(self, pointA, pointB, legType):
        if pointA != pointB:  # The last SuitLeg will have identical points.
            zoneId = self.dnaStore.getSuitEdgeZone(pointA.getIndex(), pointB.getIndex())
        else:
            zoneId = self.dnaStore.suitEdges[pointA.getIndex()][0].getZoneId()
        landmarkBuildingIndex = pointA.getLandmarkBuildingIndex()
        startTime = 0.0
        if len(self.legs) > 0:
            startTime = self.legs[-1].getEndTime()
        leg = SuitLeg(startTime, zoneId, landmarkBuildingIndex, pointA, pointB, legType)
        self.legs.append(leg)

    def getFirstLegType(self):
        pointTypeA = self.path.getPoint(0).getPointType()
        if pointTypeA == DNASuitPoint.STREET_POINT:
            return SuitLeg.TFromSky
        else:
            return SuitLeg.TWalk

    def getLegType(self, pointTypeA, pointTypeB):
        if pointTypeA == DNASuitPoint.STREET_POINT:  # Most common.
            return SuitLeg.TWalk
        if pointTypeA == DNASuitPoint.FRONT_DOOR_POINT:
            return SuitLeg.TToToonBuilding
        if pointTypeA == DNASuitPoint.COGHQ_IN_POINT:
            return SuitLeg.TToCogHQ
        if pointTypeA == DNASuitPoint.COGHQ_OUT_POINT:
            return SuitLeg.TFromCogHQ
        return SuitLeg.TWalk

    def getNumLegs(self):
        return len(self.legs)

    def getLeg(self, index):
        return self.legs[index]

    def getType(self, index):
        return self.legs[index].getType()

    def getLegTime(self, index):
        return self.legs[index].getLegTime()

    def getZoneId(self, index):
        return self.legs[index].getZoneId()

    def getBlockNumber(self, index):
        return self.legs[index].getBlockNumber()

    def getPointA(self, index):
        return self.legs[index].getPointA()

    def getPointB(self, index):
        return self.legs[index].getPointB()

    def getStartTime(self, index):
        return self.legs[index].getStartTime()

    def getLegIndexAtTime(self, time, startLeg):
        for i, leg in enumerate(self.legs):
            if leg.getEndTime() > time:
                break
        return i

    def isPointInRange(self, point, lowTime, highTime):
        legIndex = self.getLegIndexAtTime(lowTime, 0)
        while legIndex < self.getNumLegs():
            leg = self.legs[legIndex]
            if leg.getEndTime() > highTime:
                break
            if (leg.pointA == point) or (leg.pointB == point):
                return True
            legIndex += 1
        return False
