from pandac.PandaModules import CardMaker, TransparencyAttrib, NodePath
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.gui.OnscreenImage import OnscreenImage
from toontown.toon.ToonDNA import ToonDNA
from toontown.toon.Toon import Toon


STYLE_LEFT = 1
STYLE_RIGHT = 2


class ExperimentCreditsToonSlide(NodePath):
    DNA_INDEX = 0
    POSE_INDEX = 1

    def __init__(self, toonInfo, text, style, duration):
        NodePath.__init__(self, 'ExperimentCreditsToonSlide')

        self.toonInfo = toonInfo
        self.text = text
        self.style = style
        self.duration = duration

        self.toon = None

        self.createToon()

        if style == STYLE_LEFT:
            self.createStyleLeft()
        elif style == STYLE_RIGHT:
            self.createStyleRight()

        self.hide()

    def createStyleLeft(self):
        self.reparentTo(base.a2dTopLeft)

        self.toon.setPos(self, 0.52, 0, -1.60)

    def createStyleRight(self):
        pass

    def createToon(self):
        self.toon = Toon()

        dna = ToonDNA()
        dna.newToonFromProperties(*self.toonInfo[self.DNA_INDEX])

        self.toon.setDNA(dna)

        self.toon.pose(*self.toonInfo[self.POSE_INDEX])
        self.toon.setScale(0.3)
        self.toon.setH(200)

        self.toon.getGeomNode().setDepthWrite(1)
        self.toon.getGeomNode().setDepthTest(1)

        self.toon.reparentTo(self)


    def construct(self):
        seq = Sequence(

              Sequence(Func(self.show),
                       Func(self.setTransparency, 1),
                       LerpColorScaleInterval(self, 3, Vec4(1, 1, 1, 1),
                                              startColorScale=Vec4(1, 1, 1, 0)),
                       Func(self.clearColorScale),
                       Func(self.clearTransparency)),

              Wait(self.duration),

              Sequence(Func(self.setTransparency, 1),
                       LerpColorScaleInterval(self, 3, Vec4(1, 1, 1, 0),
                                              startColorScale=Vec4(1, 1, 1, 1)),
                       Func(self.clearColorScale),
                       Func(self.clearTransparency),
                       Func(self.hide)),

              )

        return seq


chanSlide = ExperimentCreditsToonSlide(
(
['mss', 'ls', 'l', 'm', 10, 0, 10, 10, 1, 5, 1, 5, 1, 11], # The Toon DNA
['bored', 135] # Pose information
),
'', # Text to be shown
STYLE_LEFT, # Put the toon on the left side of the screen
5.0 # The duration in seconds
)


class ExperimentCredits:
    def __init__(self):
        self.music = loader.loadMusic('phase_4/audio/bgm/science_fair_credits.ogg')

        cm = CardMaker('screen-cover')
        cm.setFrameFullscreenQuad()
        self.screenCover = render2d.attachNewNode(cm.generate())
        self.screenCover.hide()
        self.screenCover.setScale(100)
        self.screenCover.setColor((0, 0, 0, 1))

        self.logo = OnscreenImage(image='phase_3/maps/toontown-logo.png',
                                  scale=(1.0 * (4.0/3.0), 1, 1.0 / (4.0/3.0)),
                                  pos=(-0.05, 1, -0.85))
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.reparentTo(base.a2dTopCenter)
        self.logo.hide()

        self.creditsSeq = None

    def disableToonInterface(self):
        pass

    def enableToonInterface(self):
        pass

    def start(self):
        base.musicManager.stopAllSounds()

        self.disableToonInterface()

        self.music.play()


        self.creditsSeq = Sequence(

        # Fade the screen black
        Sequence(Func(self.screenCover.show),
                        Func(self.screenCover.setTransparency, 1),
                        LerpColorScaleInterval(self.screenCover, 4, Vec4(1, 1, 1, 1),
                                               startColorScale=Vec4(1, 1, 1, 0)),
                        Func(self.screenCover.clearColorScale),
                        Func(self.screenCover.clearTransparency)),

        # Fade the logo in
        Sequence(Func(self.logo.show),
                 LerpColorScaleInterval(self.logo, 2, Vec4(1, 1, 1, 1),
                                        startColorScale=Vec4(1, 1, 1, 0)),
                 Func(self.logo.clearColorScale)),

        # Wait 2 seconds
        Wait(2.0),

        # Fade the logo out
        Sequence(LerpColorScaleInterval(self.logo, 5, Vec4(1, 1, 1, 0),
                                        startColorScale=Vec4(1, 1, 1, 1)),
                 Func(self.logo.clearColorScale),
                 Func(self.logo.hide)),

        # Chan's slide
        chanSlide.construct(),

        )

        self.creditsSeq.start()

    def stop(self):
        pass

    def cleanup(self):
        pass
