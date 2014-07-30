from direct.interval.IntervalGlobal import *

from otp.movie.MovieEvent import MovieEvent
from otp.nametag.NametagConstants import CFSpeech


class MovieTalkEvent(MovieEvent):
    def __init__(self, track, avatar, message):
        MovieEvent.__init__(self, track)

        self.avatar = avatar
        self.message = message

        self.messageTime = 0.5 * len(self.message.split(' '))

    def construct(self):
        MovieEvent.construct(self)

        track = Sequence()
        track.append(Func(self.avatar.setChatAbsolute, self.message, CFSpeech))
        track.append(Wait(self.messageTime))
        track.append(Func(self.avatar.clearChat))
        return track
