from toontown.event.ExperimentReward import ExperimentReward


class ExperimentFireReward(ExperimentReward):
    def __init__(self, challenge, fireCount):
        ExperimentReward.__init__(self, challenge)

        self.fireCount = fireCount

    def giveReward(self):
        for avId in self.participants:
            av = self.air.doId2do[avId]
            av.b_setPinkSlips(av.getPinkSlips() + self.fireCount)

    def notifyReward(self):
        self.messageParticipants('You have earned %s Pink Slips.' % self.fireCount)
