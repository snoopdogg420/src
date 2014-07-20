from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from direct.distributed import ClockDelta
from BankGlobals import *

class DistributedBankAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBankAI")

    def __init__(self, air, furnitureMgr, catalogItem, ownerId):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.ownerId = ownerId
        self.busy = 0

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()

        if not self.busy:
            if avId == self.ownerId:
                self.sendBankMovie(avId)
            else:
                self.sendNotOwnerMovie(avId)

            self.acceptOnce(self.air.getAvatarExitEvent(avId),
                            self.__handleUnexpectedExit)

    def freeAvatar(self):
        self.sendExitMovie()
        self.sendClearMovie()

    def setMovie(self, mode, avId):
        self.sendUpdate('setMovie', args=[mode,
            avId, ClockDelta.globalClockDelta.getRealNetworkTime()])

    def sendBankMovie(self, avId):
        self.setMovie(BANK_MOVIE_GUI, avId)
        self.busy = avId

    def sendNotOwnerMovie(self, avId):
        self.setMovie(BANK_MOVIE_NOT_OWNER, avId)

    def sendExitMovie(self):
        self.setMovie(BANK_MOVIE_WITHDRAW, self.busy)

    def sendClearMovie(self):
        self.setMovie(BANK_MOVIE_CLEAR, self.busy)
        self.busy = 0

    def transferMoney(self, amount):
        av = self.air.doId2do.get(self.busy)
        if not av:
            return

        av.b_setBankMoney(min(av.getBankMoney() + amount, av.getMaxBankMoney()))
        av.b_setMoney(max(av.getMoney() - amount, 0))
        self.freeAvatar()

    def __handleUnexpectedExit(self):
        self.busy = 0
