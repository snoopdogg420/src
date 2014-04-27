from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons


class MMHoodAI(HoodAI):
    HOOD = ToontownGlobals.MinniesMelodyland
    
    def __init__(self, air, streets):
        HoodAI.__init__(self, air, streets)
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        self.spawnObjects()
