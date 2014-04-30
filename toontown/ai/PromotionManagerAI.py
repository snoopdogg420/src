from toontown.suit import SuitDNA


class PromotionManagerAI:
    def __init__(self, air):
        self.air = air

    def recoverMerits(self, toon, suitsKilled, zoneId, multiplier):
        cogMerits = toon.getCogMerits()
        for suit in suitsKilled:
            deptIndex = SuitDNA.suitDepts.index(suit['track'])
            cogMerits[deptIndex] += (suit['level']/2) * multiplier
        toon.b_setCogMerits(cogMerits)
        return cogMerits
