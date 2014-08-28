from direct.distributed.ClockDelta import globalClockDelta
from direct.task.Task import Task


class Movie:
    def __init__(self):
        self.tracks = {}

        self.doneTaskName = self.getUniqueName() + '-done'
        self.doneTask = None

    def getUniqueName(self):
        return 'Movie-' + str(id(self))

    def setup(self):
        pass  # Inheritors should override this method.

    def start(self, timestamp):
        if self.doneTask is not None:
            taskMgr.remove(self.doneTask)
            self.doneTask = None

        self.setup()

        for track in self.tracks.values():
            track.start(globalClockDelta.localElapsedTime(timestamp, bits=32))

        self.doneTask = taskMgr.doMethodLater(
            self.getDuration(), self.__handleMovieDone,
            self.getUniqueName() + '-done')

    def stop(self):
        if self.doneTask is not None:
            taskMgr.remove(self.doneTask)
            self.doneTask = None

        for track in self.tracks.values():
            track.pause()

        self.cleanup()

    def cleanup(self):
        pass  # Inheritors should override this method.

    def add(self, track):
        self.tracks[track.getName()] = track

    def get(self, name):
        return self.tracks.get(name)

    def getDuration(self):
        return max([track.getDuration() for track in self.tracks.values()])

    def __handleMovieDone(self, task):
        self.stop()
        return Task.done
