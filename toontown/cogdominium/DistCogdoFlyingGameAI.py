from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
from toontown.cogdominium import CogdoFlyingGameGlobals
from direct.distributed.ClockDelta import globalClockDelta


class DistCogdoFlyingGameAI(DistCogdoGameAI):
    notify = directNotify.newCategory('DistCogdoFlyingGameAI')

    def __init__(self, air, interior):
        DistCogdoGameAI.__init__(self, air, interior)

        self.eagleInterest = {}
        self.eagleCooldown = []

    def getNetworkTime(self):
        return globalClockDelta.getRealNetworkTime()

    def requestAction(self, action, data):
        # Get the sender's avId
        avId = self.air.getAvatarIdFromSender()

        # Handle the action based on its ID
        if action == CogdoFlyingGameGlobals.AI.GameActions.RequestEnterEagleInterest:
            self.handleEnterEagleInterest(avId, data)
        elif action == CogdoFlyingGameGlobals.AI.GameActions.RequestExitEagleInterest:
            self.handleExitEagleInterest(avId, data)

    def handleEnterEagleInterest(self, avId, eagleId):
        # Check if the eagle is cooldown mode
        if eagleId in self.eagleCooldown:
            return

        # Check if the eagle already has interest in another toon
        if eagleId in self.eagleInterest:
            return

        # Add the eagle into the eagleInterest
        self.eagleInterest[eagleId] = avId

        # Looks like the eagle is ready to get the toon!
        self.d_toonSetAsEagleTarget(avId, eagleId)

    def handleExitEagleInterest(self, avId, eagleId):
        # Check if the eagle has interest
        if not eagleId in self.eagleInterest:
            return

        # Remove the eagle from the eagleInterest
        del self.eagleInterest[eagleId]

        # TODO: Put the eagle into cooldown
        # Send the update saying the eagle no longer has interest in the toon
        self.d_toonClearAsEagleTarget(avId, eagleId)

    def requestPickUp(self, pickupNum, pickupType):
        # Get the sender's avId
        avId = self.air.getAvatarIdFromSender()

        # For now, we will automatically give them the item.
        # TODO: Logic checks
        self.d_pickUp(avId, pickupNum)

    def d_pickUp(self, avId, pickupNum):
        self.sendUpdate('pickUp', [avId, pickupNum, self.getNetworkTime()])

    def debuffPowerup(self, todo0, todo1, todo2):
        pass

    def d_doAction(self, action, data):
        self.sendUpdate('doAction', [action, data])

    def eagleExitCooldown(self, todo0, todo1):
        pass

    def d_toonSetAsEagleTarget(self, avId, eagleId):
        self.sendUpdate('toonSetAsEagleTarget', [avId, eagleId,
            self.getNetworkTime()]
        )

    def d_toonClearAsEagleTarget(self, avId, eagleId):
        self.sendUpdate('toonClearAsEagleTarget', [avId, eagleId,
            self.getNetworkTime()]
        )

    def toonDied(self, todo0, todo1):
        pass

    def toonSpawn(self, todo0, todo1):
        pass

    def toonSetBlades(self, todo0, todo1):
        pass

    def toonBladeLost(self, todo0):
        pass
