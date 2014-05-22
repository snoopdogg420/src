from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.quest import Quests
import time
from QuestionMgr import ChatterBotFactory, ChatterBotType
from direct.task import Task

class DistributedSmartNPCAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.air = air
        self.personOfInterest = 0
        self.nameOfInterest = ''
        self.factory = ChatterBotFactory()
        self.engine = self.factory.create(ChatterBotType.CLEVERBOT)
        self.brain = self.engine.create_session()
        self.myTask = taskMgr.doMethodLater(2, self.timeoutTask, 'timeoutTask')
        self.setPos(0, 0, 0)
        self.setHpr(0, 0, 0)
        
    def timeoutTask(self, task):
        if task.time <= 20:
            return task.cont
        self.response('I guess you don\'t want to talk anymore %s' % self.nameOfInterest + '...', self.personOfInterest)
        self.personOfInterest = 0
        self.nameOfInterest = ''
        return task.done
        
    def restartTask(self):
        taskMgr.remove(self.myTask)
        taskMgr.add(self.myTask)

    def avatarEnter(self):
        if not self.personOfInterest:
            avId = self.air.getAvatarIdFromSender()
            name = self.air.doId2do.get(avId).getName()
            self.personOfInterest = avId
            self.nameOfInterest = name
            self.sendUpdate('greet', [self.npcId, avId])
            self.brain = self.engine.create_session()
        else:
            #Tyler is busy!
            pass
        
    def talkMessage(self, sender, message):
        if sender == self.personOfInterest:
            self.restartTask()
            self.generateAnswer(message, sender)
            
    def generateAnswer(self, message, sender):
        name = self.air.doId2do.get(sender).getName()
        answer = self.brain.think(message)
        self.response(answer, sender)
        
    def response(self, response, sendTo):
        self.sendUpdate('respond', [self.npcId, response, sendTo])
        self.restartTask()
        
