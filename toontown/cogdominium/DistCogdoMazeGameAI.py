from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
from toontown.cogdominium import CogdoMazeGameGlobals
import random


class DistCogdoMazeGameAI(DistCogdoGameAI):
    notify = directNotify.newCategory('DistCogdoMazeGameAI')

    def __init__(self, air, interior):
        DistCogdoGameAI.__init__(self, air, interior)

        self.numSuits = [0, 0, 0]

    def validateSenderId(self, senderId):
        return senderId in self.getToonIds()

    def requestAction(self, action, data):
        senderId = self.air.getAvatarIdFromSender()
        if not self.validateSenderId(senderId):
            return False

        if action == CogdoMazeGameGlobals.GameActions.Unlock:
            if self.locks[senderId].locked:
                self.locks[senderId].locked = False
                self.d_doAction(action, senderId)

        elif action == CogdoMazeGameGlobals.GameActions.EnterDoor:
            if senderId not in self.toonsInDoor:
                self.toonsInDoor.append(senderId)
                self.d_doAction(action, senderId)
                if self.areAllToonsInDoor():
                    self.gameOver()
                    self.d_doAction(CogdoMazeGameGlobals.GameActions.GameOver)

        elif action == CogdoMazeGameGlobals.GameActions.RevealDoor:
            self.d_doAction(action, senderId)

        elif action == CogdoMazeGameGlobals.GameActions.RevealLock:
            self.d_doAction(action, data)

    def d_doAction(self, action, data=0):
        self.sendUpdate('doAction', [action, data])

    def setNumSuits(self, numSuits):
        self.numSuits = numSuits

    def getNumSuits(self):
        return self.numSuits

    def __initLocks(self):
        self.locks = {}
        data = CogdoMazeGameGlobals.TempMazeData
        width = data['width']
        height = data['height']
        positions = self.__getLockPositions(data, width, height)
        for i in range(len(self.avIdList)):
            self.__addLock(self.avIdList[i], positions[i][0], positions[i][1])

    def __getLockPositions(self, data, width, height):
        halfWidth = int(width / 2)
        halfHeight = int(height / 2)
        quadrants = [
            (0, 0, halfWidth - 2, halfHeight - 2),
            (halfWidth + 2, 0, width - 1, halfHeight - 2),
            (0, halfHeight + 2, halfWidth - 2, height - 1),
            (halfWidth + 2, halfHeight + 2, width - 1, height - 1)]
        random.shuffle(quadrants)
        positions = []
        for i in range(len(self.avIdList)):
            quadrant = quadrants[i]
            tX = -1
            tY = -1
            while tX < 0 or data['collisionTable'][tY][tX] == 1:
                tX = random.randint(quadrant[0], quadrant[2])
                tY = random.randint(quadrant[1], quadrant[3])
            positions.append((tX, tY))

        return positions

    def __addLock(self, toonId, tX, tY):
        lock = CogdoMazeGameGlobals.CogdoMazeLockInfo(toonId, tX, tY)
        self.locks[toonId] = lock

    def getLocks(self):
        toonIds = []
        spawnPointsX = []
        spawnPointsY = []
        for lock in self.locks.values():
            toonIds.append(lock.toonId)
            spawnPointsX.append(lock.tileX)
            spawnPointsY.append(lock.tileY)

        return (toonIds, spawnPointsX, spawnPointsY)
