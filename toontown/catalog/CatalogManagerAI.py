from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.PyDatagram import *
from direct.distributed.PyDatagramIterator import PyDatagramIterator
import CatalogGenerator
import datetime

class CatalogManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CatalogManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.catalogGenerator = CatalogGenerator.CatalogGenerator()
        
        self.currentAvatar = {}
        self.currentAccount = {}

    def startCatalog(self):
        avId = self.air.getAvatarIdFromSender()
        self.accept('generate-%s'%(avId), self.avatarCreated, extraArgs=[avId])
        
    def avatarCreated(self, avId, dclass):
        pass