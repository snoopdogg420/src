from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from otp.ai.MagicWordGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *

class MagicWordManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("MagicWordManagerUD")

    def sendMagicWord(self, word, targetId):
        pass
