from direct.interval.IntervalGlobal import Sequence, Func, Wait

from otp.movie.MovieEvent import MovieEvent
from otp.nametag.NametagConstants import CFSpeech


class MovieTalkEvent(MovieEvent):
    def __init__(self, avatar, message, chatFlags=CFSpeech, timePerWord=0.55):
        self.avatar = avatar
        self.message = message
        self.chatFlags = chatFlags
        self.timePerWord = timePerWord

        self.duration = self.timePerWord * len(self.message.split(' '))

    def construct(self):
        track = Sequence()
        track.append(Func(self.avatar.setChatAbsolute, self.message, self.chatFlags))
        track.append(Wait(self.duration))
        track.append(Func(self.avatar.clearChat))

        return track
