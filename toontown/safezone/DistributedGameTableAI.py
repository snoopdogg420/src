from direct.distributed import DistributedObjectAI

from toontown.safezone import PicnicGameGlobals


class DistributedGameTableAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.posHpr = (0, 0, 0, 0, 0, 0)
        self.numSeats = 6
        self.seats = [0] * self.numSeats
        self.joinTimes = [0] * self.numSeats
        self.choosing = 0
        self.game = None

    # Required:

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x, y, z, h, p, r)

    def getPosHpr(self):
        return self.posHpr

    # Requests:

    def requestJoin(self, seatIndex):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        # First, let's make some obvious sanity checks:
        if (not av) or (avId in self.seats) or self.seats[seatIndex] or self.game:
            self.sendUpdateToAvatarId(avId, 'rejectJoin', [])
            return

        self.fillSeat(seatIndex, avId)

    def requestGame(self, gameIndex):
        avId = self.air.getAvatarIdFromSender()

        # First, let's make some obvious sanity checks:
        if self.game or (self.choosing != avId):
            return

        # Trim the amount of players:
        playerLimits = PicnicGameGlobals.PlayerLimits[gameIndex]
        numPlayers = self.getNumPlayers()
        while numPlayers not in playerLimits:
            numPlayers -= 1
        self.trimPlayers(numPlayers)

        self.createGame(gameIndex)

    # Handles:

    def __handleUnexpectedExit(self):
        """
        Handle a player leaving unexpectedly. If someone leaves in a two player
        game, the player who is still playing should win. If it is more than a
        two player game, however, the game should result in a draw.
        """
        pass

    # Utilities:

    def getNumPlayers(self):
        """
        Get the number of players currently sitting at the table.
        """
        return self.numSeats - self.seats.count(0)

    def trimPlayers(self, amount):
        """
        Trim the number of players down to the specified amount. This is to
        solve the issue that can occur where there are too many players on the
        table for the chosen game.

        This operates under a "first come, first serve" basis.
        """
        while self.getNumPlayers() > amount:
            # Find and remove the player with the highest join time:
            seatIndex = self.joinTimes.index(max(self.joinTimes))
            self.emptySeat(seatIndex)

    def fillSeat(self, seatIndex, avId):
        """
        Fill the provided seat with the given avatar.
        """
        # It's important that we mark the time they joined before anything
        # else, in case a conflict occurs:
        self.joinTimes[seatIndex] = globalClock.getRealTime()

        # Next, if this is the first player, make them the "chooser":
        if self.getNumPlayers() == 0:
            self.choosing = avId

        self.seats[seatIndex] = avId

        # Handling an unexpected exit is important, as the game must stop
        # immediately. Whether it be a draw, or a player winning by default:
        self.acceptOnce(
            self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit,
            extraArgs=[avId])

        self.sendUpdate('fillSeat', [seatIndex, avId])

    def emptySeat(self, seatIndex):
        """
        Empty the provided seat.
        """
        self.ignore(self.air.getAvatarExitEvent(self.seats[seatIndex]))

        self.seats[seatIndex] = 0
        self.joinTimes[seatIndex] = 0

        self.sendUpdate('emptySeat', [seatIndex])

    def createGame(self, gameIndex):
        """
        Create the provided game.
        """
        pass
