import base64
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.MsgTypes import CLIENTAGENT_EJECT
from direct.distributed.PyDatagram import PyDatagram
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


        # Sometimes we'll want to call the original method without security
        # checks:
        wrapper.callInternal = method

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
    def rpc_messageChannel(self, channel, message):
        """
        Summary:
            Broadcasts a [message] to any clients whose Client Agents are
            subscribed to the provided [channel].

        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.

        Returns: None
        """
        dclass = self.air.dclassesByName['ClientServicesManagerUD']
        datagram = dclass.aiFormatUpdate(
            'systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER,
            channel, 1000000, [message])
        self.air.send(datagram)

    @rpcmethod(accessLevel=700)
    def rpc_messageAll(self, message):
        """
        Summary: Broadcasts a [message] to all clients.

        Parameters:
            [str message] = The message to broadcast.

        Returns: None
        """
        self.rpc_messageChannel.callInternal(self, 10, message)

    @rpcmethod(accessLevel=700)
    def rpc_messageShard(self, shardId, message):
        """
        Summary:
            Broadcasts a [message] to all clients under the provided [shardId].

        Parameters:
            [int shardId] = The ID of the shard to direct the message to.
            [str message] = The message to broadcast.

        Returns: None
        """
        # Get the DO ID of the district object:
        districtId = shardId + 1

        # Use it to get the uber zone's channel:
        channel = (districtId<<32) | 2

        self.rpc_messageChannel.callInternal(self, channel, message)

    @rpcmethod(accessLevel=600)
    def rpc_messageAccount(self, accountId, message):
        """
        Summary:
            Sends a [message] to the client associated with the provided
            [accountId].

        Parameters:
            [int accountId] = The ID of the account to direct the message to.
            [str message]   = The message to send.

        Returns: None
        """
        channel = accountId + (1003L<<32)
        self.rpc_messageChannel.callInternal(self, channel, message)

    @rpcmethod(accessLevel=600)
    def rpc_messageAvatar(self, avId, message):
        """
        Summary:
            Sends a [message] to the client associated with the provided
            [avId].

        Parameters:
            [int avId]    = The ID of the avatar to direct the message to.
            [str message] = The message to send.

        Returns: None
        """
        channel = avId + (1001L<<32)
        self.rpc_messageChannel.callInternal(self, channel, message)

    @rpcmethod(accessLevel=700)
    def rpc_kickChannel(self, channel, code, reason):
        """
        Summary:
            Kicks any clients whose Client Agents are subscribed to the
            provided [channel].

        Parameters:
            [int channel] = The channel to direct the kick to.
            [int code]    = The code for the kick.
            [str reason]  = The reason for the kick.

        Returns: None
        """
        datagram = PyDatagram()
        datagram.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_EJECT)
        datagram.addUint16(code)
        datagram.addString(reason)
        self.air.send(datagram)

    @rpcmethod(accessLevel=700)
    def rpc_kickAll(self, code, reason):
        """
        Summary: Kicks all clients.

        Parameters:
            [code]   = The code for the kick.
            [reason] = The reason for the kick.

        Returns: None
        """
        self.rpc_kickChannel.callInternal(self, 10, code, reason)

    @rpcmethod(accessLevel=700)
    def rpc_kickShard(self, shardId, code, reason):
        """
        Summary: Kicks all clients under the provided [shardId].

        Parameters:
            [int shardId] = The ID of the shard to direct the kick to.
            [int code]    = The code for the kick.
            [str reason]  = The reason for the kick.

        Returns: None
        """
        # Get the DO ID of the district object:
        districtId = shardId + 1

        # Use it to get the uber zone's channel:
        channel = (districtId<<32) | 2

        self.rpc_kickChannel.callInternal(self, channel, code, reason)

    @rpcmethod(accessLevel=300)
    def rpc_kickAccount(self, accountId, code, reason):
        """
        Summary: Kicks the client associated with the provided [accountId].

        Parameters:
            [int accountId] = The ID of the account to direct the kick to.
            [int code]      = The code for the kick.
            [str reason]    = The reason for the kick.

        Returns: None
        """
        channel = accountId + (1003L<<32)
        self.rpc_kickChannel.callInternal(self, channel, code, reason)

    @rpcmethod(accessLevel=300)
    def rpc_kickAvatar(self, avId, code, reason):
        """
        Summary: Kicks the client associated with the provided [avId].

        Parameters:
            [int avId]    = The ID of the avatar to direct the kick to.
            [int code]    = The code for the kick.
            [str reason]  = The reason for the kick.

        Returns: None
        """
        channel = avId + (1001L<<32)
        self.rpc_kickChannel.callInternal(self, channel, code, reason)
