from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from toontown.toon.DistributedToonAI import DistributedToonAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pandac.PandaModules import *

class SystemServicesManagerAI(DistributedObjectGlobalAI):
    notify = directNotify.newCategory('SystemServicesManager')
    
    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)
    
    def gameWhisper(self, msg, shards):
        for doId, do in simbase.air.doId2do.items():
            if 'DistributedToonAI' in str(simbase.air.doId2do[doId]):
                do.sendUpdate('setSystemMessage', [0, msg])
