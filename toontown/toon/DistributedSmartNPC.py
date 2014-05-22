from pandac.PandaModules import *
from DistributedNPCToonBase import *
from toontown.quest import QuestParser
from toontown.quest import QuestChoiceGui
from toontown.quest import TrackChoiceGui
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel
from otp.nametag.NametagConstants import *

class DistributedSmartNPC(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        self.sendUpdate('avatarEnter', [])
        
    def greet(self, npcId, avId):
        if avId in base.cr.doId2do:
            avName = base.cr.doId2do.get(avId).getName()
            self.setChatAbsolute('Hello, %s' % avName + '!', CFSpeech | CFTimeout)

    def respond(self, npcId, message, avId):
        try:
            name = base.cr.doId2do.get(avId).getName()
            self.setChatAbsolute(message, CFSpeech | CFTimeout)
        except:
            print 'Responding to non-available character!'
