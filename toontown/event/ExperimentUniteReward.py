from toontown.event.ExperimentReward import ExperimentReward
from toontown.chat import ResistanceChat

import random


class ExperimentUniteReward(ExperimentReward):
    ALLOWED_UNITES = [ResistanceChat.RESISTANCE_TOONUP,
                      ResistanceChat.RESISTANCE_RESTOCK]

    def __init__(self, challenge, uniteType, uniteCount):
        ExperimentReward.__init__(self, challenge)

        self.uniteType = uniteType
        self.uniteCount = uniteCount

    def giveReward(self):
        for avId in self.participants:
            av = self.air.doId2do.get(avId)
            if av is None:
                continue

            for _ in xrange(self.uniteCount):
                if self.uniteType == 'any':
                    menuIndex = random.choice(ALLOWED_UNITES)
                else:
                    menuIndex = self.uniteType

                itemIndex = random.choice(ResistanceChat.getItems(menuIndex))
                textId = ResistanceChat.encodeId(menuIndex, itemIndex)

                av.addResistanceMessage(textId)


    def notifyReward(self):
        self.messageParticipants('You have earned %s unites!' % self.uniteCount)
