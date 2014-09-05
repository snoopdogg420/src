from toontown.safezone import SafeZoneLoader
from toontown.safezone import TTPlayground
from direct.actor.Actor import Actor

class TTSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TTPlayground.TTPlayground
        self.musicFile = 'phase_4/audio/bgm/TC_nbrhood.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_4/dna/toontown_central_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_4/dna/storage_TT_sz.pdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg',
                                            'phase_4/audio/sfx/SZ_TC_bird2.ogg',
                                            'phase_4/audio/sfx/SZ_TC_bird3.ogg'])
        bank = self.geom.find('**/*toon_landmark_TT_bank_DNARoot')
        doorTrigger = bank.find('**/door_trigger*')
        doorTrigger.setY(doorTrigger.getY() - 1.5)

        self.camModel = loader.loadModel('phase_4/models/events/SillyMeterCrate_mod.bam')

        self.cam1 = Actor(self.camModel)
        self.cam1.loadAnims({'neutral': 'phase_4/models/events/SillyMeterCrate_chan_open.bam'})
        self.cam1.reparentTo(render)
        self.cam1.loop('neutral')
        self.cam1.setPos(79.953,2,4)
        self.cam1.setHpr(-447.775,0,0)
        self.cam1.setScale(0.5)

        self.ropes = render.attachNewNode('ball')

        self.ropesd = loader.loadModel("phase_4/models/modules/tt_m_ara_int_ropes.bam")
        self.ropesd.reparentTo(self.geom) # The geom is created by the dna parser
        self.ropesd.setPos(80,1,4.025)
        self.ropesd.setScale(1.3)
        self.ropesd.node().addSolid(CollisionSphere(80, 1, 0, 35))

        self.constructionSite.attachNewNode(CollisionNode('constructionSiteBlocker'))

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.birdSound

