from direct.interval.IntervalGlobal import LerpQuatInterval
from direct.interval.IntervalGlobal import Sequence, Parallel, Func

from otp.movie.MovieEvent import MovieEvent
from otp.otpbase import OTPGlobals


class MovieSimpleRotateWalkEvent(MovieEvent):
    def __init__(self, avatar, quatA, quatB, speed=OTPGlobals.ToonRotateSpeed,
                 animName='walk', animPlayRate=1, sfx=None):
        self.avatar = avatar
        self.quatA = quatA
        self.quatB = quatB
        self.speed = speed
        self.animName = animName
        self.animPlayRate = animPlayRate
        self.sfx = sfx

    def construct(self):
        track = Sequence()

        # First, set the avatar's initial rotational components:
        track.append(Func(self.avatar.setQuat, self.quatA))

        # Next, construct the rotate track:
        rotateTrack = Parallel()
        if self.animName is not None:
            rotateTrack.append(
                Func(self.avatar.setPlayRate, self.animPlayRate, self.animName)
            )
            rotateTrack.append(Func(self.avatar.loop, self.animName))
        if self.sfx is not None:
            rotateTrack.append(
                Func(base.playSfx, self.sfx, looping=1, node=self.avatar)
            )
        rotateTrack.append(self.getQuatInterval())
        track.append(rotateTrack)

        # Finally, clean up what is necessary:
        if self.animName is not None:
            track.append(Func(self.avatar.setPlayRate, 1, self.animName))
        if self.sfx is not None:
            track.append(Func(self.sfx.stop))

        return track

    def getQuatInterval(self):
        duration = abs((self.quatB.getHpr()-self.quatA.getHpr())[0]) / self.speed
        return LerpQuatInterval(
            self.avatar, duration, quat=self.quatB, startQuat=self.quatA
        )
