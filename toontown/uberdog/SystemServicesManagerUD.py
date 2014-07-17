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

    def systemMessage(self, msg, channel):
        system = simbase.air.dclassesByName['SystemServicesManagerUD']
        dg = system.aiFormatUpdate(
         'systemMessage', 4821, 4821, channel, [msg, channel])
        simbase.air.send(dg)
