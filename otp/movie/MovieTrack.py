from direct.interval.IntervalGlobal import Sequence


class MovieTrack(Sequence):
    def __init__(self, name='track'):
        Sequence.__init__(self)

        self.name = name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def add(self, event):
        self.append(event.construct())
