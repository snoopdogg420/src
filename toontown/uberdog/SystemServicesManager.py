from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify

class SystemServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('SystemServicesManager')
    
    def systemMessage(self, msg):
        pass
