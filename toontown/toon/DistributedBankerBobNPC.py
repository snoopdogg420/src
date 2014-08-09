from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.hood import ZoneUtil
from toontown.nametag.NametagGlobals import *
from toontown.quest import QuestChoiceGui
from toontown.quest import QuestParser
from toontown.quest import TrackChoiceGui
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TeaserPanel


ChoiceTimeout = 20


class DistributedBankerBobNPC(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.curQuestMovie = None
        self.questChoiceGui = None
        self.trackChoiceGui = None
        return

    def disable(self):
        self.cleanupMovie()
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        self.sendUpdate('avatarEnter', [])
        self.nametag3d.setDepthTest(0)
        self.nametag3d.setBin('fixed', 0)

    def finishMovie(self, av, isLocalToon, elapsedTime):
        av.startLookAround()
        self.startLookAround()
        self.detectAvatars()
        self.initPos()
        if isLocalToon:
            taskMgr.remove(self.uniqueName('lerpCamera'))
            base.localAvatar.posCamera(0, 0)
            base.cr.playGame.getPlace().setState('walk')
            self.sendUpdate('setMovieDone', [])
            self.nametag3d.clearDepthTest()
            self.nametag3d.clearBin()

    def exitInteraction(self):
        self.clearChat()
        self.startLookAround()
        self.detectAvatars()
        av = base.cr.doId2do.get(avId)
        if isLocalToon:
            base.localAvatar.posCamera(0, 0)
            base.cr.playGame.getPlace().setState('walk')
        self.setChatAbsolute('Don\'t spend them all at once now.', CFSpeech | CFTimeout)

    def cleanupMovie(self):
        print 'Cleaning a movie..?'
