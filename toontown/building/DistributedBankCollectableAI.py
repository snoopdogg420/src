from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task.Task import Task


class DistributedBankCollectableAI(DistributedObjectAI):
    def requestGrab(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return

        self.sendUpdate('grab', [avId])
        av.addMoney(100)

        taskName = self.uniqueName('deleteBankCollectable')
        taskMgr.doMethodLater(5, self.__handleDeleteBankCollectable, taskName)

    def __handleDeleteBankCollectable(self, task):
        self.requestDelete()
        return Task.done
