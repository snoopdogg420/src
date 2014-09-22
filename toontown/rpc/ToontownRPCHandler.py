import base64
from direct.directnotify.DirectNotifyGlobal import directNotify
import json
import time

from Crypto.Cipher import AES

from otp.distributed import OtpDoGlobals


class RPCMethod:
    def __init__(self, accessLevel=600):
        self.accessLevel = accessLevel

    def __call__(self, method):
        accessLevel = self.accessLevel


        def wrapper(self, token, *args, **kwds):
            # First, base64 decode the token:
            try:
                token = base64.b64decode(token)
            except TypeError:
                self.notify.warning("Couldn't decode the provided token.")
                return "Couldn't decode the provided token."

            # Ensure this token is a valid size:
            if (not token) or ((len(token) % 16) != 0):
                self.notify.warning('Invalid token length.')
                return 'Invalid token length.'

            # Next, decrypt the token using AES-128 in CBC mode:
            rpcServerSecret = config.GetString(
                'rpc-server-secret', '6163636f756e7473')

            # Ensure that our secret is the correct size:
            if len(rpcServerSecret) > AES.block_size:
                self.notify.warning('rpc-server-secret is too big!')
                rpcServerSecret = rpcServerSecret[:AES.block_size]
            elif len(rpcServerSecret) < AES.block_size:
                self.notify.warning('rpc-server-secret is too small!')
                rpcServerSecret += '\x80'
                while len(rpcServerSecret) < AES.block_size:
                    rpcServerSecret += '\x00'

            # Take the initialization vector off the front of the token:
            iv = token[:AES.block_size]

            # Truncate the token to get our cipher text:
            cipherText = token[AES.block_size:]

            # Decrypt!
            cipher = AES.new(rpcServerSecret, mode=AES.MODE_CBC, IV=iv)
            try:
                token = json.loads(cipher.decrypt(cipherText).replace('\x00', ''))
                if ('timestamp' not in token) or (not isinstance(token['timestamp'], int)):
                    raise ValueError
                if ('accesslevel' not in token) or (not isinstance(token['accesslevel'], int)):
                    raise ValueError
            except ValueError:
                self.notify.warning('Invalid token.')
                return 'Invalid token.'

            # Next, check if this token has expired:
            expiration = config.GetInt('rpc-token-expiration', 5)
            delta = int(time.time()) - token['timestamp']
            if delta > expiration:
                self.notify.warning('The provided token has expired.')
                return 'The provided token has expired.'

            if token['accesslevel'] < accessLevel:
                return 'Insufficient access.'

            return method(self, *args, **kwds)


        return wrapper


rpcmethod = RPCMethod


class ToontownRPCHandler:
    notify = directNotify.newCategory('ToontownRPCHandler')

    def __init__(self, air):
        self.air = air

        for name in ToontownRPCHandler.__dict__:
            if name.startswith('rpc_'):
                func = getattr(self, name)
                name = name[4:]
                self.air.rpcServer.register_function(func, name=name)

    @rpcmethod(accessLevel=700)
    def rpc_systemMessage(self, message):
        """
        Broadcast a <message> to the game server.
        """
        message = 'ADMIN: ' + message
        dclass = self.air.dclassesByName['ClientServicesManagerUD']
        datagram = dclass.aiFormatUpdate(
            'systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER,
            10, 1000000, [message])
        self.air.send(datagram)
