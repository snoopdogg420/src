from direct.task.Task import Task


class Movie:
    def __init__(self):
        self.tracks = {}

    def setup(self):
        pass  # Inheritors should override this method.

    def start(self, timestamp):
        self.setup()

        for track in self.tracks.values():
            track.start(timestamp)

        taskMgr.doMethodLater(
            self.getDuration(), self.__handleMovieDone, 'Movie-done')

    def stop(self):
        for track in self.tracks.values():
            track.stop()

        self.cleanup()

    def cleanup(self):
        pass  # Inheritors should override this method.

    def add(self, track):
        self.tracks[track.getName()] = track

    def get(self, name):
        return self.tracks.get(name)

    def getDuration(self):
        return max([track.getDuration() for track in self.tracks])

    def __handleMovieDone(self, task):
        self.cleanup()
        return Task.done
