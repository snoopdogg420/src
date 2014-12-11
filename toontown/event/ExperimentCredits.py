from pandac.PandaModules import CardMaker
from direct.interval.IntervalGlobal import Sequence, Func
from direct.interval.LerpInterval import LerpColorScaleInterval


class ExperimentCredits:
    def __init__(self):
        self.music = loader.loadMusic('phase_4/audio/bgm/science_fair_credits.ogg')

        cm = CardMaker('screen-cover')
        cm.setFrameFullscreenQuad()
        self.screenCover = aspect2d.attachNewNode(cm.generate())
        self.screenCover.hide()
        self.screenCover.setScale(10)
        self.screenCover.setColor((0, 0, 0, 1))

    def getScreenFadeBlack(self):
        return Sequence(Func(self.screenCover.show),
                        Func(self.screenCover.setTransparency, 1),
                        LerpColorScaleInterval(self.screenCover, 3, Vec4(1, 1, 1, 1),
                                               startColorScale=Vec4(1, 1, 1, 0)),
                        Func(self.screenCover.clearColorScale),
                        Func(self.screenCover.clearTransparency))

    def start(self):
        base.musicManager.stopAllSounds()

        self.music.play()
        Sequence(self.getScreenFadeBlack()).start()

    def stop(self):
        self.screenCover.hide()

    def cleanup(self):
        self.screenCover.removeNode()
