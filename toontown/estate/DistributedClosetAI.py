from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed import ClockDelta
from direct.task.Task import Task

from ClosetGlobals import *
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from toontown.toon import ToonDNA


class DistributedClosetAI(DistributedFurnitureItemAI):
    notify = directNotify.newCategory('DistributedClosetAI"')

    def __init__(self, air, furnitureMgr, catalogItem, ownerId):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)

        self.ownerId = ownerId
        self.busy = 0
        self.customerId = 0
        self.customerDNA = None

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def getOwnerId(self):
        return self.ownerId

    def enterAvatar(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if not self.busy:
            self.setState(
                OPEN, avId, self.ownerId, av.dna.gender,
                av.clothesTopsList, av.clothesBottomsList)
            self.busy = avId
            self.customerId = avId
            self.customerDNA = ToonDNA.ToonDNA()
            self.customerDNA.makeFromNetString(av.dna.makeNetString())
            taskMgr.doMethodLater(TIMEOUT_TIME, self.__timeout, self.uniqueName('timeout'))
        else:
            self.freeAvatar(avId)

    def __timeout(self, task):
        self.setMovie(CLOSET_MOVIE_TIMEOUT, self.busy)
        av = self.air.doId2do.get(self.customerId)
        self.busy = 0
        self.customerId = 0
        self.customerDNA = None
        taskMgr.remove(self.uniqueName('timeout'))
        self.setState(
            CLOSED, self.customerId, self.ownerId, av.dna.gender,
            av.clothesTopsList, av.clothesBottomsList)
        self.setMovie(CLOSET_MOVIE_CLEAR, 0)
        return Task.done

    def freeAvatar(self, avId):
        self.sendUpdateToAvatarId(avId, 'freeAvatar')

    def removeItem(self, trashItem, t_or_b):
        av = self.air.doId2do.get(self.customerId)
        if not av:
            return
        dna = ToonDNA.ToonDNA()
        dna.makeFromNetString(trashItem)
        if t_or_b == SHIRT:
            av.removeItemInClothesTopsList(
                dna.topTex, dna.topTexColor, dna.sleeveTex, dna.sleeveTexColor)
            av.d_setClothesTopsList(av.clothesTopsList)
        else:
            av.removeItemInClothesBottomsList(dna.botTex, dna.botTexColor)
            av.d_setClothesBottomsList(av.clothesBottomsList)

    def setDNA(self, dnaString, finished, whichItems):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.customerId:
            if self.customerId:
                self.air.writeServerEvent('suspicious', avId, 'DistributedClosetAI.setDNA customer is %s' % self.customerId)
                self.notify.warning('customerId: %s, but got setDNA for: %s' % (self.customerId, avId))
            return
        testDNA = ToonDNA.ToonDNA()
        if not testDNA.isValidNetString(dnaString):
            self.air.writeServerEvent('suspicious', avId, 'DistributedClosetAI.setDNA: invalid dna: %s' % dnaString)
            return
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if (finished == 2) and (whichItems > 0):
            av.b_setDNAString(dnaString)
            self.air.writeServerEvent('changeClothes', avId, '%s|%s|%s' % (self.doId, whichItems, self.customerDNA.asTuple()))
        elif finished == 1:
            if self.customerDNA:
                av.b_setDNAString(self.customerDNA.makeNetString())
        else:
            self.sendUpdate('setCustomerDNA', [avId, dnaString])
        if finished == 0:
            return
        if self.busy == avId:
            self.completePurchase(avId)
        elif self.busy:
            self.air.writeServerEvent('suspicious', avId, 'DistributedClosetAI.setDNA busy with %s' % self.busy)
            self.notify.warning('setDNA from unknown avId: %s busy: %s' % (avId, self.busy))

    def setState(self, mode, avId, ownerId, gender, topList, bottomList):
        self.sendUpdateToAvatarId(
            avId, 'setState',
            args=[mode, avId, ownerId, gender, topList, bottomList])

    def setMovie(self, mode, avId):
        timestamp = ClockDelta.globalClockDelta.getRealNetworkTime(bits=32)
        self.sendUpdate('setMovie', args=[mode, avId, timestamp])

    def completePurchase(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        self.setMovie(CLOSET_MOVIE_COMPLETE, avId)
        self.busy = 0
        self.customerId = 0
        self.customerDNA = None
        taskMgr.remove(self.uniqueName('timeout'))
        self.setState(
            CLOSED, avId, self.ownerId, av.dna.gender,
            av.clothesTopsList, av.clothesBottomsList)
        self.setMovie(CLOSET_MOVIE_CLEAR, 0)
