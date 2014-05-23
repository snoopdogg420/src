from ClickablePopup import *
from MarginPopup import *
from otp.nametag import NametagGlobals
from otp.nametag.NametagConstants import *


class WhisperPopup(MarginPopup, ClickablePopup):
    WTNormal = WTNormal
    WTQuickTalker = WTQuickTalker
    WTSystem = WTSystem
    WTBattleSOS = WTBattleSOS
    WTEmote = WTEmote
    WTToontownBoardingGroup = WTToontownBoardingGroup

    WORDWRAP = 7.5
    SCALE_2D = 0.25

    def __init__(self, text, font, whisperType, timeout=10.0):
        ClickablePopup.__init__(self)
        MarginPopup.__init__(self)

        self.active = 0
        self.senderName = ''
        self.fromId = 0
        self.isPlayer = 0

        self.innerNP = NodePath.anyPath(self).attachNewNode('innerNP')
        self.innerNP.setScale(self.SCALE_2D)

        self.text = text
        self.font = font
        self.whisperType = whisperType
        self.timeout = timeout

        self.left = 0.0
        self.right = 0.0
        self.bottom = 0.0
        self.top = 0.0

        self.updateContents()

        self.setPriority(2)
        self.setVisible(True)

    def updateContents(self):
        if self.whisperType in WHISPER_COLORS:
            wt = self.whisperType
        else:
            wt = WTSystem
        clickState = self.getClickState() if self.active else 0
        fgColor, bgColor = WHISPER_COLORS[wt][clickState]

        balloon = NametagGlobals.speechBalloon2d.generate(
            self.text, self.font, textColor=fgColor, balloonColor=bgColor,
            wordWrap=self.WORDWRAP)
        balloon.reparentTo(self.innerNP)

        # Calculate the center of the TextNode.
        text = balloon.find('**/+TextNode')
        t = text.node()
        self.left, self.right, self.bottom, self.top = t.getFrameActual()
        center = self.innerNP.getRelativePoint(
            text, ((self.left+self.right) / 2.0, 0, (self.bottom+self.top) / 2.0))

        # Next translate the balloon along the inverse.
        balloon.setPos(balloon, -center)
        self.testpos = balloon.getPos()

        if self.active and self.fromId:
            self.setClickRegionEvent('clickedWhisper', extraArgs=[self.fromId, self.isPlayer])
        else:
            self.setClickRegionEvent(None)

    def marginVisibilityChanged(self):
        self.considerUpdateClickRegion()

    def considerUpdateClickRegion(self):
        if self.isDisplayed() and self.active:
            print self.left, self.right, self.bottom, self.top
            if hasattr(self, 'testpos'):
                print self.testpos
            self.updateClickRegion(self.left, self.right, self.bottom, self.top)

    def setClickable(self, senderName, fromId, isPlayer=0):
        self.active = 1
        self.senderName = senderName
        self.fromId = fromId
        self.isPlayer = isPlayer
        self.updateContents()
        self.considerUpdateClickRegion()

    def clickStateChanged(self):
        self.updateContents()

    def manage(self, manager):
        MarginPopup.manage(self, manager)

        taskMgr.doMethodLater(self.timeout, self.unmanage,
                              'whisper-timeout-%d' % id(self), [manager])

    def unmanage(self, manager):
        MarginPopup.unmanage(self, manager)

        ClickablePopup.destroy(self)
        self.innerNP.removeNode()
