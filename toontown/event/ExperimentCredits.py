from pandac.PandaModules import CardMaker, TransparencyAttrib
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.gui.OnscreenImage import OnscreenImage


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

        )

        self.creditsSeq.start()

    def stop(self):
        pass

    def cleanup(self):
        pass
