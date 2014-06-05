import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')

        self.notify.setInfo(True)

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        self.createGlobals()
        self.notify.info('Done.')

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                                                    'ClientServicesManager')

        self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER,
                                                          'ChatAgent')
        
        self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_TTR_FRIENDS_MANAGER,
                                                               'TTIFriendsManager')

        self.globalPartyMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        
        self.deliveryManager = simbase.air.generateGlobalObject(OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')