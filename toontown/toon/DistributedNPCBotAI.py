from otp.ai.AIBaseGlobal import *
from direct.distributed import DistributedNode

class DistributedNPCBotAI(DistributedNodeAI):

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.air = air

    def setDNAString(self, dnaString):
        self.dnaString = dnaString

    def getDNAString(self):
        return self.dnaString

    def d_setDNAString(self, dnaString):
        self.sendUpdate('setDNAString', [dnaString])

    def b_setDNAString(self, dnaString):
        self.setDNAString(dnaString)
        self.d_setDNAString(dnaString)