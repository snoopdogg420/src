from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpHprInterval
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import Vec3
from pandac.PandaModules import Vec4

from toontown.event import ExperimentEventObjectives
from toontown.event.DistributedEvent import DistributedEvent
from toontown.event.ExperimentEventObjectiveGUI import ExperimentEventObjectiveGUI


class DistributedExperimentEvent(DistributedEvent):
    notify = directNotify.newCategory('DistributedExperimentEvent')

    def __init__(self, cr):
        DistributedEvent.__init__(self, cr)

        self.introMusic = base.loadMusic('phase_4/audio/bgm/TE_battle_intro.ogg')
        self.music = base.loadMusic('phase_4/audio/bgm/TE_battle.ogg')
        self.musicSequence = None

        self.objectiveGui = None

        self.blimp = None
        self.blimpTrack = None

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

        if self.blimp is not None:
            self.blimp.cleanup()
            self.blimp = None

        if self.blimpTrack is not None:
            self.blimpTrack.finish()
            self.blimpTrack = None

        base.musicManager.stopAllSounds()
        base.unlockMusic()

        self.cr.playGame.hood.startSky()
        render.setColorScale(Vec4(1, 1, 1, 1))
        aspect2d.setColorScale(Vec4(1, 1, 1, 1))

    def setVisGroups(self, visGroups):
        self.cr.sendSetZoneMsg(self.zoneId, visGroups)

    def createBlimp(self, timestamp):
        self.blimp = Actor(loader.loadModel('phase_4/models/events/blimp_mod.bam'))
        self.blimp.loadAnims({'flying': 'phase_4/models/events/blimp_chan_flying.bam'})
        self.blimp.reparentTo(render)
        self.blimp.loop('flying')
        self.blimp.setPos(144, -188, 55)
        self.blimp.setHpr(140, 0, 5)

        self.blimpTrack = Sequence(
            LerpHprInterval(self.blimp, 3.5, Vec3(140, 0, 5),
                            startHpr=Vec3(140, 0, -5), blendType='easeInOut',
                            fluid=1),
            LerpHprInterval(self.blimp, 3.5, Vec3(140, 0, -5),
                            startHpr=Vec3(140, 0, 5), blendType='easeInOut',
                            fluid=1)
        )
        self.blimpTrack.loop()

    def setObjective(self, objectiveId):
        if objectiveId == 0:
            self.completeObjective()
            return

        objectiveInfo = ExperimentEventObjectives.getObjectiveInfo(objectiveId)
        self.objectiveGui = ExperimentEventObjectiveGUI(*objectiveInfo)
        self.objectiveGui.setPos(0, 0, 0.8)
        self.objectiveGui.fadeIn()

    def setObjectiveCount(self, count):
        if self.objectiveGui:
            self.objectiveGui.updateProgress(count)

    def completeObjective(self):
        if self.objectiveGui:
            self.objectiveGui.fadeOutDestroy()
            self.objectiveGui = None
