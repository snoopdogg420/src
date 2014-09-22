class ToontownRPCHandler:
    def __init__(self, air):
        self.air = air

        for name in ToontownRPCHandler.__dict__:
            if name.startswith('rpc_'):
                func = getattr(self, name)
                name = name[4:]
                self.air.rpcServer.register_function(func, name=name)

    def rpc_test(self):
        print 'Received RPC request.'
