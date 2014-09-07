from toontown.nametag.Nametag2d import Nametag2d
from toontown.nametag.NametagFloat3d import NametagFloat3d


class NametagFloat2d(NametagFloat3d):
    def doBillboardEffect(self):
        pass

    def update(self):
        NametagFloat3d.update(self)

        if self.getChatText() and self.hasChatButton():
            self.updateClickRegion()
        else:
            self.region.setActive(False)

    def setClickRegion(self, left, right, bottom, top):
        Nametag2d.setClickRegion(self, left, right, bottom, top)
