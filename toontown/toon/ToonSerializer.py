import os


class ToonSerializer:
    def __init__(self, toon):
        self.toon = toon
        self.filepath = 'backups/toondata/%s.json' % self.toon.doId

    def saveToon(self, callback=None):
        toonData = {}

        toonData['maxHp'] = self.toon.maxHp
        toonData['hp'] = self.toon.hp

        toonData['maxCarry'] = self.toon.maxCarry
        toonData['money'] = self.toon.money
        toonData['questCarryLimit'] = self.toon.questCarryLimit

        toonData['trackArray'] = self.toon.trackArray
        toonData['trackBonusLevel'] = self.toon.trackBonusLevel

        toonData['experience'] = self.toon.experience.makeNetString()
        toonData['inventory'] = self.toon.inventory.makeNetString()
        toonData['pinkSlips'] = self.toon.pinkSlips

        toonData['cogMerits'] = self.toon.cogMerits
        toonData['cogParts'] = self.toon.cogParts
        toonData['cogTypes'] = self.toon.cogTypes
        toonData['cogLevels'] = self.toon.cogLevels
        toonData['cogs'] = self.toon.cogs
        toonData['cogCounts'] = self.toon.cogCounts
        toonData['cogRadar'] = self.toon.cogRadar
        toonData['buildingRadar'] = self.toon.buildingRadar
        toonData['promotionStatus'] = self.toon.promotionStatus

        toonData['quests'] = self.toon.quests
        toonData['resistanceMessages'] = self.toon.resistanceMessages
        toonData['sosCards'] = self.toon.getNPCFriendsList()

        simbase.backups.save('toondata', (self.toon.doId,), toonData)

        if callback:
            callback(self.toon)

    def restoreToon(self, callback=None):
        toonData = simbase.backups.load('toondata', (self.toon.doId,))
        if toonData is None:
            return

        self.toon.b_setMaxHp(toonData['maxHp'])
        self.toon.b_setHp(toonData['hp'])

        self.toon.b_setMaxCarry(toonData['maxCarry'])
        self.toon.b_setMoney(toonData['money'])
        self.toon.b_setQuestCarryLimit(toonData['questCarryLimit'])

        self.toon.b_setTrackAccess(toonData['trackArray'])
        self.toon.b_setTrackBonusLevel(toonData['trackBonusLevel'])

        self.toon.b_setExperience(toonData['experience'])
        self.toon.b_setInventory(toonData['inventory'])
        self.toon.b_setPinkSlips(toonData['pinkSlips'])

        self.toon.b_setCogMerits(toonData['cogMerits'])
        self.toon.b_setCogParts(toonData['cogParts'])
        self.toon.b_setCogTypes(toonData['cogTypes'])
        self.toon.b_setCogLevels(toonData['cogLevels'])
        self.toon.b_setCogStatus(toonData['cogs'])
        self.toon.b_setCogCount(toonData['cogCounts'])
        self.toon.b_setCogRadar(toonData['cogRadar'])
        self.toon.b_setBuildingRadar(toonData['buildingRadar'])
        self.toon.b_setPromotionStatus(toonData['promotionStatus'])

        self.toon.b_setQuests(toonData['quests'])
        self.toon.b_setResistanceMessages(toonData['resistanceMessages'])
        self.toon.b_setNPCFriendsDict(toonData['sosCards'])

        self.toon.b_setExperience(self.toon.experience.makeNetString())

        os.remove(self.filepath)

        if callback:
            callback(self.toon)
