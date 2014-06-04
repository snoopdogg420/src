from toontown.coghq import CogDisguiseGlobals
from toontown.suit import SuitDNA


class PromotionManagerAI:
    def __init__(self, air):
        self.air = air

    def recoverMerits(self, toon, suitsKilled, zoneId, multiplier=1.0, extraMerits=0):
        cogMerits = toon.getCogMerits()
        parts = toon.getCogParts()
        completedSuits = (
            CogDisguiseGlobals.isSuitComplete(parts, 0),
            CogDisguiseGlobals.isSuitComplete(parts, 1),
            CogDisguiseGlobals.isSuitComplete(parts, 2),
            CogDisguiseGlobals.isSuitComplete(parts, 3)
        )
        for suit in suitsKilled:
            deptIndex = SuitDNA.suitDepts.index(suit['track'])
            if completedSuits[deptIndex]:
                cogMerits[deptIndex] += (suit['level']/2) * multiplier
        if completedSuits[deptIndex]:
            cogMerits += extraMerits
        toon.b_setCogMerits(cogMerits)
        return cogMerits
