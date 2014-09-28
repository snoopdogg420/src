from direct.distributed.DistributedObjectUD import DistributedObjectUD

from toontown.uberdog.ClientServicesManagerUD import executeHttpRequest


class CentralLoggerUD(DistributedObjectUD):
    def sendMessage(self, category, description, sender, receiver):
        # TODO: Clean this up.
        if description == 'sys-hack':
            accountId = self.air.getAccountIdFromSender()
            if not accountId:
                return
            self.air.writeServerEvent('ban', accountId, 'sys-hack')
            executeHttpRequest('accounts/ban/', Id=accountId,
                               Release='0000-00-00', Reason='sys-hack')
        else:
            self.air.writeServerEvent(category, sender, receiver, eventString)

    def logAIGarbage(self):
        pass
