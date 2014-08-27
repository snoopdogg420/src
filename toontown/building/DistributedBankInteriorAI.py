from direct.distributed.ClockDelta import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task.Task import Task
import time

from otp.ai.MagicWordGlobal import *
from toontown.building.DistributedBankCollectableAI import DistributedBankCollectableAI


class DistributedBankInteriorAI(DistributedObjectAI):
    def __init__(self, block, air, zoneId):
        DistributedObjectAI.__init__(self, air)

        self.block = block
        self.zoneId = zoneId

        self.bankCollectable = None

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.sendUpdate('setState', ['vaultClosed', 0])

        delay = 3600 - (int(time.time()) % 3600)  # Time until the next hour.
        taskMgr.doMethodLater(delay, self.createBankCollectable, 'createBankCollectable')

    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]

    def __handleDeleteBankCollectable(self, task):
        if self.bankCollectable is not None:
            self.bankCollectable.requestDelete()
            self.bankCollectable = None

        self.sendUpdate('setState', ['vaultClosing', globalClockDelta.getRealNetworkTime()])
        taskMgr.doMethodLater(5, self.closedTask, self.uniqueName('closedTask'))

        return Task.done

    def createBankCollectable(self, task=None):
        self.bankCollectable = DistributedBankCollectableAI(self.air)
        self.bankCollectable.generateWithRequired(self.zoneId)

        self.sendUpdate('setState', ['vaultOpening', globalClockDelta.getRealNetworkTime()])
        taskMgr.doMethodLater(5, self.openedTask, self.uniqueName('openedTask'))

        taskMgr.doMethodLater(3600, self.createBankCollectable, 'createBankCollectable')
        taskMgr.doMethodLater(60, self.__handleDeleteBankCollectable, 'deleteBankCollectable')

        if task is not None:
            return Task.done

    def closedTask(self, task):
        self.sendUpdate('setState', ['vaultClosed', 0])
        return Task.done

    def openedTask(self, task):
        self.sendUpdate('setState', ['vaultOpen', 0])
        return Task.done
