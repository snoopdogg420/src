from toontown.toonbase import ToontownGlobals
from HoodAI import HoodAI
from toontown.dna.DNAParser import DNAStorage
from toontown.toon import NPCToons

class DLHoodAI(HoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland
    
    def __init__(self, air, streets):
        HoodAI.__init__(self, air, streets)    
    
    def createSafeZone(self):
        HoodAI.createSafeZone(self)
        
        self.spawnObjects()
