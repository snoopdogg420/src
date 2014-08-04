from toontown.nametag import Nametag2d
from toontown.nametag import Nametag3d


class NametagGroup:
    def __init__(self):
        self.nametags = []
        self.manager = None

        self.nametag2d = Nametag2d.Nametag2d()
        self.nametag3d = Nametag3d.Nametag3d()

        self.add(self.nametag2d)
        self.add(self.nametag3d)

        self.speedChatColor = None

    def getNametags(self):
        return self.nametags

    def getManager(self):
        return self.manager

    def setNametag2d(self, nametag2d):
        self.nametag2d = nametag2d

    def getNametag2d(self):
        return self.nametag2d

    def setNametag3d(self, nametag3d):
        self.nametag3d = nametag3d

    def getNametag3d(self):
        return self.nametag3d

    def add(self, nametag):
        self.nametags.append(nametag)
        # TODO: Manage the nametag.

    def remove(self, nametag):
        self.nametags.remove(nametag)
        # TODO: Unmanage the nametag.
        nametag.destroy()

    def manage(self, manager):
        self.manager = manager

    def unmanage(self, manager):
        for nametag in self.nametags:
            # TODO: Check if this is an instance of MarginPopup.
            nametag.unmanage(manager)
        self.manager = None

    def setSpeedChatColor(self, speedChatColor):
        self.speedChatColor = speedChatColor

    def getSpeedChatColor(self):
        return self.speedChatColor

    def destroy(self):
        pass
