from toontown.movie.ToontownMovie import ToontownMovie


class GrandOpeningMovie(ToontownMovie):
    def __init__(self, scene):
        ToontownMovie.__init__(self)

        self.scene = scene
