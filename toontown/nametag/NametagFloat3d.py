from toontown.nametag.Nametag3d import Nametag3d


class NametagFloat3d(Nametag3d):
    SCALING_FACTOR = 1.0

    def tick(self, task):
        self.contents.setScale(NametagFloat3d.SCALING_FACTOR)
        return Task.cont
