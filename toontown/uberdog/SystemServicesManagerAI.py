from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from toontown.toon.DistributedToonAI import DistributedToonAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pandac.PandaModules import *

class SystemServicesManagerAI(DistributedObjectGlobalAI):
    notify = directNotify.newCategory('SystemServicesManager')
    
    def systemMessage(self, msg, shards):
        for obj in simbase.air.doId2do.items():
            if 'DistributedToonAI' in str(simbase.air.doId2do[obj[0]]):
                    obj[1].sendUpdate('setSystemMessage', [0, msg])
