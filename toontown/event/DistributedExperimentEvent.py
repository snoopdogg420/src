from pandac.PandaModules import Vec4
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.actor.Actor import Actor
from toontown.event.DistributedEvent import DistributedEvent
from toontown.hood import ZoneUtil
from toontown.dna.DNAStorage import DNAStorage
from toontown.dna.DNAParser import loadDNAFileAI
import time


class DistributedExperimentEvent(DistributedEvent):
    notify = directNotify.newCategory('DistributedExperimentEvent')

    def __init__(self, cr):
        DistributedEvent.__init__(self, cr)

        self.introMusic = base.loadMusic('phase_4/audio/bgm/TE_battle_intro.ogg')
        self.music = base.loadMusic('phase_4/audio/bgm/TE_battle.ogg')
        self.musicSequence = None

        self.blimp = None

    def start(self):
        taskMgr.remove('TT-birds')

        base.musicManager.stopAllSounds()
        base.lockMusic()

        self.musicSequence = Sequence(
            Func(base.playMusic, self.introMusic, looping=0, volume=1, playLocked=True),
            Wait(self.introMusic.length()),
            Func(base.playMusic, self.music, looping=1, volume=1, playLocked=True))
        self.musicSequence.start()

        self.cr.playGame.hood.startSpookySky()
        render.setColorScale(Vec4(0.40, 0.40, 0.60, 1))
        aspect2d.setColorScale(Vec4(0.40, 0.40, 0.60, 1))

    def delete(self):
        DistributedEvent.delete(self)

        self.musicSequence.finish()
        self.musicSequence = None

        self.blimp.cleanup()

        base.musicManager.stopAllSounds()
        base.unlockMusic()

        self.cr.playGame.hood.startSky()
        render.setColorScale(Vec4(1, 1, 1, 1))
        aspect2d.setColorScale(Vec4(1, 1, 1, 1))

    def setVisGroups(self, visGroups):
        self.cr.sendSetZoneMsg(self.zoneId, visGroups)

    def createBlimp(self, timestamp):
        # TODO: Make the blimp fly around the playground
        self.blimp = Actor(loader.loadModel('phase_4/models/events/blimp_mod.bam'))
        self.blimp.loadAnims({'flying': 'phase_4/models/events/blimp_chan_flying.bam'})
        self.blimp.reparentTo(render)
        self.blimp.loop('flying')
        self.blimp.setPos(144, -188, 55)
        self.blimp.setHpr(140, 0, 5)
