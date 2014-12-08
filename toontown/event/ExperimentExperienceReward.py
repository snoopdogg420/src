from toontown.event.ExperimentReward import ExperimentReward

import random


class ExperimentExperienceReward(ExperimentReward):
    def giveReward(self):
        for avId in self.participants:
            av = self.air.doId2do.get(avId)
            if av is None:
                continue

            for track, hasAccess in enumerate(av.trackArray):
                if hasAccess:
                    xp = av.experience.getNextExpValue(track) * random.random()
                    av.experience.setExp(xp)

            av.d_setExperience(av.experience.makeNetString())

    def notifyReward(self):
        self.messageParticipants('You have earned some extra Gag points!')
