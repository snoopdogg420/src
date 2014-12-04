from direct.distributed.ClockDelta import globalClockDelta


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
            self.stop()

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
            track.finish()

        self.cleanup()

    def cleanup(self):
        pass  # Inheritors should override this method.

    def addTrack(self, track):
        self.tracks[track.getName()] = track

    def getTrack(self, name):
        return self.tracks.get(name)

    def getDuration(self):
        return max([track.getDuration() for track in self.tracks.values()])

    def __handleMovieDone(self, task):
        self.stop()
        return task.done
