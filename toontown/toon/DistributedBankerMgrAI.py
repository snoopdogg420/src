from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toon import NPCToons
from direct.distributed import ClockDelta
from toontown.estate.BankGlobals import *

class DistributedBankerMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBankerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.busy = 0

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendBankMovie(avId)

    def freeAvatar(self):
        self.sendExitMovie()
        self.sendClearMovie()

    def setMovie(self, mode, avId):
        self.sendUpdate('setMovie', args=[mode,
            avId, ClockDelta.globalClockDelta.getRealNetworkTime()])
        
    def sendBankMovie(self, avId):
        self.setMovie(BANK_MOVIE_GUI, avId)
        self.busy = avId
        
    def sendNotOwnerMovie(self, avId):
        self.setMovie(BANK_MOVIE_NOT_OWNER, avId)
        
    def sendExitMovie(self):
        self.setMovie(BANK_MOVIE_WITHDRAW, self.busy)
        
    def sendClearMovie(self):
        self.setMovie(BANK_MOVIE_CLEAR, self.busy)
        self.busy = 0

    def transferMoney(self, amount):
        av = self.air.doId2do.get(self.busy)
        if not av:
            return
        
        av.b_setBankMoney(min(av.getBankMoney() + amount, av.getMaxBankMoney()))
        av.b_setMoney(max(av.getMoney() - amount, 0))
        simbase.air.doFind('DistributedBankerBobNPCAI').sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TIMEOUT,
         2002,
         self.busy,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.freeAvatar()
    
    def __handleUnexpectedExit(self):
        self.busy = 0
