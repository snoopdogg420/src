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
        self.stopDouble = 0
        self.nameOfInterest = ''
        self.factory = ChatterBotFactory()
        self.engine = self.factory.create(ChatterBotType.CLEVERBOT)
        self.brain = self.engine.create_session()
        self.myTask = taskMgr.doMethodLater(0.5, self.tylerTask, 'tylerTask')
        self.index = 0
        
    def tylerTask(self, task):
        if task.time >= 5:
            self.index  = 0
        if task.time <= 25:
            return task.cont
        self.response('I guess you don\'t want to talk anymore %s' % self.nameOfInterest + '...', self.personOfInterest)
        self.stopDouble = self.personOfInterest
        self.personOfInterest = 0
        self.nameOfInterest = ''
        return task.done
        
    def restartTask(self):
        taskMgr.remove(self.myTask)
        taskMgr.add(self.myTask)

    def avatarEnter(self):
        if not self.personOfInterest:
            sender = self.air.getAvatarIdFromSender()
            if not sender == self.stopDouble:
                name = self.air.doId2do.get(sender).getName()
                self.personOfInterest = sender
                self.nameOfInterest = name
                self.sendUpdate('greet', [self.npcId, sender])
                self.brain = self.engine.create_session()
            else:
                self.sendUpdate('dismiss', [sender, 2])
                pass
        else:
            #Tyler is busy!
            pass
        
    def talkMessage(self, sender, message):
        if sender == self.personOfInterest:
            self.index += 1
            if self.index >= 4:
                self.stopDouble = self.personOfInterest
                self.personOfInterest = 0
                self.nameOfInterest = ''
                taskMgr.remove(self.myTask)
                self.index = 0
                self.sendUpdate('dismiss', [sender, 1])
                return
            self.restartTask()
            self.generateAnswer(message, sender)
            
    def generateAnswer(self, message, sender):
        name = self.air.doId2do.get(sender).getName()
        answer = self.brain.think(message)
        self.response(answer, sender)

    def response(self, response, sendTo):
        self.sendUpdate('respond', [self.npcId, response, sendTo])
        self.restartTask()
        
