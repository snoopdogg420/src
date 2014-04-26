class BattleManagerAI:
    def __init__(self, air):
        self.air = air

        self.cellId2battle = {}

    def destroy(self, battle):
        for cellId, otherBattle in self.cellId2battle.items():
            if battle is otherBattle:
                battle.requestDelete()
                del self.cellId2battle[cellId]

    def getBattle(self, cellId):
        return self.cellId2battle.get(cellId)

    def requestBattleAddSuit(self, cellId, otherSuit):
        battle = self.getBattle(cellId)
        if battle:
            battle.suitRequestJoin(otherSuit)
