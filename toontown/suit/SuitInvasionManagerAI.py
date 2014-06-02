from toontown.toonbase import ToontownGlobals, TTLocalizerEnglish
from otp.ai.MagicWordGlobal import *
from toontown.suit.SuitDNA import *
import random
import shlex

class SuitInvasionManagerAI:
    MIN_TIME_INBETWEEN = 10
    MAX_TIME_INBETWEEN = 30
    MIN_TIME_DURING = 3
    MAX_TIME_DURING = 10

    def __init__(self, air):
        self.air = air
        self.currentInvadingSuit = None
        self.currentInvadingDept = None
        self.invasionStatus = False
        self.isSkelecog = 0
        self.isWaiter = 0
        self.isV2 = 0
        # self.startInvading()

    def getInvading(self):
        return self.invasionStatus

    def getInvadingCog(self):
        currentInvadingSuit = self.currentInvadingSuit
        currentInvadingDept = self.currentInvadingDept

        if currentInvadingSuit == 'any':
            if currentInvadingDept in suitDepts:
                currentInvadingSuit = getRandomSuitByDept(currentInvadingDept)
            else:
                currentInvadingSuit = None

        return (currentInvadingSuit, self.isSkelecog,
                self.isV2, self.isWaiter)

    def newInvasion(self, name='any', dept='any', skelecog=0, v2=0, waiter=0):
        print 'NEW_INVASION: suit: %s, dept: %s, skelecog: %s, v2: %s, waiter: %s' % (
                name, dept, skelecog, v2, waiter)
        if name == 'any' and dept == 'any':
            if not skelecog and not v2 and not waiter:
                return False
        self.currentInvadingSuit = name
        self.currentInvadingDept = dept
        self.invasionStatus = True
        self.isSkelecog = skelecog
        self.isWaiter = waiter
        self.isV2 = v2

        self.cleanupCurrentSuits()
        self.alertPlayersOfInvasion()
        self.invasionStarted()

        return True

    def alertPlayersOfInvasion(self):
        currentInvadingSuit = self.currentInvadingSuit
        departmentInvasion = False
        if currentInvadingSuit == 'any':
            if self.currentInvadingDept == 'any':
                currentInvadingSuit = 'f'
            else:
                #Department invasion
                currentInvadingSuit = self.currentInvadingDept
                departmentInvasion = True
        if self.isSkelecog:
            msgType = ToontownGlobals.SkelecogInvasionBegin
            self.isWaiter = 0
            self.isV2 = 0
            departmentInvasion = False
        elif self.isV2:
            msgType = ToontownGlobals.V2InvasionBegin
            self.isSkelecog = 0
            self.isWaiter = 0
            departmentInvasion = False
        elif self.isWaiter:
            msgType = ToontownGlobals.WaiterInvasionBegin
            self.isSkelecog = 0
            self.isV2 = 0
            departmentInvasion = False
        elif departmentInvasion:
            msgType = ToontownGlobals.DepartmentInvasionBegin
            self.isSkelecog = 0
            self.isV2 = 0
            self.isWaiter = 0
        else:
            msgType = ToontownGlobals.SuitInvasionBegin
            self.isSkelecog = 0
            self.isV2 = 0
            self.isWaiter = 0
        self.air.newsManager.setInvasionStatus(msgType, currentInvadingSuit,
                                               1000, self.isSkelecog)

    def alertPlayersInvasionEnded(self):
        currentInvadingSuit = self.currentInvadingSuit
        departmentInvasion = False
        if currentInvadingSuit == 'any':
            if self.currentInvadingDept == 'any':
                currentInvadingSuit = 'f'
            else:
                #Department invasion
                currentInvadingSuit = self.currentInvadingDept
                departmentInvasion = True
        if self.isSkelecog:
            msgType = ToontownGlobals.SkelecogInvasionEnd
            departmentInvasion = False
        elif self.isV2:
            msgType = ToontownGlobals.V2InvasionEnd
            departmentInvasion = False
        elif self.isWaiter:
            msgType = ToontownGlobals.WaiterInvasionEnd
            departmentInvasion = False
        elif departmentInvasion:
            msgType = ToontownGlobals.DepartmentInvasionEnd
        else:
            msgType = ToontownGlobals.SuitInvasionEnd
        self.air.newsManager.setInvasionStatus(msgType, currentInvadingSuit,
                                               1000, self.isSkelecog)

    def invasionStarted(self):
        t = self.MIN_TIME_DURING + random.randint(1, self.MAX_TIME_DURING)
        if t > self.MAX_TIME_DURING:
            t = self.MAX_TIME_DURING
        taskMgr.doMethodLater(t*60, self.cleanupInvasion, 'suitInvasionManager-cleanup')

    def startInvading(self):
        #Used for randomly spawning cog invasions. - No longer used.
        t = self.MIN_TIME_INBETWEEN + random.randint(1, self.MAX_TIME_INBETWEEN)
        if t > self.MAX_TIME_INBETWEEN:
            t = self.MAX_TIME_INBETWEEN
        taskMgr.doMethodLater(t*60, self.newInvasion, 'suitInvasionManager-invasion')

    def cleanupInvasion(self, task=None):
        self.invasionStatus = False
        self.alertPlayersInvasionEnded()
        self.currentInvadingSuit = None
        self.currentInvadingDept = None
        self.isSkelecog = 0
        self.isWaiter = 0
        self.isV2 = 0
        self.cleanupCurrentSuits()

        if task:
            return task.done

    def cleanupCurrentSuits(self):
        for suitPlanner in self.air.suitPlanners:
            self.air.suitPlanners.get(suitPlanner).flySuits()

    def cleanupTasks(self):
        taskMgr.remove('suitInvasionManager-cleanup')