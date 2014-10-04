from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM

class DistributedTrickOrTreatTargetAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTrickOrTreatTargetAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'TrickOrTreatTargeFSM')
        self.air = air
        self.trickOrTreatInfo = simbase.backups.load('holidays', ('halloween',), default= {})
        
    def enterOff(self):
        self.requestDelete()
        
    def requestScavengerHunt(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av is None:
            return
        zones = self.trickOrTreatInfo.get(str(avId), [])
        if self.zoneId in zones:
            self.sendUpdate('doScavengerHunt', [0])
        else:
            self.trickOrTreatInfo.setdefault(str(avId), []).append(self.zoneId)
            self.sendUpdate('doScavengerHunt', [100])
        if len(zones) == 6:
            av.b_setCheesyEffect(12, 0, 0)
        simbase.backups.save('holidays', ('halloween',), self.trickOrTreatInfo)

