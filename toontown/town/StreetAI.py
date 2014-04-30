from toontown.dna.DNASpawnerAI import DNASpawnerAI
from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI

from toontown.toonbase import ToontownGlobals
from direct.directnotify.DirectNotifyGlobal import *

class StreetAI:
    """
    AI-side representation of everything in a single street.

    One subclass of this class exists for every neighborhood in the game.
    StreetAIs are responsible for spawning all SuitPlanners,ponds, and other
    street objects, etc.
    """

    notify = directNotify.newCategory('StreetAI')
    notify.setInfo(True)
    
    def __init__(self, air, zoneId):
        self.air = air
        self.zoneId = zoneId

        self.spawnObjects()
    
    def spawnObjects(self):
        filename = self.air.genDNAFileName(self.zoneId)
        self.notify.info('Reading DNA file... ' + filename)
        DNASpawnerAI().spawnObjects(filename, self.zoneId)
