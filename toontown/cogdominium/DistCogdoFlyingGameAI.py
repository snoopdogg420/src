from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
from toontown.cogdominium import CogdoFlyingGameGlobals
from direct.distributed.ClockDelta import globalClockDelta


class DistCogdoFlyingGameAI(DistCogdoGameAI):
    notify = directNotify.newCategory('DistCogdoFlyingGameAI')

    def __init__(self, air, interior):
        DistCogdoGameAI.__init__(self, air, interior)

        self.eagleInterest = {}
        self.eagleCooldown = []

        # I hate how long these variable names are...
        # The damage constants:
        self.deathDamage = CogdoFlyingGameGlobals.AI.SafezoneId2DeathDamage[self.getHoodId()]
        self.whirlwindDamage = CogdoFlyingGameGlobals.AI.SafezoneId2WhirlwindDamage[self.getHoodId()]
        self.eagleDamage = CogdoFlyingGameGlobals.AI.SafezoneId2LegalEagleDamage[self.getHoodId()]
        self.minionDamage = CogdoFlyingGameGlobals.AI.SafezoneId2MinionDamage[self.getHoodId()]

    def getNetworkTime(self):
        return globalClockDelta.getRealNetworkTime()

    def damageAvId(self, avId, damage):
        # Get the av
        av = self.air.doId2do.get(avId)

        # Check if the av exists
        if av:

            # Damage the av
            av.takeDamage(damage)

    def requestAction(self, action, data):
        # Get the sender's avId
        avId = self.air.getAvatarIdFromSender()

        # Handle the action based on its ID
        if action == CogdoFlyingGameGlobals.AI.GameActions.RequestEnterEagleInterest:
            self.handleEnterEagleInterest(avId, data)
        elif action == CogdoFlyingGameGlobals.AI.GameActions.RequestExitEagleInterest:
            self.handleExitEagleInterest(avId, data)
        elif action == CogdoFlyingGameGlobals.AI.GameActions.HitLegalEagle:
            self.handleHitEagle(avId, data)
        elif action == CogdoFlyingGameGlobals.AI.GameActions.Spawn:
            self.handleSpawn(avId)
        elif action == CogdoFlyingGameGlobals.AI.GameActions.Died:
            self.handleDied(avId)
        elif action == CogdoFlyingGameGlobals.AI.GameActions.HitMinion:
            self.handleHitMinion(avId)
        elif action == CogdoFlyingGameGlobals.AI.GameActions.HitWhirlwind:
            self.handleHitWhirlwind(avId)

    def handleEnterEagleInterest(self, avId, eagleId):
        # Check if the eagle is in the eagleCooldown mode
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

        # Send the update saying the eagle no longer has interest in the toon
        self.d_toonClearAsEagleTarget(avId, eagleId)

    def handleHitEagle(self, avId, eagleId):
        # Add the eagleId to the eagleCooldown
        self.eagleEnterCooldown(eagleId)

        # Damage the player
        self.damageAvId(avId, self.eagleDamage)

    def handleHitMinion(self, avId):
        # Damage the player
        self.damageAvId(avId, self.minionDamage)

    def handleHitWhirlwind(self, avId):
        # Damage the player
        self.damageAvId(avId, self.whirlwindDamage)

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

    def eagleEnterCooldown(self, eagleId):
        # Check if the eagle is already in the eagleCooldown down
        if eagleId in self.eagleCooldown:
            return

        # Add the eagleId to the eagleCooldown
        self.eagleCooldown.append(eagleId)

        # Set a task to remove the eagle from eagleCooldown
        taskMgr.doMethodLater(CogdoFlyingGameGlobals.LegalEagle.CooldownTime,
            self.eagleCooldownTask, self.getEagleCooldownTaskName(eagleId),
            extraArgs=[eagleId]
        )

    def getEagleCooldownTaskName(self, eagleId):
        return '%s-%s-cooldown' % (id(self), eagleId)

    def eagleCooldownTask(self, eagleId):
        # Remove the eagle from the eagleCooldown
        self.eagleCooldown.remove(eagleId)

        # Send the update stating that the eagle has completed its cooldown
        self.d_eagleExitCooldown(eagleId)

    def d_eagleExitCooldown(self, eagleId):
        self.sendUpdate('eagleExitCooldown', [eagleId, self.getNetworkTime()])

    def d_toonSetAsEagleTarget(self, avId, eagleId):
        self.sendUpdate('toonSetAsEagleTarget', [avId, eagleId,
            self.getNetworkTime()]
        )

    def d_toonClearAsEagleTarget(self, avId, eagleId):
        self.sendUpdate('toonClearAsEagleTarget', [avId, eagleId,
            self.getNetworkTime()]
        )

    def handleDied(self, avId):
        # Damage the av
        self.damageAvId(avId, self.deathDamage)

        # Send the toonDied update
        self.d_toonDied(avId)

    def d_toonDied(self, avId):
        self.sendUpdate('toonDied', [avId, self.getNetworkTime()])

    def handleSpawn(self, avId):
        self.d_toonSpawn(avId)

    def toonSpawn(self, avId):
        self.sendUpdate('toonSpawn', [avId, self.getNetworkTime()])

    def toonSetBlades(self, todo0, todo1):
        pass

    def toonBladeLost(self, todo0):
        pass
