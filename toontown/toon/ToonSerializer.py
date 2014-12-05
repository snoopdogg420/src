from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

import os


class ToonSerializer:
    def __init__(self, toon):
        self.toon = toon
        self.filepath = 'toondata/%s.td' % self.toon.doId

        if not os.path.exists('toondata'):
            os.makedirs('toondata')

    def saveToon(self, callback=None):
        with open(self.filepath, 'wb') as f:
            data = PyDatagram()

            data.addInt16(self.toon.maxHp)
            data.addInt16(self.toon.hp)

            data.addUint8(self.toon.maxCarry)
            data.addInt16(self.toon.money)
            data.addUint8(self.toon.questCarryLimit)

            data.addUint8(len(self.toon.trackArray))
            for track in self.toon.trackArray:
                data.addUint16(track)

            data.addUint8(len(self.toon.trackBonusLevel))
            for track in self.toon.trackBonusLevel:
                data.addInt8(track)

            data.addString(self.toon.experience.makeNetString())
            data.addString(self.toon.inventory.makeNetString())
            data.addUint8(self.toon.pinkSlips)

            data.addUint8(len(self.toon.cogMerits))
            for merit in self.toon.cogMerits:
                data.addUint16(merit)
            data.addUint8(len(self.toon.cogParts))
            for part in self.toon.cogParts:
                data.addUint32(part)
            data.addUint8(len(self.toon.cogTypes))
            for cog in self.toon.cogTypes:
                data.addUint8(cog)
            data.addUint8(len(self.toon.cogLevels))
            for level in self.toon.cogLevels:
                data.addUint8(level)
            data.addUint8(len(self.toon.cogs))
            for cog in self.toon.cogs:
                data.addUint32(cog)
            data.addUint8(len(self.toon.cogCounts))
            for cog in self.toon.cogCounts:
                data.addUint32(cog)
            data.addUint8(len(self.toon.cogRadar))
            for cog in self.toon.cogRadar:
                data.addUint8(cog)
            data.addUint8(len(self.toon.buildingRadar))
            for building in self.toon.buildingRadar:
                data.addUint8(building)
            data.addUint8(len(self.toon.promotionStatus))
            for promotion in self.toon.promotionStatus:
                data.addUint8(promotion)

            data.addUint8(len(self.toon.getQuests()))
            for quest in self.toon.getQuests():
                data.addUint32(quest)
            data.addUint8(len(self.toon.resistanceMessages))
            for message in self.toon.resistanceMessages:
                data.addUint8(len(message))
                for x in message:
                    data.addInt16(x)

            sosCards = self.toon.getNPCFriendsList()
            data.addUint8(len(sosCards))
            for sosCard in sosCards:
                data.addUint32(sosCard[0])
                data.addUint8(sosCard[1])

            f.write(PyDatagramIterator(data).getRemainingBytes())

        if callback:
            callback(self.toon)

    def restoreToon(self, callback=None):
        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, 'rb') as f:
            data = f.read()
            dg = PyDatagram(data)
            data = PyDatagramIterator(dg)

            self.toon.b_setMaxHp(data.getInt16())
            self.toon.b_setHp(data.getInt16())

            self.toon.b_setMaxCarry(data.getUint8())
            self.toon.b_setMoney(data.getInt16())
            self.toon.b_setQuestCarryLimit(data.getUint8())

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint16())
            self.toon.b_setTrackAccess(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getInt8())
            self.toon.b_setTrackBonusLevel(tdata)

            self.toon.b_setExperience(data.getString())
            self.toon.b_setInventory(data.getString())
            self.toon.b_setPinkSlips(data.getUint8())

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint16())
            self.toon.b_setCogMerits(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint32())
            self.toon.b_setCogParts(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint8())
            self.toon.b_setCogTypes(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint8())
            self.toon.b_setCogLevels(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint32())
            self.toon.b_setCogStatus(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint32())
            self.toon.b_setCogCount(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint8())
            self.toon.b_setCogRadar(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint8())
            self.toon.b_setBuildingRadar(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint8())
            self.toon.b_setPromotionStatus(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                tdata.append(data.getUint32())
            self.toon.b_setQuests(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                ndata = []
                for _ in xrange(data.getUint8()):
                    ndata.append(data.getInt16())
                tdata.append(ndata)
            self.toon.b_setResistanceMessages(tdata)

            tdata = []
            for _ in xrange(data.getUint8()):
                x = data.getUint32()
                y = data.getUint8()
                tdata.append([x, y])
            self.toon.b_setNPCFriendsDict(tdata)

            self.toon.b_setExperience(self.toon.experience.makeNetString())

        os.remove(self.filepath)

        if callback:
            callback(self.toon)
