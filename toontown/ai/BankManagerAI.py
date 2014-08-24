from direct.fsm.FSM import FSM
from toontown.toonbase import ToontownGlobals

class OperationFSM(FSM):

    def __init__(self, air, bankMgr):
        FSM.__init__(self, 'OperationFSM')
        self.air = air
        self.bankMgr = bankMgr

    def enterOff(self):
        if self.target:
            del self.bankMgr.avId2fsm[self.target]

class BankRetrieveFSM(OperationFSM):

    def enterStart(self, avId, DISLid):
        self.target = avId
        self.DISLid = DISLid

        self.air.dbInterface.queryObject(
            self.air.dbId, self.DISLid, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass == self.air.dclassesByName['AccountAI']:
            money = fields['MONEY']
            av = self.air.doId2do.get(self.target)
            if not av:
                self.demand('Off')
                return

            av.b_setBankMoney(money)
            self.demand('Off')

    def enterOff(self):
        messenger.send('bankDone-%s' % self.target)
        OperationFSM.enterOff(self)

class BankUpdateFSM(OperationFSM):

    def enterStart(self, avId, DISLid, money):
        self.target = avId

        money = min(money, ToontownGlobals.MaxBankMoney)
        if money < 0:
            self.demand('Off')
            return

        self.air.dbInterface.updateObject(
            self.air.dbId,
            DISLid,
            self.air.dclassesByName['AccountAI'],
            {'MONEY': money})

        av = self.air.doId2do.get(self.target)
        if not av:
            self.demand('Off')
            return

        av.b_setBankMoney(money)
        self.demand('Off')

class BankManagerAI:

    def __init__(self, air):
        self.air = air
        self.avId2fsm = {}

    def performFSM(self, target, fsmClass, *args):
        self.avId2fsm[target] = fsmClass(self.air, self)
        self.avId2fsm[target].request('Start', *args)

    def setMoney(self, avId, money):
        av = self.air.doId2do.get(avId)

        if not av:
            return

        DISLid = av.getDISLid()
        self.performFSM(avId, BankUpdateFSM, avId, DISLid, money)

    def getMoney(self, avId):
        av = self.air.doId2do.get(avId)

        if not av:
            return

        DISLid = av.getDISLid()
        self.performFSM(avId, BankRetrieveFSM, avId, DISLid)
        return 'bankDone-%s' % avId
