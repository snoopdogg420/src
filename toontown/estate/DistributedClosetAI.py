from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from direct.distributed import ClockDelta
from toontown.toon import ToonDNA
from ClosetGlobals import *

class DistributedClosetAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedClosetAI")
    
    def __init__(self, air, furnitureMgr, catalogItem, ownerId):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.ownerId = ownerId
        self.busy = 0
        self.customerId = 0
        self.customerDNA = ToonDNA.ToonDNA()
        self.timedOut = 0

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId
    
    def getOwnerId(self):
        return self.ownerId

    def enterAvatar(self):
        avId = self.air.getAvatarIdFromSender()
        
        if not self.busy:   
            self.sendOpenMovie(avId)
        else:
            self.freeAvatar(avId)

    def freeAvatar(self, avId):
        self.sendUpdateToAvatarId(avId, 'freeAvatar', args=[])

    def removeItem(self, todo0, todo1):
        pass

    def setDNA(self, blob, finished, which):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.customerId:
            if self.customerId:
                self.air.writeServerEvent('suspicious', avId, 'DistributedClosetAI.setDNA customer is %s' % self.customerId)
                self.notify.warning('customerId: %s, but got setDNA for: %s' % (self.customerId, avId))
            return
        testDNA = ToonDNA.ToonDNA()
        if not testDNA.isValidNetString(blob):
            self.air.writeServerEvent('suspicious', avId, 'DistributedClosetAI.setDNA: invalid dna: %s' % blob)
            return
        if self.air.doId2do.has_key(avId):
            av = self.air.doId2do[avId]
            if finished == 2 and which > 0:
                av.b_setDNAString(blob)
                self.air.writeServerEvent('ChangeClothes', avId, '%s|%s|%s' % (self.doId, which, self.customerDNA.asTuple()))
            elif finished == 1:
                if self.customerDNA:
                    av.b_setDNAString(self.customerDNA.makeNetString())
            else:
                self.sendUpdate('setCustomerDNA', [avId, blob])
        else:
            self.notify.warning('no av for avId: %d' % avId)
        if self.timedOut == 1 or finished == 0:
            return
        if self.busy == avId:
            taskMgr.remove(self.uniqueName('clearMovie'))
            self.completePurchase(avId)
        elif self.busy:
            self.air.writeServerEvent('suspicious', avId, 'DistributedClosetAI.setDNA busy with %s' % self.busy)
            self.notify.warning('setDNA from unknown avId: %s busy: %s' % (avId, self.busy))

    def setState(self, mode, avId, ownerId, gender, topList, bottomList):
        self.sendUpdateToAvatarId(avId, 'setState', args=[mode, avId, ownerId, gender, topList, bottomList])

    def setMovie(self, mode, avId):
        self.sendUpdate('setMovie', args=[mode,
            avId, ClockDelta.globalClockDelta.getRealNetworkTime()])
        
    def sendOpenMovie(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        
        gender = av.dna.gender
        topList = av.clothesTopsList
        bottomList = av.clothesBottomsList
        
        self.setState(OPEN, avId, self.ownerId, gender, topList, bottomList)
        self.busy = avId
        self.customerId = avId
        self.customerDNA.makeFromNetString(av.getDNAString())
        #self.acceptOnce(self.air.getAvatarExitEvent(self.busy), self.sendTimeoutMovie, self.uniqueName('clearMovie'))
        
    def sendClearMovie(self):
        self.timedOut = 0
        self.setMovie(CLOSET_MOVIE_CLEAR, self.busy)
        self.sendUpdate('setCustomerDNA', args=[0, ''])
        
    def sendTimeoutMovie(self):
        self.setMovie(CLOSET_MOVIE_TIMEOUT, self.busy)
        self.sendClearMovie()
        self.busy = 0
        self.customerId = 0
        self.timedOut = 1
        
    def completePurchase(self, avId):
        self.setMovie(CLOSED, avId)
        self.setMovie(CLOSET_MOVIE_COMPLETE, avId)
        self.sendClearMovie()
        self.busy = 0
        self.customerId = 0

    def resetItemLists(self):
        pass

    def setCustomerDNA(self, todo0, todo1):
        pass
