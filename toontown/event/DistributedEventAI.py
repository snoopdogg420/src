from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM
from direct.showbase.PythonUtil import Functor

from otp.ai.MagicWordGlobal import *


class DistributedEventAI(DistributedObjectAI, FSM):
    notify = directNotify.newCategory('DistributedEventAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, self.__class__.__name__)

        self.participants = []

    def start(self):
        self.sendUpdate('start', [])

    def messageParticipants(self, message):
        self.sendUpdate('messageParticipants', [message])

    def joinEvent(self, avId):
        if avId in self.participants:
            return

        av = self.air.doId2do[avId]
        av.currentEvent = self
        self.participants.append(avId)

    def leaveEvent(self, avId):
        if avId not in self.participants:
            return

        av = self.air.doId2do[avId]
        av.currentEvent = None
        self.participants.remove(avId)

    def toonChangedZone(self, avId, zoneId):
        pass

    def setState(self, state):
        self.request(state)

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime(bits=32)])

    def b_setState(self, state):
        self.setState(state)
        self.d_setState(state)

    def getState(self):
        return self.state

@magicWord(category=CATEGORY_PROGRAMMER, types=[str, str])
def event(command, state):
    invoker = spellbook.getInvoker()
    event = None
    for do in simbase.air.doId2do.values():
        if isinstance(do, DistributedEventAI):
            if invoker.doId in do.participants:
                event = do
                break
    if event is None:
        return "You aren't in an event!"
    if command == 'state':
        event.b_setState(state)
        return 'Setting event to state %s.' % state
    else:
        return 'Unknown command %s.' % command

