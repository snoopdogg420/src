from toontown.coghq import CogDisguiseGlobals


class CogSuitManagerAI:
    def __init__(self, air):
        self.air = air

    def recoverPart(self, toon, factoryType, suitTrack, zoneId, toons):
        recoveredParts = [0, 0, 0, 0]
        parts = toon.getCogParts()
        if CogDisguiseGlobals.isSuitComplete(parts, suitTrack):
            return recoveredParts
        recoveredParts[suitTrack] = toon.giveGenericCogPart(factoryType, suitTrack)
        return recoveredParts
