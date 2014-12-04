from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.task.Task import Task
from panda3d.core import ClockObject, Mat3, Vec3, Point3

from otp.movie.MovieEvent import MovieEvent
from otp.otpbase import OTPGlobals


class MovieWalkEvent(MovieEvent):
    def __init__(self, avatar, duration, speed=OTPGlobals.ToonForwardSpeed,
                 animName='walk', animPlayRate=1, sfx=None):
        self.avatar = avatar
        self.duration = duration
        self.speed = speed
        self.animName = animName
        self.animPlayRate = animPlayRate
        self.sfx = sfx

        self.stepTaskName = self.getUniqueName() + '-step'

    def getUniqueName(self):
        return 'MovieWalkEvent-' + str(id(self))

    def construct(self):
        track = Sequence()

        # Construct the walk track:
        walkTrack = Parallel()
        if self.animName is not None:
            walkTrack.append(Func(self.avatar.setPlayRate, self.animPlayRate, self.animName))
            walkTrack.append(Func(self.avatar.loop, self.animName))
        if self.sfx is not None:
            walkTrack.append(Func(base.playSfx, self.sfx, looping=1, node=self.avatar))
        walkTrack.append(Func(taskMgr.add, self.step, self.stepTaskName, 25))
        track.append(walkTrack)

        # Wait the duration, and then stop the step task:
        track.append(Wait(self.duration))
        track.append(Func(taskMgr.remove, self.stepTaskName))

        # Finally, clean up what is necessary:
        if self.animName is not None:
            track.append(Func(self.avatar.setPlayRate, 1, self.animName))
        if self.sfx is not None:
            track.append(Func(self.sfx.stop))

        return track

    def step(self, task):
        distance = ClockObject.getGlobalClock().getDt() * self.speed

        rotMat = Mat3.rotateMatNormaxis(self.avatar.getH(), Vec3.up())
        step = Vec3(rotMat.xform(Vec3.forward() * distance))
        self.avatar.setFluidPos(Point3(self.avatar.getPos() + step))

        return Task.cont
