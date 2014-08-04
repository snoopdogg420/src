from toontown.nametag import Nametag


class Nametag3d(Nametag.Nametag):
    def __init__(self, avatar=None, name=''):
        Nametag.Nametag.__init__(self, avatar, name)

        self.billboardOffset = 3

    def setBillboardOffset(self, billboardOffset):
        self.billboardOffset = billboardOffset

    def getBillboardOffset(self):
        return self.billboardOffset

