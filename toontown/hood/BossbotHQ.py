from toontown.coghq.BossbotCogHQLoader import BossbotCogHQLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.CogHood import CogHood


class BossbotHQ(CogHood):
    notify = directNotify.newCategory('BossbotHQ')

    ID = ToontownGlobals.BossbotHQ
    LOADER_CLASS = BossbotCogHQLoader

    def load(self):
        CogHood.load(self)

        self.sky.hide()

    def enter(self, requestStatus):
        CogHood.enter(self, requestStatus)

        base.localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.BossbotHQCameraNear, ToontownGlobals.BossbotHQCameraFar)
