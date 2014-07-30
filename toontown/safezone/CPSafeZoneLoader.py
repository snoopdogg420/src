from pandac.PandaModules import *
import SafeZoneLoader
import CPPlayground

class CPSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = CPPlayground.CPPlayground
        self.musicFile = 'phase_6/audio/bgm/CP_nbrhood.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/CP_SZ.ogg'
        self.dnaFile = 'phase_6/dna/chestnut_park_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_CP_sz.dna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.SafeZoneLoader.exit(self)
