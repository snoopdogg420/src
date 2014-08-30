from direct.interval.IntervalGlobal import LerpPosInterval
from direct.interval.IntervalGlobal import Sequence, Parallel, Func

from otp.movie.MovieEvent import MovieEvent
from otp.otpbase import OTPGlobals


class MovieSimpleWalkEvent(MovieEvent):
    def __init__(self, avatar, pointA, pointB,
                 speed=OTPGlobals.ToonForwardSpeed, animName='run',
                 animPlayRate=1, sfx=None):
        self.avatar = avatar
        self.pointA = pointA
        self.pointB = pointB
        self.speed = speed
        self.animName = animName
        self.animPlayRate = animPlayRate
        self.sfx = sfx

    def construct(self):
        track = Sequence()

        # First, set the avatar's initial positional components:
        track.append(Func(self.avatar.setPos, self.pointA))

        # Next, construct the walk track:
        walkTrack = Parallel()
        if self.animName is not None:
            walkTrack.append(
                Func(self.avatar.setPlayRate, self.animPlayRate, self.animName)
            )
            walkTrack.append(Func(self.avatar.loop, self.animName))
        if self.sfx is not None:
            walkTrack.append(
                Func(base.playSfx, self.sfx, looping=1, node=self.avatar)
            )
        walkTrack.append(self.getPosInterval())
        track.append(walkTrack)

        # Finally, clean up what is necessary:
        if self.animName is not None:
            track.append(Func(self.avatar.setPlayRate, 1, self.animName))
        if self.sfx is not None:
            track.append(Func(self.sfx.stop))

        return track

    def getPosInterval(self):
        duration = (self.pointB-self.pointA).length() / self.speed
        return LerpPosInterval(
            self.avatar, duration, pos=self.pointB, startPos=self.pointA
        )
