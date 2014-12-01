from direct.interval.IntervalGlobal import Func

from otp.movie.MovieEvent import MovieEvent


class MovieFuncEvent(MovieEvent, Func):
    def construct(self):
        return self
