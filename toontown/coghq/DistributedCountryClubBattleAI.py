from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.coghq.DistributedLevelBattleAI import DistributedLevelBattleAI


class DistributedCountryClubBattleAI(DistributedLevelBattleAI):
    notify = directNotify.newCategory('DistributedCountryClubBattleAI')
