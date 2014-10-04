from otp.speedchat import SpeedChatGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *

class DistributedTrickOrTreatTarget(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrickOrTreatTarget')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.triggered = False
        self.triggerDelay = 15
        
    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, self.phraseSaid)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        DistributedTrickOrTreatTarget.notify.debug('announceGenerate')

    def phraseSaid(self, phraseId):
        self.notify.debug('Checking if phrase was said')
        helpPhrase = 10003

        def reset():
            self.triggered = False

        if phraseId == helpPhrase and not self.triggered:
            self.triggered = True
            self.d_requestScavengerHunt()
            taskMgr.doMethodLater(self.triggerDelay, reset, 'ScavengerHunt-phrase-reset', extraArgs=[])
            
    def delete(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.delete(self)
        
    def d_requestScavengerHunt(self):
        self.sendUpdate('requestScavengerHunt', [])

    def doScavengerHunt(self, avId, amount):
        DistributedTrickOrTreatTarget.notify.debug('doScavengerHunt')
        print(avId)
        av = base.localAvatar
        av.trickOrTreatTargetMet(amount)
        