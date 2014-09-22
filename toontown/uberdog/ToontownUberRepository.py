from direct.distributed.PyDatagram import *
from direct.task.Task import Task
import urlparse

from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
import toontown.minigame.MinigameCreatorAI


if config.GetBool('want-rpc-server', False):
    from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
    from toontown.rpc.ToontownRPCHandler import ToontownRPCHandler


class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')

        self.notify.setInfo(True)

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', False):
            rpcServerEndpoint = config.GetString('rpc-server-endpoint', 'http://localhost:8080/')
            url = urlparse.urlparse(rpcServerEndpoint)

            if url.scheme != 'http':
                self.notify.error('Invalid scheme for RPC server endpoint: %s' % url.scheme)

            hostname = url.hostname or 'localhost'
            port = url.port or 8080

            self.rpcServer = SimpleJSONRPCServer((hostname, port), logRequests=False)
            self.rpcHandler = ToontownRPCHandler(self)

            taskMgr.setupTaskChain(
                'RPCServer', numThreads=1, threadPriority=TP_normal,
                frameBudget=0.001, frameSync=True)
            taskMgr.add(self.rpcServerPollTask, 'RPCServer-poll',
                        taskChain='RPCServer')

        self.createGlobals()
        self.notify.info('Done.')

    def rpcServerPollTask(self, task):
        self.rpcServer.handle_request()
        return Task.cont

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                                                    'ClientServicesManager')

        self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER,
                                                          'ChatAgent')

        self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_TTI_FRIENDS_MANAGER,
                                                               'TTIFriendsManager')

        self.globalPartyMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')

        self.deliveryManager = simbase.air.generateGlobalObject(OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')
