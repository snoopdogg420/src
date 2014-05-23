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

    def getZoneId(self):
        return self.zoneId

    def getStartTime(self):
        return self.startTime

    def getLegTime(self):
        return self.legTime

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
    def getTypeName(legType):
        if legType in SuitLeg.TypeToName:
            return SuitLeg.TypeToName[legType]
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
        startPoint = self.path.getPoint(0)
        startEdge = self.dnaStore.suitEdges[startPoint.getIndex()][0]
        zoneId = startEdge.getZoneId()
        startLeg = SuitLeg(
            self.getStartTime(0), zoneId, -1, startPoint, startPoint,
            SuitLeg.TFromSky)
        self.legs.append(startLeg)
        for i in xrange(self.path.getNumPoints()):
            if not 0 < i < (self.path.getNumPoints() - 1):
                continue
            pointA = self.path.getPoint(i)
            pointB = self.path.getPoint(i + 1)
            zoneId = self.dnaStore.getSuitEdgeZone(
                pointA.getIndex(), pointB.getIndex())
            leg = SuitLeg(
                self.getStartTime(i), zoneId, -1, pointA, pointB,
                SuitLeg.TWalk)
            self.legs.append(leg)
        endIndex = self.path.getNumPoints() - 1
        endPoint = self.path.getPoint(endIndex)
        endEdge = self.dnaStore.suitEdges[endPoint.getIndex()][0]
        zoneId = endEdge.getZoneId()
        endLeg = SuitLeg(
            self.getStartTime(endIndex), zoneId, -1, endPoint, endPoint,
            SuitLeg.TToSky)
        self.legs.append(endLeg)

    def getNumLegs(self):
        return len(self.legs)

    def getLeg(self, index):
        return self.legs[index]

    def getType(self, index):
        return self.legs[index].getType()

    def getLegTime(self, index):
        if self.getType(index) == SuitLeg.TFromSky:
            return self.fromSky
        if self.getType(index) == SuitLeg.TToSky:
            return self.toSky
        if self.getType(index) == SuitLeg.TFromSuitBuilding:
            return self.fromSuitBuilding
        if self.getType(index) == SuitLeg.TToSuitBuilding:
            return self.toSuitBuilding
        if self.getType(index) == SuitLeg.TToToonBuilding:
            return self.toToonBuilding
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
        if index < (self.getNumLegs() - 1):
            return self.legs[index].getStartTime()
        startTime = 0.0
        for legIndex in xrange(self.getNumLegs()):
            if legIndex == index:
                break
            startTime += self.getLegTime(legIndex)
        return startTime

    def getLegIndexAtTime(self, time, startLeg):
        endTime = 0.0
        for legIndex in xrange(self.getNumLegs()):
            endTime += self.getLegTime(legIndex)
            if endTime > time:
                break
        return legIndex

    def isPointInRange(self, point, lowTime, highTime):
        # Check if this point is in the provided time range:
        pointIndex = point.getIndex()
        startLegIndex = self.getLegIndexAtTime(lowTime, 0)
        endLegIndex = self.getLegIndexAtTime(highTime, pointIndex)
        for leg in self.legs[startLegIndex:endLegIndex + 1]:
            if leg.getPointA().getIndex() == pointIndex:
                return 1
            if leg.getPointB().getIndex() == pointIndex:
                return 1
        return 0

    def getFirstLegType(self):
        return self.getType(0)

    def getNextLegType(self, index):
        return self.getType(index + 1)

    def getLastLegType(self):
        return self.getType(self.getNumLegs() - 1)

    def __getitem__(self, key):
        return self.legs[key]
