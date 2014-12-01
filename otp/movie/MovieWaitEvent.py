from direct.interval.IntervalGlobal import Wait

from otp.movie.MovieEvent import MovieEvent


class MovieWaitEvent(MovieEvent, Wait):
    def construct(self):
        return self
