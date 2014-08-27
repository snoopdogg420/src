from direct.interval.IntervalGlobal import *

from otp.movie.MovieEvent import MovieEvent


class MovieFuncEvent(MovieEvent, Func):
    def construct(self):
        return self
