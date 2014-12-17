from toontown.cogdominium.DistCogdoLevelGameAI import DistCogdoLevelGameAI
from toontown.cogdominium import CogdoCraneGameSpec


class DistCogdoCraneGameAI(DistCogdoLevelGameAI):
    notify = directNotify.newCategory('DistCogdoCraneGameAI')

    def getLevelSpec(self):
        return CogdoCraneGameSpec.levelSpec
