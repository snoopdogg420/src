from toontown.coghq import CogDisguiseGlobals


class CogSuitManagerAI:
    def __init__(self, air):
        self.air = air

    def recoverPart(self, toon, factoryType, suitTrack, zoneId, toons):
        parts = toon.getCogParts()
        if CogDisguiseGlobals.isSuitComplete(parts, suitTrack):
            return
        return toon.giveGenericCogPart(factoryType, suitTrack)
