from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI

class DistributedClosetAI(DistributedFurnitureItemAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedClosetAI")
    
    def __init__(self, air, furnitureMgr, catalogItem, ownerId):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, catalogItem)
        self.ownerId = ownerId

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId
    
    def getOwnerId(self):
        return self.ownerId

    def enterAvatar(self):
        pass

    def freeAvatar(self):
        pass

    def removeItem(self, todo0, todo1):
        pass

    def setDNA(self, todo0, todo1, todo2):
        pass

    def setState(self, todo0, todo1, todo2, todo3, todo4, todo5):
        pass

    def setMovie(self, todo0, todo1, todo2):
        pass

    def resetItemLists(self):
        pass

    def setCustomerDNA(self, todo0, todo1):
        pass

