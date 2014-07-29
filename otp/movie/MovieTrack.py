from direct.interval.IntervalGlobal import *


class MovieTrack(Sequence):
    def __init__(self, movie, name='MovieTrack'):
        Sequence.__init__(self)

        self.movie = movie
        self.name = name

        self.movie.add(self)

    def setMovie(self, movie):
        self.movie = movie

    def getMovie(self):
        return self.movie

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def add(self, event):
        self.append(event.construct())
