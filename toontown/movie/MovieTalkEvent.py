from direct.interval.IntervalGlobal import Sequence, Func, Wait

from otp.movie.MovieEvent import MovieEvent
from otp.nametag.NametagConstants import CFSpeech


class MovieTalkEvent(MovieEvent):
    def __init__(self, avatar, message, duration, chatFlags=CFSpeech, stompTime=0.2):
        self.avatar = avatar
        self.message = message
        self.duration = duration
        self.chatFlags = chatFlags
        self.stompTime = stompTime

    def construct(self):
        track = Sequence()

        track.append(Func(self.avatar.setChatAbsolute, self.message, self.chatFlags))
        track.append(Wait(self.duration))
        track.append(Func(self.avatar.clearChat))

        if self.stompTime > 0:
            track.append(Wait(self.stompTime))

        return track
