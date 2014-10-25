from direct.distributed.DistributedObject import DistributedObject
from toontown.catalog.CatalogItemList import CatalogItemList
import time


class CatalogManager(DistributedObject):
    notify = directNotify.newCategory('CatalogManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.popularItems = None

    def generate(self):
        if base.cr.catalogManager != None:
            base.cr.catalogManager.delete()
        base.cr.catalogManager = self
        DistributedObject.generate(self)
        if hasattr(base.localAvatar, 'catalogScheduleNextTime') and base.localAvatar.catalogScheduleNextTime == 0:
            self.d_startCatalog()

    def disable(self):
        base.cr.catalogManager = None
        DistributedObject.disable(self)

    def delete(self):
        base.cr.catalogManager = None
        DistributedObject.delete(self)

    def d_startCatalog(self):
        self.sendUpdate('startCatalog')

    def fetchPopularItems(self):
        self.sendUpdate('fetchPopularItems')

    def setPopularItems(self, popularItems):
        self.popularItems = CatalogItemList(popularItems)
        messenger.send('PopularItemsSet')
