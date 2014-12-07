from toontown.event.ExperimentReward import ExperimentReward

import random


class ExperimentGagReward(ExperimentReward):
    def __init__(self, challenge, gagTrack):
        ExperimentReward.__init__(self, challenge)

        self.gagTrack = gagTrack

    def giveReward(self):
        for avId in self.participants:
            av = self.air.doId2do.get(avId)
            if av is None:
                continue

            possibleTracks = []
            for track, access in enumerate(av.trackArray):
                if not access:
                    possibleTracks.append(track)

            trackChoice = random.choice(possibleTracks)
            av.trackArray[trackChoice] = 1
            av.d_setTrackAccess(av.trackArray)
            av.b_setMaxCarry(av.maxCarry + 10)

    def notifyReward(self):
        self.messageParticipants('You have earned a new Gag track!')
