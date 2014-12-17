from toontown.cogdominium.DistCogdoLevelGameAI import DistCogdoLevelGameAI
from toontown.cogdominium import CogdoCraneGameSpec
from otp.level.LevelSpec import LevelSpec


class DistCogdoCraneGameAI(DistCogdoLevelGameAI):
    notify = directNotify.newCategory('DistCogdoCraneGameAI')

    def getLevelSpec(self):
        return LevelSpec(CogdoCraneGameSpec)

    def startHandleEdits(self):
        pass

    def stopHandleEdits(self):
        pass
