from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
from direct.distributed.ClockDelta import globalClockDelta


class DistCogdoFlyingGameAI(DistCogdoGameAI):
    notify = directNotify.newCategory('DistCogdoFlyingGameAI')

    def requestAction(self, todo0, todo1):
        pass

    def requestPickUp(self, pickupNum, pickupType):
        avId = self.air.getAvatarIdFromSender()
        self.pickUp(avId, pickupNum)

    def pickUp(self, avId, pickupNum):
        self.sendUpdate('pickUp', [avId, pickupNum, globalClockDelta.getRealNetworkTime()])

    def debuffPowerup(self, todo0, todo1, todo2):
        pass

    def doAction(self, todo0, todo1):
        pass

    def eagleExitCooldown(self, todo0, todo1):
        pass

    def toonSetAsEagleTarget(self, todo0, todo1, todo2):
        pass

    def toonClearAsEagleTarget(self, todo0, todo1, todo2):
        pass

    def toonDied(self, todo0, todo1):
        pass

    def toonSpawn(self, todo0, todo1):
        print 'toonSpawned'
        print todo0, todo1

    def toonSetBlades(self, todo0, todo1):
        pass

    def toonBladeLost(self, todo0):
        pass
