from direct.actor.Actor import Actor
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Sequence, LerpHprInterval
from panda3d.core import Vec3


class BossbotScene:
    pass


class LawbotScene:
    pass


class CashbotScene:
    pass


class SellbotScene:
    pass


class ExperimentBlimp(Actor, FSM):
    notify = directNotify.newCategory('ExperimentBlimp')

    def __init__(self, other=None):
        Actor.__init__(self, None, None, other, flattenable=0, setFinal=1)
        FSM.__init__(self, 'ExperimentBlimp')

        self.loadModel('phase_4/models/events/blimp_mod.bam')
        self.loadAnims({'flying': 'phase_4/models/events/blimp_chan_flying.bam'})

        self.tv = loader.loadModel('phase_4/models/events/blimp_tv.bam')
        self.tv.reparentTo(self)

        self.flyTrack = Sequence(
            LerpHprInterval(self, 3.5, Vec3(140, 0, 5),
                            startHpr=Vec3(140, 0, -5), blendType='easeInOut',
                            fluid=1),
            LerpHprInterval(self, 3.5, Vec3(140, 0, -5),
                            startHpr=Vec3(140, 0, 5), blendType='easeInOut',
                            fluid=1)
        )

    def cleanup(self):
        if self.flyTrack is not None:
            self.stopFlying()
            self.flyTrack = None

        if self.tv is not None:
            self.tv.removeNode()
            self.tv = None

        Actor.cleanup(self)

    def enterPhase0(self):
        """
        Phase 0 describes the blimp when it is mostly displaying a static image
        on its monitor. On a random interval it will flash an image of the
        Chairman.
        """
        pass

    def enterPhase1(self):
        """
        Phase 1 describes the blimp when it is constantly flickering between
        the first four boss Cogs (the Sellbot V.P., the Cashbot C.F.O., the
        Lawbot C.J., and the Bossbot C.E.O.). They will be standing still in a
        neutral animation inside of their respective headquarters.
        """
        pass

    def enterPhase2(self):
        """
        Phase 2 describes the blimp in the same state as phase 1, however, the
        boss Cogs' subordinates have joined in on the spectating.
        """
        pass

    def enterPhase3(self):
        """
        Phase 3 describes the blimp in the same state as phase 2, however, the
        both the boss Cogs, and their subordinates are cheering over the
        destruction of Toontown Central.
        """
        pass

    def startFlying(self):
        self.loop('flying')
        self.flyTrack.loop(globalClockDelta.localElapsedTime(0))

    def stopFlying(self):
        self.flyTrack.finish()
        self.stop()
