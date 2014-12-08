from toontown.event.ExperimentReward import ExperimentReward


class ExperimentHealthReward(ExperimentReward):
    def __init__(self, challenge, hpAmount):
        ExperimentReward.__init__(self, challenge)

        self.hpAmount = hpAmount

    def giveReward(self):
        for avId in self.participants:
            av = self.air.doId2do.get(avId)
            if av is None:
                continue

            av.b_setMaxHp(av.getMaxHp() + self.hpAmount)
            av.toonUp(av.getMaxHp())

    def notifyReward(self):
        self.messageParticipants('You have earned a laff boost!')
