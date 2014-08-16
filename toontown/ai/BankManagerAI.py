from direct.fsm.FSM import FSM

class OperationFSM(FSM):

    def __init__(self, air, bankMgr):
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
            self.demand('Off', money)

    def enterOff(self, result):
        messenger.send('bankDone-%s' % self.target, [result])
        OperationFSM.enterOff(self)

class BankAddFSM(OperationFSM):

    def enterStart(self, avId, DISLid, money):
        self.target = avId
        self.DISLid = DISLid
        self.money = money

        self.air.dbInterface.queryObject(
            self.air.dbId, self.DISLid, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass == self.air.dclassesByName['AccountAI']:
            money = fields['MONEY']
            self.demand('Retrieved', money)

    def enterRetrieved(self, result):
        self.air.dbInterface.updateObject(
            self.air.dbId,
            self.DISLid,
            self.air.dclassesByName['AccountAI'],
            {'MONEY': result + self.money})
        av = self.air.doId2do.get(self.target)
        if not av:
            self.demand('Off')
            return

        av.b_setBankMoney(result + self.money)
        self.demand('Off')

class BankTakeFSM(OperationFSM):

    def enterStart(self, avId, DISLid, money):
        self.target = avId
        self.DISLid = DISLid
        self.money = money

        self.air.dbInterface.queryObject(
            self.air.dbId, self.DISLid, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass == self.air.dclassesByName['AccountAI']:
            money = fields['MONEY']
            self.demand('Retrieved', money)

    def enterRetrieved(self, result):
        self.air.dbInterface.updateObject(
            self.air.dbId,
            self.DISLid,
            self.air.dclassesByName['AccountAI'],
            {'MONEY': result - self.money})
        av = self.air.doId2do.get(self.target)
        if not av:
            self.demand('Off')
            return

        av.b_setBankMoney(result - self.money)
        self.demand('Off')

class BankManagerAI:

    def __init__(self, air):
        self.air = air
        self.avId2fsm = {}

    def performFSM(self, target, fsmClass, *args):
        self.avId2fsm[target] = fsmClass(self.air, self)
        self.avId2fsm[target].demand('Start', *args)

    def getMoney(self, avId):
        av = self.air.doId2do.get(avId)

        if not av:
            return

        DISLid = av.getDISLid()
        self.performFSM(avId, BankRetrieveFSM, avId, DISLid)
        return 'bankDone-%s' % avId

    def addMoney(self, avId, money):
        av = self.air.doId2do.get(avId)

        if not av:
            return

        DISLid = av.getDISLid()
        self.performFSM(avId, BankAddFSM, avId, DISLid, money)

    def takeMoney(self, avId, money):
        av = self.air.doId2do.get(avId)

        if not av:
            return

        DISLid = av.getDISLid()
        self.performFSM(avId, BankTakeFSM, avId, DISLid, money)
