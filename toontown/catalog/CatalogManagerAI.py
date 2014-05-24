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
        self.getToonFields(avId)
        
    def getToonFields(self, avId):
        self.air.dbInterface.queryObject(self.air.dbId, avId, self.getToonFieldsResp)
    
    def getToonFieldsResp(self, dclass, fields):
        self.currentAvatar = fields
        accountId = self.currentAvatar['setDISLid'][0]
        self.air.dbInterface.queryObject(self.air.dbId, accountId, self.getAccountResp)
    
    def getAccountResp(self, dclass, fields):
        self.currentAccount = fields
        self.newCatalog()
        
    def newCatalog(self):
        print 'CatalogManager: Avatar %s - Checking Catalog.'%(self.currentAvatar['setName'])
        accountStartDate = self.currentAccount['CREATED']
        print 'CatalogManager: CREATED: %s'%(accountStartDate)
        currentDate = datetime.datetime.now().strftime("%a %B %d %H:%M:%S %Y")
        print 'CatalogManager: CURRENT DATE: %s'%(currentDate)
        
        accountStartDate = datetime.datetime.strptime(accountStartDate, "%a %B %d %H:%M:%S %Y")
        currentDate = datetime.datetime.strptime(currentDate, "%a %B %d %H:%M:%S %Y")
        
        difference = currentDate - accountStartDate
        weeks = difference.days / 7
        months = weeks / 4
        
        print '%s weeks have passed since creation'%(weeks)
        print '%s months have passed since creation'%(months)