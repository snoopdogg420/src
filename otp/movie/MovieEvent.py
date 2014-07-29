from direct.interval.IntervalGlobal import *


class MovieEvent:
    def __init__(self, track):
        self.track = track
        self.movie = self.track.getMovie()

    def construct(self):
        return Sequence()  # Inheritors should override this method.
