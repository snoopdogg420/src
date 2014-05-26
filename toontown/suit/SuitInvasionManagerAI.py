from toontown.suit.SuitDNA import suitHeadTypes as suitNames
from toontown.toonbase import ToontownGlobals
import random

from otp.ai.MagicWordGlobal import *
import shlex

class SuitInvasionManagerAI:

    MIN_TIME_INBETWEEN = 10
    MAX_TIME_INBETWEEN = 30

    MIN_TIME_DURING = 3
    MAX_TIME_DURING = 10

    def __init__(self, air):
        self.air = air
        self.currentInvadingSuit = None
        self.isSkelecog = 0

        self.startInvading()

    def isInvasionRunning(self):
        return not self.currentInvadingSuit is None

    def getInvading(self):
        return self.isInvasionRunning

    def getInvadingCog(self):
        return (self.currentInvadingSuit, self.isSkelecog)

    def newInvasion(self, task=None, name=None, skelecog=0):
        if name:
            self.currentInvadingSuit = name
            self.isSkelecog = skelecog
        elif self.currentInvadingSuit == None:
            self.currentInvadingSuit = random.choice(suitNames)
            roll = random.randint(0, 100)

            if roll >= 99:
                self.isSkelecog = 1

        if self.currentInvadingSuit:
            self.air.newsManager.setInvasionStatus(ToontownGlobals.SuitInvasionBegin, self.currentInvadingSuit, 10, self.isSkelecog)
            self.cleanupCurrentSuits()
            self.invasionStarted()
            if task:
                return task.done

        if task:
            return task.again

    def invasionStarted(self):
        t = self.MIN_TIME_DURING + random.randint(1, self.MAX_TIME_DURING)

        if t > self.MAX_TIME_DURING:
            t = self.MAX_TIME_DURING

        taskMgr.doMethodLater(t*60, self.cleanupInvasion, 'suitInvasionManager-cleanup')

    def startInvading(self):
        t = self.MIN_TIME_INBETWEEN + random.randint(1, self.MAX_TIME_INBETWEEN)

        if t > self.MAX_TIME_INBETWEEN:
            t = self.MAX_TIME_INBETWEEN

        taskMgr.doMethodLater(t*60, self.newInvasion, 'suitInvasionManager-invasion')

    def summonInvasion(self, name, skelecog):
        if name in suitNames:
            if self.currentInvadingSuit:
                self.cleanupInvasion()
                self.cleanupTasks()

            self.newInvasion(task=None, name=name, skelecog=skelecog)

    def cleanupInvasion(self, task=None):
        self.air.newsManager.setInvasionStatus(ToontownGlobals.SuitInvasionEnd, self.currentInvadingSuit, 10, self.isSkelecog)
        self.currentInvadingSuit = None
        self.isSkelecog = 0

        self.cleanupCurrentSuits()

        if task:
            self.startInvading()
            return task.done

    def cleanupCurrentSuits(self):
        for suitPlanner in self.air.suitPlanners:
            self.air.suitPlanners.get(suitPlanner).flySuits()

    def cleanupTasks(self):
        taskMgr.remove('suitInvasionManager-invasion')
        taskMgr.remove('suitInvasionManager-cleanup')

@magicWord(category=CATEGORY_ADMINISTRATOR, types=[str, str, int])
def invasion(command, name='f', skelecog=0):
    command = command.lower()
    target = spellbook.getTarget()

    if command == 'summon':
        simbase.air.suitInvasionManager.summonInvasion(name, skelecog)

        if skelecog:
            name = 'Skelecog'
        return 'Summoning %s.'%(name)
    elif command == 'end':
        if simbase.air.suitInvasionManager.isInvasionRunning():
            simbase.air.suitInvasionManager.cleanupInvasion()
            simbase.air.suitInvasionManager.cleanupTasks()
            simbase.air.suitInvasionManager.startInvading()
            return 'Ended invasion.'
        else:
            return 'There is no invasion to end.'
    else:
        return "Unknown command '%s'."%(command)