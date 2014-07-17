import anydbm
import base64
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.distributed.MsgTypes import STATESERVER_OBJECT_GET_ZONE_OBJECTS
from direct.fsm.FSM import FSM
import hashlib
import hmac
import json
from otp.ai.MagicWordGlobal import *
from pandac.PandaModules import *
import time
from toontown.makeatoon.NameGenerator import NameGenerator
from toontown.toon.ToonDNA import ToonDNA
import urllib2
from toontown.toonbase import TTLocalizer

class SystemServicesManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('SystemServicesManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

    def gameWhisper(self, msg, channels):
        system = simbase.air.dclassesByName['SystemServicesManagerUD']
        channel = channels[0]
        print 'Sending one to: %s' % channel
        dg = system.aiFormatUpdate('gameWhisper', 4821, 4821,
                                                channel,
                                                [msg, channels])
        simbase.air.send(dg)
