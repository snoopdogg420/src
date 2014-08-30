from direct.interval.IntervalGlobal import LerpQuatInterval, LerpPosInterval
from direct.interval.IntervalGlobal import Sequence, Parallel, Func
from direct.interval.IntervalGlobal import SoundInterval

from otp.movie.MovieEvent import MovieEvent
from otp.otpbase import OTPGlobals


class MovieSimpleWalkEvent(MovieEvent):
    def __init__(self, avatar, quatA, quatB, pointA, pointB,
                 rotateSpeed=OTPGlobals.ToonRotateSpeed,
                 walkSpeed=OTPGlobals.ToonForwardSpeed,
                 rotateAnimName='walk', rotateAnimPlayRate=1,
                 walkAnimName='walk', walkAnimPlayRate=1, rotateSfx=None,
                 walkSfx=None):
        self.avatar = avatar
        self.quatA = quatA
        self.quatB = quatB
        self.pointA = pointA
        self.pointB = pointB
        self.rotateSpeed = rotateSpeed
        self.walkSpeed = walkSpeed
        self.rotateAnimName = rotateAnimName
        self.rotateAnimPlayRate = rotateAnimPlayRate
        self.walkAnimName = walkAnimName
        self.walkAnimPlayRate = walkAnimPlayRate
        self.rotateSfx = rotateSfx
        self.walkSfx = walkSfx

    def construct(self):
        track = Sequence()

        # First, set the avatar's positional components to its starting point:
        track.append(Func(self.avatar.setPos, self.pointA))
        track.append(Func(self.avatar.setQuat, self.quatA))

        # Next, construct the rotate track:
        rotateTrack = Parallel()
        if self.rotateAnimName is not None:
            rotateTrack.append(
                Func(self.avatar.setPlayRate, self.rotateAnimPlayRate,
                     self.rotateAnimName)
            )
            rotateTrack.append(
                Func(self.avatar.loop, self.rotateAnimName)
            )
        if self.rotateSfx is not None:
            rotateTrack.append(
                Func(base.playSfx, self.rotateSfx, looping=1, node=self.avatar)
            )
        rotateTrack.append(self.getQuatInterval())
        track.append(rotateTrack)

        # Clean up what is necessary:
        if self.rotateAnimName is not None:
            track.append(
                Func(self.avatar.setPlayRate, 1, self.rotateAnimName)
            )
        if self.rotateSfx is not None:
            track.append(
                Func(self.rotateSfx.stop)
            )

        # Then construct the walk track:
        walkTrack = Parallel()
        if self.walkAnimName is not None:
            walkTrack.append(
                Func(self.avatar.setPlayRate, self.walkAnimPlayRate,
                     self.walkAnimName)
            )
            walkTrack.append(
                Func(self.avatar.loop, self.walkAnimName)
            )
        if self.walkSfx is not None:
            walkTrack.append(
                SoundInterval(self.walkSfx, loop=1, node=self.avatar)
            )
        walkTrack.append(self.getPosInterval())
        track.append(walkTrack)

        # Finally, clean up what is necessary:
        if self.walkAnimName is not None:
            track.append(
                Func(self.avatar.setPlayRate, 1, self.walkAnimName)
            )
        if self.walkSfx is not None:
            track.append(
                Func(self.walkSfx.stop)
            )

        return track

    def getQuatInterval(self):
        duration = abs((self.quatB.getHpr()-self.quatA.getHpr())[0]) / self.rotateSpeed
        return LerpQuatInterval(
            self.avatar, duration, quat=self.quatB, startQuat=self.quatA
        )

    def getPosInterval(self):
        duration = (self.pointB-self.pointA).length() / self.walkSpeed
        return LerpPosInterval(
            self.avatar, duration, pos=self.pointB, startPos=self.pointA
        )
