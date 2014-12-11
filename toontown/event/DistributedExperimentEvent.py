from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import Filename, Vec4

from otp.ai.MagicWordGlobal import *
from toontown.event import ExperimentChallenges
from toontown.event.DistributedEvent import DistributedEvent
from toontown.event.ExperimentBlimp import ExperimentBlimp
from toontown.event.ExperimentChallengeGUI import ExperimentChallengeGUI
from toontown.event.ExperimentCredits import ExperimentCredits


class DistributedExperimentEvent(DistributedEvent):
    notify = directNotify.newCategory('DistributedExperimentEvent')

    def __init__(self, cr):
        DistributedEvent.__init__(self, cr)

        self.introMusic = base.loadMusic('phase_4/audio/bgm/TE_battle_intro.ogg')
        self.music = base.loadMusic('phase_4/audio/bgm/TE_battle.ogg')
        self.musicSequence = None
        self.credits = None

        self.blimp = None

        self.challengeGui = None
        self.phase = 0

    def start(self):
        taskMgr.remove('TT-birds')

        base.musicManager.stopAllSounds()
        base.lockMusic()

        self.musicSequence = Sequence(
            Func(base.playMusic, self.introMusic, looping=0, volume=1, playLocked=True),
            Wait(self.introMusic.length()),
            Func(base.playMusic, self.music, looping=1, volume=1, playLocked=True))
        self.musicSequence.start()

        if __debug__:
            skyblue2Filename = Filename('../resources/phase_3.5/maps/skyblue2_invasion.jpg')
            middayskyBFilename = Filename('../resources/phase_3.5/maps/middayskyB_invasion.jpg')
            toontown_central_tutorial_palette_4amla_1Filename = Filename('../resources/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1_invasion.jpg')
            toontown_central_tutorial_palette_4amla_1_aFilename = Filename('../resources/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1_a_invasion.rgb')
        else:
            skyblue2Filename = Filename('/phase_3.5/maps/skyblue2_invasion.jpg')
            middayskyBFilename = Filename('/phase_3.5/maps/middayskyB_invasion.jpg')
            toontown_central_tutorial_palette_4amla_1Filename = Filename('/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1_invasion.jpg')
            toontown_central_tutorial_palette_4amla_1_aFilename = Filename('/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1_a_invasion.rgb')
        self.cr.playGame.hood.sky.findTexture('skyblue2').read(skyblue2Filename)
        self.cr.playGame.hood.sky.findTexture('middayskyB').read(middayskyBFilename)
        self.cr.playGame.hood.sky.findTexture('toontown_central_tutorial_palette_4amla_1').read(toontown_central_tutorial_palette_4amla_1Filename, toontown_central_tutorial_palette_4amla_1_aFilename, 0, 0)

        render.setColorScale(Vec4(0.85, 0.65, 0.65, 1))
        aspect2d.setColorScale(Vec4(0.85, 0.65, 0.65, 1))

    def delete(self):
        self.cleanupDestruction()

        base.musicManager.stopAllSounds()
        base.unlockMusic()

        DistributedEvent.delete(self)

    def cleanupDestruction(self):
        if self.musicSequence:
            self.musicSequence.finish()
            self.musicSequence = None

        if self.blimp:
            self.blimp.cleanup()
            self.blimp = None

        base.setCellsActive(base.bottomCells[:2], 1)
        if self.challengeGui:
            self.challengeGui.destroy()

        if __debug__:
            skyblue2Filename = Filename('../resources/phase_3.5/maps/skyblue2.jpg')
            middayskyBFilename = Filename('../resources/phase_3.5/maps/middayskyB.jpg')
            toontown_central_tutorial_palette_4amla_1Filename = Filename('../resources/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1.jpg')
            toontown_central_tutorial_palette_4amla_1_aFilename = Filename('../resources/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1_a.rgb')
        else:
            skyblue2Filename = Filename('/phase_3.5/maps/skyblue2.jpg')
            middayskyBFilename = Filename('/phase_3.5/maps/middayskyB.jpg')
            toontown_central_tutorial_palette_4amla_1Filename = Filename('/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1.jpg')
            toontown_central_tutorial_palette_4amla_1_aFilename = Filename('/phase_3.5/maps/toontown_central_tutorial_palette_4amla_1_a.rgb')
        self.cr.playGame.hood.sky.findTexture('skyblue2').read(skyblue2Filename)
        self.cr.playGame.hood.sky.findTexture('middayskyB').read(middayskyBFilename)
        self.cr.playGame.hood.sky.findTexture('toontown_central_tutorial_palette_4amla_1').read(toontown_central_tutorial_palette_4amla_1Filename, toontown_central_tutorial_palette_4amla_1_aFilename, 0, 0)

        render.setColorScale(Vec4(1, 1, 1, 1))
        aspect2d.setColorScale(Vec4(1, 1, 1, 1))

    def setVisGroups(self, visGroups):
        self.cr.sendSetZoneMsg(self.zoneId, visGroups)

    def setChallenge(self, challengeId):
        if challengeId == 0:
            self.completeChallenge()
            return

        challengeInfo = ExperimentChallenges.getChallengeInfo(challengeId)
        self.challengeGui = ExperimentChallengeGUI(*challengeInfo)
        self.challengeGui.setPos(0.92, 0, 0.17)
        self.showChallengeGui()

    def setChallengeCount(self, count):
        if self.challengeGui:
            self.challengeGui.updateProgress(count)

    def completeChallenge(self):
        if self.challengeGui:
            self.challengeGui.fadeOutDestroy()
            self.challengeGui = None

    def showChallengeGui(self):
        if self.challengeGui is None:
            return

        if not self.challengeGui.visible:
            self.challengeGui.fadeIn()
            base.setCellsActive([base.bottomCells[1], base.bottomCells[2]], 0)

    def hideChallengeGui(self):
        if self.challengeGui is None:
            return

        if self.challengeGui.visible:
            self.challengeGui.fadeOut()
            base.setCellsActive([base.bottomCells[1], base.bottomCells[2]], 1)

    def enterIntroduction(self, timestamp):
        pass

    def exitIntroduction(self, timestamp):
        pass

    def enterPhase0(self, timestamp):
        if self.blimp is None:
            self.blimp = ExperimentBlimp()
            self.blimp.reparentTo(render)
            self.blimp.setPosHpr(144, -188, 55, 140, 0, 5)
            self.blimp.startFlying(timestamp)
        self.blimp.request('Phase0', timestamp)

    def exitPhase0(self):
        pass

    def enterPhase1(self, timestamp):
        self.blimp.request('Phase1', timestamp)

    def exitPhase1(self):
        pass

    def enterPhase2(self, timestamp):
        self.blimp.request('Phase2', timestamp)

    def exitPhase2(self):
        pass

    def enterPhase3(self, timestamp):
        self.blimp.request('Phase3', timestamp)

    def exitPhase3(self):
        pass

    def enterCredits(self, timestamp):
        self.cleanupDestruction()

        self.credits = ExperimentCredits()
        self.credits.start()

    def exitCredits(self):
        pass


@magicWord(category=CATEGORY_PROGRAMMER, types=[int])
def blimp(phase):
    if not (0 <= phase <= 3):
        return 'Invalid phase.'
    for event in base.cr.doFindAllInstances(DistributedExperimentEvent):
        event.blimp.request('Phase%d' % phase, globalClockDelta.getRealNetworkTime(bits=32))
        break
    else:
        return "Couldn't find a blimp."
