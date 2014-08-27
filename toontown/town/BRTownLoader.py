from toontown.battle import BattleParticles
from toontown.suit import Suit
from toontown.town import BRStreet
from toontown.town import TownLoader


class BRTownLoader(TownLoader.TownLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = BRStreet.BRStreet
        self.musicFile = 'phase_8/audio/bgm/TB_SZ.ogg'
        self.activityMusicFile = 'phase_8/audio/bgm/TB_SZ_activity.ogg'
        self.townStorageDNAFile = 'phase_8/dna/storage_BR_town.pdna'

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(3)
        dnaFile = 'phase_8/dna/the_burrrgh_' + str(self.canonicalBranchZone) + '.pdna'
        self.createHood(dnaFile)
        self.windSound = map(base.loadSfx, ['phase_8/audio/sfx/SZ_TB_wind_1.ogg',
                                            'phase_8/audio/sfx/SZ_TB_wind_2.ogg',
                                            'phase_8/audio/sfx/SZ_TB_wind_3.ogg'])
        self.snow = BattleParticles.loadParticleFile('snowdisk.ptf')
        self.snow.setPos(0, 0, 5)
        self.snowRender = self.geom.attachNewNode('snowRender')
        self.snowRender.setDepthWrite(0)
        self.snowRender.setBin('fixed', 1)

    def unload(self):
        TownLoader.TownLoader.unload(self)
        Suit.unloadSuits(3)
        del self.windSound
        del self.snow
        del self.snowRender

    def enter(self, requestStatus):
        TownLoader.TownLoader.enter(self, requestStatus)
        self.snow.start(camera, self.snowRender)

    def exit(self):
        TownLoader.TownLoader.exit(self)
        self.snow.cleanup()
        self.snowRender.removeNode()
