class ExperimentReward:
    def __init__(self, challenge):
        self.challenge = challenge
        self.participants = self.challenge.experimentEvent.participants
        self.air = self.challenge.experimentEvent.air

    def handleReward(self):
        self.giveReward()
        self.notifyReward()

    def giveReward(self):
        pass

    def notifyReward(self):
        pass

    def messageParticipants(self, message):
        self.challenge.experimentEvent.messageParticipants(message)
