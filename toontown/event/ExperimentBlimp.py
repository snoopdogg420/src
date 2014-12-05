from direct.actor.Actor import Actor
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Func
from direct.interval.IntervalGlobal import Sequence, Wait
from panda3d.core import NodePath, Texture

from toontown.suit import Suit
from toontown.suit.BossCog import BossCog
from toontown.suit.SuitDNA import SuitDNA


STATIC_SCREEN_INDEX = 0
CHAIRMAN_SCREEN_INDEX = 1
BOSSBOT_SCREEN_INDEX = 2
LAWBOT_SCREEN_INDEX = 3
CASHBOT_SCREEN_INDEX = 4
SELLBOT_SCREEN_INDEX = 5

TELEVISION_TRACK_0 = (
    (STATIC_SCREEN_INDEX, 45), (CHAIRMAN_SCREEN_INDEX, 0.25),
    (STATIC_SCREEN_INDEX, 0.5), (CHAIRMAN_SCREEN_INDEX, 0.1),
    (STATIC_SCREEN_INDEX, 0.1), (CHAIRMAN_SCREEN_INDEX, 0.1)
)
TELEVISION_TRACK_1 = (
    (STATIC_SCREEN_INDEX, 0.1), (SELLBOT_SCREEN_INDEX, 0.1),
    (STATIC_SCREEN_INDEX, 0.1), (BOSSBOT_SCREEN_INDEX, 5),
    (STATIC_SCREEN_INDEX, 0.1), (BOSSBOT_SCREEN_INDEX, 0.1),
    (STATIC_SCREEN_INDEX, 0.1), (LAWBOT_SCREEN_INDEX, 5),
    (STATIC_SCREEN_INDEX, 0.1), (LAWBOT_SCREEN_INDEX, 0.1),
    (STATIC_SCREEN_INDEX, 0.1), (CASHBOT_SCREEN_INDEX, 5),
    (STATIC_SCREEN_INDEX, 0.1), (CASHBOT_SCREEN_INDEX, 0.1),
    (STATIC_SCREEN_INDEX, 0.1), (SELLBOT_SCREEN_INDEX, 5)
)
TELEVISION_TRACK_2 = TELEVISION_TRACK_1
TELEVISION_TRACK_3 = TELEVISION_TRACK_2


class TelevisionScene(NodePath):
    def __init__(self, name):
        NodePath.__init__(self, name)

        self.cameraPosHpr = (0, 0, 0, 0, 0, 0)

    def delete(self):
        NodePath.removeNode(self)

    def setCameraPosHpr(self, x, y, z, h, p, r):
        self.cameraPosHpr = (x, y, z, h, p, r)

    def getCameraPosHpr(self):
        return self.cameraPosHpr


class BossbotScene(TelevisionScene, FSM):
    def __init__(self):
        TelevisionScene.__init__(self, 'BossbotScene')
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

        TelevisionScene.delete(self)

    def enterPhase0(self):
        self.setCameraPosHpr(0, 203.5, 23.5, 0, 354, 0)

    def enterPhase1(self):
        self.setCameraPosHpr(0, 203.5, 23.5, 0, 354, 0)

    def enterPhase2(self):
        self.setCameraPosHpr(0, 203.5, 23.5, 0, 354, 0)


class LawbotScene(TelevisionScene, FSM):
    def __init__(self):
        TelevisionScene.__init__(self, 'LawbotScene')
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

        self.chairs = []
        chairModel = loader.loadModel('phase_11/models/lawbotHQ/LB_chairA.bam')
        for x, y, z, h, p, r in ((-16.5, 3.73, 81.58, 23.2, 0, 0),
                                 (8.5, 3.73, 81.58, 336.8, 0, 0)):
            chair = chairModel.copyTo(self)
            chair.setPosHpr(x, y, z, h, p, r)
            self.chairs.append(chair)
        chairModel.removeNode()

        self.couches = []
        couchModel = loader.loadModel('phase_11/models/lawbotHQ/LB_couchA.bam')
        for x, y, z, h, p, r in ((-16.28, 19.88, 81.58, 23.2, 0, 0),
                                 (8.55, 19.42, 81.58, 333.43, 0, 0)):
            couch = couchModel.copyTo(self)
            couch.setPosHpr(x, y, z, h, p, r)
            self.couches.append(couch)
        couchModel.removeNode()

    def delete(self):
        for couch in self.couches[:]:
            couch.removeNode()
            self.couches.remove(couch)

        for chair in self.chairs[:]:
            chair.removeNode()
            self.chairs.remove(chair)

        if self.boss is not None:
            self.boss.delete()
            self.boss = None

        if self.background is not None:
            self.background.removeNode()
            self.background = None

        TelevisionScene.delete(self)

    def enterPhase0(self):
        self.setCameraPosHpr(-3.84, -29.84, 93.08, 0, 348, 0)

    def enterPhase1(self):
        self.setCameraPosHpr(-3.84, -29.84, 93.08, 0, 348, 0)

    def enterPhase2(self):
        self.setCameraPosHpr(-3.84, -29.84, 93.08, 0, 348, 0)


class CashbotScene(TelevisionScene, FSM):
    def __init__(self):
        TelevisionScene.__init__(self, 'CashbotScene')
        FSM.__init__(self, 'CashbotScene')

        self.background = loader.loadModel('phase_10/models/cogHQ/EndVault.bam')
        self.background.reparentTo(self)

        self.boss = BossCog()
        dna = SuitDNA()
        dna.newBossCog('m')
        self.boss.setDNA(dna)
        self.boss.reparentTo(self)
        self.boss.setPosHpr(21.66, -117.47, 2.92, 228.01, 0, 0)
        self.boss.loop('Bb_neutral')

        self.subordinates = []
        for name, (x, y, z, h, p, r) in (('rb', (33.41, -135.55, 14.68, 251.57, 0, 0)),
                                         ('mb', (38.75, -126.4, 14.68, 210.96, 0, 0))):
            subordinate = Suit.Suit()
            dna = SuitDNA()
            dna.newSuit(name)
            subordinate.setDNA(dna)
            subordinate.nametag.setNametag2d(None)
            subordinate.nametag.setNametag3d(None)
            subordinate.reparentTo(hidden)
            subordinate.setPosHpr(x, y, z, h, p, r)
            self.subordinates.append(subordinate)

    def delete(self):
        for subordinate in self.subordinates[:]:
            subordinate.delete()
            self.subordinates.remove(subordinate)

        if self.boss is not None:
            self.boss.delete()
            self.boss = None

        if self.background is not None:
            self.background.removeNode()
            self.background = None

        TelevisionScene.delete(self)

    def enterPhase0(self):
        self.setCameraPosHpr(48.05, -142.49, 20.16, 48.01, 0, 0)

    def enterPhase1(self):
        self.setCameraPosHpr(48.05, -142.49, 20.16, 48.01, 0, 0)

        for subordinate in self.subordinates:
            subordinate.loop('neutral')
            subordinate.reparentTo(self)

    def enterPhase2(self):
        self.setCameraPosHpr(48.05, -142.49, 20.16, 48.01, 0, 0)

    def defaultExit(self):
        for subordinate in self.subordinates:
            subordinate.reparentTo(hidden)


class SellbotScene(TelevisionScene, FSM):
    def __init__(self):
        TelevisionScene.__init__(self, 'SellbotScene')
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

        self.subordinates = []
        for name, (x, y, z, h, p, r) in (('mh', (-2.76, 16.68, 11.63, 195.95, 0, 0)),
                                         ('ms', (7.18, 14.98, 12.57, 153.43, 0, 0)),
                                         ('tf', (-1.55, 62.22, 15.27, 180, 0, 0))):
            subordinate = Suit.Suit()
            dna = SuitDNA()
            dna.newSuit(name)
            subordinate.setDNA(dna)
            subordinate.nametag.setNametag2d(None)
            subordinate.nametag.setNametag3d(None)
            subordinate.reparentTo(hidden)
            subordinate.setPosHpr(x, y, z, h, p, r)
            self.subordinates.append(subordinate)

    def delete(self):
        for subordinate in self.subordinates[:]:
            subordinate.delete()
            self.subordinates.remove(subordinate)

        if self.boss is not None:
            self.boss.delete()
            self.boss = None

        if self.background is not None:
            self.background.removeNode()
            self.background = None

        TelevisionScene.delete(self)

    def enterPhase0(self):
        self.setCameraPosHpr(0.9, -0.6, 17.72, 354.81, 0, 0)

    def enterPhase1(self):
        self.setCameraPosHpr(0.9, -0.6, 17.72, 354.81, 0, 0)

        for subordinate in self.subordinates:
            subordinate.loop('neutral')
            subordinate.reparentTo(self)

    def enterPhase2(self):
        self.setCameraPosHpr(0.9, -0.6, 17.72, 354.81, 0, 0)

    def defaultExit(self):
        for subordinate in self.subordinates:
            subordinate.reparentTo(hidden)


class ExperimentTelevision(NodePath, FSM):
    def __init__(self):
        NodePath.__init__(self, 'ExperimentTelevision')
        FSM.__init__(self, 'ExperimentTelevision')

        self.model = loader.loadModel('phase_4/models/events/blimp_tv.bam')
        self.model.reparentTo(self)

        self.staticTex = loader.loadTexture('phase_4/maps/blimp_tv_map_01.png')
        self.staticTex.setMinfilter(Texture.FTLinearMipmapLinear)
        self.staticTex.setMagfilter(Texture.FTLinear)

        self.chairmanTex = loader.loadTexture('phase_4/maps/blimp_tv_map_CM.png')
        self.chairmanTex.setMinfilter(Texture.FTLinearMipmapLinear)
        self.chairmanTex.setMagfilter(Texture.FTLinear)

        self.bossbotScene = BossbotScene()
        self.lawbotScene = LawbotScene()
        self.cashbotScene = CashbotScene()
        self.sellbotScene = SellbotScene()

        self.buffer = base.win.makeTextureBuffer('television', 960, 540)
        self.buffer.setSort(-1)

        self.camera = base.makeCamera(self.buffer)

        self.track = None

    def delete(self):
        if self.track is not None:
            self.track.finish()
            self.track = None

        if self.camera is not None:
            self.camera.removeNode()
            self.camera = None

        if self.buffer is not None:
            base.graphicsEngine.removeWindow(self.buffer)
            self.buffer = None

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

        if self.chairmanTex is not None:
            self.chairmanTex.clear()
            self.chairmanTex = None

        if self.staticTex is not None:
            self.staticTex.clear()
            self.staticTex = None

        if self.model is not None:
            self.model.removeNode()
            self.model = None

        NodePath.removeNode(self)

    def enterPhase0(self, timestamp):
        self.setTrack(TELEVISION_TRACK_0, timestamp=timestamp)

    def enterPhase1(self, timestamp):
        self.bossbotScene.request('Phase0')
        self.lawbotScene.request('Phase0')
        self.cashbotScene.request('Phase0')
        self.sellbotScene.request('Phase0')

        self.setTrack(TELEVISION_TRACK_1, timestamp=timestamp)

    def enterPhase2(self, timestamp):
        self.bossbotScene.request('Phase1')
        self.lawbotScene.request('Phase1')
        self.cashbotScene.request('Phase1')
        self.sellbotScene.request('Phase1')

        self.setTrack(TELEVISION_TRACK_2, timestamp=timestamp)

    def enterPhase3(self, timestamp):
        self.bossbotScene.request('Phase2')
        self.lawbotScene.request('Phase2')
        self.cashbotScene.request('Phase2')
        self.sellbotScene.request('Phase2')

        self.setTrack(TELEVISION_TRACK_3, timestamp=timestamp)

    def defaultExit(self):
        if self.track is not None:
            self.track.finish()
            self.track = None

    def setScreen(self, screenIndex):
        tvScreen = self.find('**/tv_screen')
        ts = tvScreen.findTextureStage('*')
        if screenIndex in (STATIC_SCREEN_INDEX, CHAIRMAN_SCREEN_INDEX):
            tvScreen.setTexScale(ts, 1, 1)
            if screenIndex == STATIC_SCREEN_INDEX:
                tvScreen.setTexture(ts, self.staticTex, 1)
            elif screenIndex == CHAIRMAN_SCREEN_INDEX:
                tvScreen.setTexture(ts, self.chairmanTex, 1)
        elif screenIndex in (BOSSBOT_SCREEN_INDEX, LAWBOT_SCREEN_INDEX,
                             CASHBOT_SCREEN_INDEX, SELLBOT_SCREEN_INDEX):
            tvScreen.setTexScale(ts, 1, 1.15)
            if screenIndex == BOSSBOT_SCREEN_INDEX:
                self.camera.reparentTo(self.bossbotScene)
                self.camera.setPosHpr(*self.bossbotScene.getCameraPosHpr())
            elif screenIndex == LAWBOT_SCREEN_INDEX:
                self.camera.reparentTo(self.lawbotScene)
                self.camera.setPosHpr(*self.lawbotScene.getCameraPosHpr())
            elif screenIndex == CASHBOT_SCREEN_INDEX:
                self.camera.reparentTo(self.cashbotScene)
                self.camera.setPosHpr(*self.cashbotScene.getCameraPosHpr())
            elif screenIndex == SELLBOT_SCREEN_INDEX:
                self.camera.reparentTo(self.sellbotScene)
                self.camera.setPosHpr(*self.sellbotScene.getCameraPosHpr())
            tvScreen.setTexture(ts, self.buffer.getTexture(), 1)

    def setTrack(self, track, timestamp=0.0):
        self.track = Sequence()
        for screenIndex, duration in track:
            self.track.append(Func(self.setScreen, screenIndex))
            self.track.append(Wait(duration))
        self.track.loop(globalClockDelta.localElapsedTime(timestamp, bits=32))


class ExperimentBlimp(Actor, FSM):
    def __init__(self):
        Actor.__init__(self, None, None, None, flattenable=0, setFinal=1)
        FSM.__init__(self, 'ExperimentBlimp')

        self.loadModel('phase_4/models/events/blimp_mod.bam')
        self.loadAnims({'flying': 'phase_4/models/events/blimp_chan_flying.bam'})

        self.television = ExperimentTelevision()
        self.television.reparentTo(self)

        self.flyTrack = Sequence(
            self.hprInterval(3.5, (140, 0, -5), blendType='easeInOut'),
            self.hprInterval(3.5, (140, 0, 5), blendType='easeInOut')
        )

    def cleanup(self):
        if self.flyTrack is not None:
            self.flyTrack.finish()
            self.flyTrack = None

        if self.television is not None:
            self.television.delete()
            self.television = None

        Actor.cleanup(self)

    def enterPhase0(self, timestamp):
        self.television.request('Phase0', timestamp)

    def enterPhase1(self, timestamp):
        self.television.request('Phase1', timestamp)

    def enterPhase2(self, timestamp):
        self.television.request('Phase2', timestamp)

    def enterPhase3(self, timestamp):
        self.television.request('Phase3', timestamp)

    def startFlying(self, timestamp):
        self.flyTrack.loop(globalClockDelta.localElapsedTime(timestamp, bits=32))
        self.loop('flying')

    def stopFlying(self):
        self.stop()
        self.flyTrack.finish()
