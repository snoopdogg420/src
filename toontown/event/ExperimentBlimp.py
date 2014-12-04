from direct.actor.Actor import Actor
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Func
from direct.interval.IntervalGlobal import Sequence, LerpHprInterval, Wait
from panda3d.core import NodePath, Vec3, Texture

from toontown.suit.BossCog import BossCog
from toontown.suit.SuitDNA import SuitDNA


STATIC_SCREEN_INDEX = 0
CHAIRMAN_SCREEN_INDEX = 1
BOSSBOT_SCREEN_INDEX = 2
LAWBOT_SCREEN_INDEX = 3
CASHBOT_SCREEN_INDEX = 4
SELLBOT_SCREEN_INDEX = 5


class BossbotScene(NodePath, FSM):
    def __init__(self):
        NodePath.__init__(self, 'BossbotScene')
        FSM.__init__(self, 'BossbotScene')

        self.background = loader.loadModel('phase_12/models/bossbotHQ/BanquetInterior_1.bam')
        self.background.reparentTo(self)

        self.boss = BossCog()
        dna = SuitDNA()
        dna.newBossCog('c')
        self.boss.setDNA(dna)
        self.boss.reparentTo(self)
        self.boss.setPosHpr(0, 236.89, 0, 180, 0, 0)
        self.boss.loop('Bb_neutral')

    def delete(self):
        if self.boss is not None:
            self.boss.delete()
            self.boss = None

        if self.background is not None:
            self.background.removeNode()
            self.background = None

        NodePath.removeNode(self)

    def enterPhase0(self):
        pass

    def enterPhase1(self):
        pass

    def enterPhase2(self):
        pass


class LawbotScene(NodePath, FSM):
    def __init__(self):
        NodePath.__init__(self, 'LawbotScene')
        FSM.__init__(self, 'LawbotScene')

        self.background = loader.loadModel('phase_11/models/lawbotHQ/LawbotCourtroom3.bam')
        self.background.reparentTo(self)

        self.boss = BossCog()
        dna = SuitDNA()
        dna.newBossCog('l')
        self.boss.setDNA(dna)
        self.boss.reparentTo(self)
        self.boss.setPosHpr(-3.7, 0, 71.24, 180, 0, 0)
        self.boss.loop('Bb_neutral')

        self.chair0 = loader.loadModel('phase_11/models/lawbotHQ/LB_chairA.bam')
        self.chair0.setPosHpr(-16.5, 3.73, 81.58, 23.2, 0, 0)
        self.chair0.reparentTo(self)

        self.chair1 = loader.loadModel('phase_11/models/lawbotHQ/LB_chairA.bam')
        self.chair1.setPosHpr(8.5, 3.73, 81.58, 336.8, 0, 0)
        self.chair1.reparentTo(self)

        self.chair2 = loader.loadModel('phase_11/models/lawbotHQ/LB_couchA.bam')
        self.chair2.setPosHpr(-16.28, 19.88, 81.58, 23.2, 0, 0)
        self.chair2.reparentTo(self)

        self.chair3 = loader.loadModel('phase_11/models/lawbotHQ/LB_couchA.bam')
        self.chair3.setPosHpr(8.55, 19.42, 81.58, 333.43, 0, 0)
        self.chair3.reparentTo(self)

    def delete(self):
        if self.chair3 is not None:
            self.chair3.removeNode()
            self.chair3 = None

        if self.chair2 is not None:
            self.chair2.removeNode()
            self.chair2 = None

        if self.chair1 is not None:
            self.chair1.removeNode()
            self.chair1 = None

        if self.chair0 is not None:
            self.chair0.removeNode()
            self.chair0 = None

        if self.boss is not None:
            self.boss.delete()
            self.boss = None

        if self.background is not None:
            self.background.removeNode()
            self.background = None

        NodePath.removeNode(self)

    def enterPhase0(self):
        pass

    def enterPhase1(self):
        pass

    def enterPhase2(self):
        pass


class CashbotScene(NodePath, FSM):
    def __init__(self):
        NodePath.__init__(self, 'CashbotScene')
        FSM.__init__(self, 'CashbotScene')

        self.background = loader.loadModel('phase_10/models/cogHQ/EndVault.bam')
        self.background.reparentTo(self)

        self.boss = BossCog()
        dna = SuitDNA()
        dna.newBossCog('m')
        self.boss.setDNA(dna)
        self.boss.reparentTo(self)
        self.boss.setPosHpr(25.03, -117.47, 2.92, 210.96, 0, 0)
        self.boss.loop('Bb_neutral')

    def delete(self):
        if self.boss is not None:
            self.boss.delete()
            self.boss = None

        if self.background is not None:
            self.background.removeNode()
            self.background = None

        NodePath.removeNode(self)

    def enterPhase0(self):
        pass

    def enterPhase1(self):
        pass

    def enterPhase2(self):
        pass


class SellbotScene(NodePath, FSM):
    def __init__(self):
        NodePath.__init__(self, 'SellbotScene')
        FSM.__init__(self, 'SellbotScene')

        self.background = loader.loadModel('phase_9/models/cogHQ/SellbotHQLobby.bam')
        self.background.reparentTo(self)

        self.boss = BossCog()
        dna = SuitDNA()
        dna.newBossCog('s')
        self.boss.setDNA(dna)
        self.boss.reparentTo(self)
        self.boss.setPosHpr(6.36, 34.23, 0, 169.7, 0, 0)
        self.boss.loop('Bb_neutral')

    def delete(self):
        if self.boss is not None:
            self.boss.delete()
            self.boss = None

        if self.background is not None:
            self.background.removeNode()
            self.background = None

        NodePath.removeNode(self)

    def enterPhase0(self):
        pass

    def enterPhase1(self):
        pass

    def enterPhase2(self):
        pass


class ExperimentBlimp(Actor, FSM):
    notify = directNotify.newCategory('ExperimentBlimp')

    def __init__(self):
        Actor.__init__(self, None, None, None, flattenable=0, setFinal=1)
        FSM.__init__(self, 'ExperimentBlimp')

        self.bossbotScene = BossbotScene()
        self.lawbotScene = LawbotScene()
        self.cashbotScene = CashbotScene()
        self.sellbotScene = SellbotScene()

        self.loadModel('phase_4/models/events/blimp_mod.bam')
        self.loadAnims({'flying': 'phase_4/models/events/blimp_chan_flying.bam'})

        self.tv = loader.loadModel('phase_4/models/events/blimp_tv.bam')
        self.tv.reparentTo(self)

        self.staticScreenTex = loader.loadTexture('phase_4/maps/blimp_tv_map_01.png')
        self.staticScreenTex.setMinfilter(Texture.FTLinearMipmapLinear)
        self.staticScreenTex.setMagfilter(Texture.FTLinear)

        self.chairmanScreenTex = loader.loadTexture('phase_4/maps/blimp_tv_map_CM.png')
        self.chairmanScreenTex.setMinfilter(Texture.FTLinearMipmapLinear)
        self.chairmanScreenTex.setMagfilter(Texture.FTLinear)

        self.buffer = base.win.makeTextureBuffer('tv', 960, 540)
        self.buffer.setSort(-100)

        self.camera = base.makeCamera(self.buffer)

        self.tvIval = None

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

        if self.tvIval is not None:
            self.tvIval.finish()
            self.tvIval = None

        if self.camera is not None:
            self.camera.removeNode()
            self.camera = None

        if self.buffer is not None:
            base.graphicsEngine.removeWindow(self.buffer)
            self.buffer = None

        if self.chairmanScreenTex is not None:
            self.chairmanScreenTex.clear()
            self.chairmanScreenTex = None

        if self.staticScreenTex is not None:
            self.staticScreenTex.clear()
            self.staticScreenTex = None

        if self.tv is not None:
            self.tv.removeNode()
            self.tv = None

        if self.sellbotScene is not None:
            self.sellbotScene.delete()
            self.sellbotScene = None

        if self.cashbotScene is not None:
            self.cashbotScene.delete()
            self.cashbotScene = None

        if self.lawbotScene is not None:
            self.lawbotScene.delete()
            self.lawbotScene = None

        if self.bossbotScene is not None:
            self.bossbotScene.delete()
            self.bossbotScene = None

        Actor.cleanup(self)

    def enterPhase0(self, timestamp):
        """
        Phase 0 describes the blimp when it is almost always displaying a
        static image on its monitor. It will, however, flash a drawing of the
        Chairman every 45 seconds.
        """
        self.tvIval = Sequence(
            Wait(45),
            Func(self.setScreen, CHAIRMAN_SCREEN_INDEX),
            Wait(0.25),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.5),
            Func(self.setScreen, CHAIRMAN_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, CHAIRMAN_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, STATIC_SCREEN_INDEX)
        )
        self.tvIval.loop(globalClockDelta.localElapsedTime(timestamp, bits=32))

    def exitPhase0(self):
        if self.tvIval is not None:
            self.tvIval.finish()
            self.tvIval = None

    def enterPhase1(self, timestamp):
        """
        Phase 1 describes the blimp when it is constantly flickering between
        the first four boss Cogs (the Sellbot V.P., the Cashbot C.F.O., the
        Lawbot C.J., and the Bossbot C.E.O.). They will be standing still in a
        neutral animation inside of their respective headquarters.
        """
        self.bossbotScene.request('Phase0')
        self.lawbotScene.request('Phase0')
        self.cashbotScene.request('Phase0')
        self.sellbotScene.request('Phase0')
        self.tvIval = Sequence(
            Func(self.setScreen, BOSSBOT_SCREEN_INDEX),
            Wait(5),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, BOSSBOT_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, LAWBOT_SCREEN_INDEX),
            Wait(5),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, LAWBOT_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, CASHBOT_SCREEN_INDEX),
            Wait(5),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, CASHBOT_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, SELLBOT_SCREEN_INDEX),
            Wait(5),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, SELLBOT_SCREEN_INDEX),
            Wait(0.1),
            Func(self.setScreen, STATIC_SCREEN_INDEX),
            Wait(0.1)
        )
        self.tvIval.loop(globalClockDelta.localElapsedTime(timestamp, bits=32))

    def exitPhase1(self):
        if self.tvIval is not None:
            self.tvIval.finish()
            self.tvIval = None

    def enterPhase2(self, timestamp):
        """
        Phase 2 describes the blimp in the same state as phase 1, however, the
        boss Cogs' subordinates have joined in on the spectating.
        """
        self.bossbotScene.request('Phase1')
        self.lawbotScene.request('Phase1')
        self.cashbotScene.request('Phase1')
        self.sellbotScene.request('Phase1')

    def enterPhase3(self, timestamp):
        """
        Phase 3 describes the blimp in the same state as phase 2, however, the
        both the boss Cogs, and their subordinates are cheering over the
        destruction of Toontown Central.
        """
        self.bossbotScene.request('Phase2')
        self.lawbotScene.request('Phase2')
        self.cashbotScene.request('Phase2')
        self.sellbotScene.request('Phase2')

    def startFlying(self, timestamp):
        self.loop('flying')
        self.flyTrack.loop(globalClockDelta.localElapsedTime(timestamp, bits=32))

    def stopFlying(self):
        self.flyTrack.finish()
        self.stop()

    def setScreen(self, screenIndex):
        tvScreen = self.tv.find('**/tv_screen')
        ts = tvScreen.findTextureStage('*')
        if screenIndex == STATIC_SCREEN_INDEX:
            tvScreen.setTexScale(ts, 1, 1)
            tvScreen.setTexture(ts, self.staticScreenTex, 1)
        elif screenIndex == CHAIRMAN_SCREEN_INDEX:
            tvScreen.setTexScale(ts, 1, 1)
            tvScreen.setTexture(ts, self.chairmanScreenTex, 1)
        elif screenIndex == BOSSBOT_SCREEN_INDEX:
            tvScreen.setTexScale(ts, 1, 1.15)
            self.camera.reparentTo(self.bossbotScene)
            self.camera.setPosHpr(0, 203.5, 23.5, 0, 354, 0)
            tvScreen.setTexture(ts, self.buffer.getTexture(), 1)
        elif screenIndex == LAWBOT_SCREEN_INDEX:
            tvScreen.setTexScale(ts, 1, 1.15)
            self.camera.reparentTo(self.lawbotScene)
            self.camera.setPosHpr(-3.84, -29.84, 93.08, 0, 348, 0)
            tvScreen.setTexture(ts, self.buffer.getTexture(), 1)
        elif screenIndex == CASHBOT_SCREEN_INDEX:
            tvScreen.setTexScale(ts, 1, 1.15)
            self.camera.reparentTo(self.cashbotScene)
            self.camera.setPosHpr(48.05, -142.49, 20.16, 48.01, 0, 0)
            tvScreen.setTexture(ts, self.buffer.getTexture(), 1)
        elif screenIndex == SELLBOT_SCREEN_INDEX:
            tvScreen.setTexScale(ts, 1, 1.15)
            self.camera.reparentTo(self.sellbotScene)
            self.camera.setPosHpr(0.9, -0.6, 17.72, 354.81, 0, 0)
            tvScreen.setTexture(ts, self.buffer.getTexture(), 1)
