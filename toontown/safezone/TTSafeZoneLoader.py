from toontown.safezone import SafeZoneLoader
from toontown.safezone import TTPlayground

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

        SillyMeterCrate = loader.loadModel("phase_4/models/events/SillyMeterCrate.bam")
        SillyMeterCrate.reparentTo(self.geom) # The geom is created by the dna parser
        SillyMeterCrate.setPos(79.953,2,4)
        SillyMeterCrate.setHpr(-447.775,0,0)
        SillyMeterCrate.setScale(0.5)

        ropes = loader.loadModel("phase_4/models/modules/tt_m_ara_int_ropes.bam")
        ropes.reparentTo(self.geom) # The geom is created by the dna parser
        ropes.setPos(80,0,4.025)
        ropes.setHpr(-447.775,0,0)
        ropes.setScale(1)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.birdSound

