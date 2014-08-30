from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.task.Task import Task
from pandac.PandaModules import ClockObject

from otp.movie.MovieEvent import MovieEvent
from otp.otpbase import OTPGlobals


class MovieRotateWalkEvent(MovieEvent):
    def __init__(self, avatar, duration, speed=OTPGlobals.ToonRotateSpeed,
                 animName='walk', animPlayRate=1, sfx=None):
        self.avatar = avatar
        self.duration = duration
        self.speed = speed
        self.animName = animName
        self.animPlayRate = animPlayRate
        self.sfx = sfx

        self.stepTaskName = self.getUniqueName() + '-step'

    def getUniqueName(self):
        return 'MovieRotateWalkEvent-' + str(id(self))

    def construct(self):
        track = Sequence()

        # Construct the rotate track:
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
        rotateTrack.append(Func(taskMgr.add, self.step, self.stepTaskName, 25))
        track.append(rotateTrack)

        # Wait the duration, and the stop the step task:
        track.append(Wait(self.duration))
        track.append(Func(taskMgr.remove, self.stepTaskName))

        # Finally, clean up what is necessary:
        if self.animName is not None:
            track.append(Func(self.avatar.setPlayRate, 1, self.animName))
        if self.sfx is not None:
            track.append(Func(self.sfx.stop))

        return track

    def step(self, task):
        step = ClockObject.getGlobalClock().getDt() * self.speed
        self.avatar.setH(self.avatar.getH() + step)

        return Task.cont
