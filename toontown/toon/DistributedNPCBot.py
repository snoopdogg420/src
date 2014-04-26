from DistributedNPCToonBase import *
from direct.distributed import DistributedNode
import Toon
import ToonDNA

class DistributedNPCBot(DistributedNode.DistributedNode):

    NumBots = 0

    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        self.toon = None

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)
        self.toon = Toon.Toon()
        DistributedNPCBot.NumBots += 1
        self.toon.setName('Bot #%d' % DistributedNPCBot.NumBots)

    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        DistributedNPCToonBase.disable(self)

    def setDNAString(self, dnaString):
        if dnaString == self.dnaString:
            return None
        dna = ToonDNA.ToonDNA(dnaString)
        self.dnaString = dna.makeNetString()
        self.toon.setDNA(self.dnaString)
        self.toon.reparentTo(render)
        self.toon.nametag.manage(base.marginManager)
        self.toon.loop('neutral')
        self.toon.initializeDropShadow()
        self.toon.startBlink()
        self.toon.startLookAround()
        self.toon.initializeBodyCollisions('bodyCollisions-%d' % self.doId)