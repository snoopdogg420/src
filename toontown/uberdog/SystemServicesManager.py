from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed.PotentialAvatar import PotentialAvatar
from pandac.PandaModules import *

class SystemServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('SystemServicesManager')
    
    def systemMessage(self, msg):
        #The client doesn't get to do shit
        pass
