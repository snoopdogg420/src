from direct.task.Task import Task
from panda3d.core import ClockObject

from otp.otpbase import OTPGlobals
from toontown.movie.MovieWalkEvent import MovieWalkEvent


class MovieRotateEvent(MovieWalkEvent):
    def __init__(self, avatar, duration, speed=OTPGlobals.ToonRotateSpeed,
                 animName='walk', animPlayRate=1, sfx=None):
        MovieWalkEvent.__init__(self, avatar, duration, speed=speed,
                                animName=animName, animPlayRate=animPlayRate,
                                sfx=sfx)

    def getUniqueName(self):
        return 'MovieRotateEvent-' + str(id(self))

    def step(self, task):
        step = ClockObject.getGlobalClock().getDt() * self.speed
        self.avatar.setH(self.avatar.getH() + step)

        return Task.cont
