UNKNOWN = 700
USER = 100
COMMUNITY_MANAGER = 200
MODERATOR = 300
ARTIST = 400
PROGRAMMER = 500
ADMINISTRATOR = 600
SYSTEM_ADMINISTRATOR = 700


class RPCMethod:
    def __init__(self, accessLevel=UNKNOWN):
        self.accessLevel = accessLevel

    def __call__(self, method):
        method.accessLevel = self.accessLevel
        return method


rpcmethod = RPCMethod


class ToontownRPCHandlerBase:
    def __init__(self, air):
        self.air = air
