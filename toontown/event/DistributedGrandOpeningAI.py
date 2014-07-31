from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM


class DistributedGrandOpeningAI(DistributedObjectAI, FSM):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedGrandOpeningAI')
