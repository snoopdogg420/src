from direct.distributed.MsgTypes import CLIENTAGENT_EJECT
from direct.distributed.PyDatagram import PyDatagram

from otp.distributed import OtpDoGlobals
from toontown.rpc.ToontownRPCHandlerBase import *


class ToontownRPCHandler(ToontownRPCHandlerBase):
    # --- TESTING ---

    @rpcmethod(accessLevel=COMMUNITY_MANAGER)
    def rpc_ping(self, data):
        """
        Summary:
            Responds with the [data] that was sent. This method exists only for
            testing purposes.

        Parameters:
            [str data] = The data to be given back in response.

        Example response: 'pong'
        """
        return data

    # --- MESSAGING ---

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_messageChannel(self, channel, message):
        """
        Summary:
            Broadcasts a [message] to any client whose Client Agent is
            subscribed to the provided [channel].

        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.

        Example response: None
        """
        dclass = self.air.dclassesByName['ClientServicesManagerUD']
        datagram = dclass.aiFormatUpdate(
            'systemMessage', OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER,
            channel, 1000000, [message])
        self.air.send(datagram)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_messageAll(self, message):
        """
        Summary: Broadcasts a [message] to all clients.

        Parameters:
            [str message] = The message to broadcast.

        Example response: None
        """
        self.rpc_messageChannel(10, message)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_messageShard(self, shardId, message):
        """
        Summary:
            Broadcasts a [message] to all clients under the provided [shardId].

        Parameters:
            [int shardId] = The ID of the shard to direct the message to.
            [str message] = The message to broadcast.

        Example response: None
        """
        # Get the DO ID of the district object:
        districtId = shardId + 1

        # Use it to get the uber zone's channel:
        channel = (districtId<<32) | 2

        self.rpc_messageChannel(channel, message)

    @rpcmethod(accessLevel=ADMINISTRATOR)
    def rpc_messageAccount(self, accountId, message):
        """
        Summary:
            Sends a [message] to the client associated with the provided
            [accountId].

        Parameters:
            [int accountId] = The ID of the account to direct the message to.
            [str message]   = The message to send.

        Example response: None
        """
        channel = accountId + (1003L<<32)
        self.rpc_messageChannel(channel, message)

    @rpcmethod(accessLevel=ADMINISTRATOR)
    def rpc_messageAvatar(self, avId, message):
        """
        Summary:
            Sends a [message] to the client associated with the provided
            [avId].

        Parameters:
            [int avId]    = The ID of the avatar to direct the message to.
            [str message] = The message to send.

        Example response: None
        """
        channel = avId + (1001L<<32)
        self.rpc_messageChannel(channel, message)

    # --- KICKS ---

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_kickChannel(self, channel, code, reason):
        """
        Summary:
            Kicks any client whose Client Agent is subscribed to the provided
            [channel].

        Parameters:
            [int channel] = The channel to direct the kick to.
            [int code]    = The code for the kick.
            [str reason]  = The reason for the kick.

        Example response: None
        """
        datagram = PyDatagram()
        datagram.addServerHeader(channel, self.air.ourChannel, CLIENTAGENT_EJECT)
        datagram.addUint16(code)
        datagram.addString(reason)
        self.air.send(datagram)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_kickAll(self, code, reason):
        """
        Summary: Kicks all clients.

        Parameters:
            [code]   = The code for the kick.
            [reason] = The reason for the kick.

        Example response: None
        """
        self.rpc_kickChannel(10, code, reason)

    @rpcmethod(accessLevel=SYSTEM_ADMINISTRATOR)
    def rpc_kickShard(self, shardId, code, reason):
        """
        Summary: Kicks all clients under the provided [shardId].

        Parameters:
            [int shardId] = The ID of the shard to direct the kick to.
            [int code]    = The code for the kick.
            [str reason]  = The reason for the kick.

        Example response: None
        """
        # Get the DO ID of the district object:
        districtId = shardId + 1

        # Use it to get the uber zone's channel:
        channel = (districtId<<32) | 2

        self.rpc_kickChannel(channel, code, reason)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_kickAccount(self, accountId, code, reason):
        """
        Summary: Kicks the client associated with the provided [accountId].

        Parameters:
            [int accountId] = The ID of the account to direct the kick to.
            [int code]      = The code for the kick.
            [str reason]    = The reason for the kick.

        Example response: None
        """
        channel = accountId + (1003L<<32)
        self.rpc_kickChannel(channel, code, reason)

    @rpcmethod(accessLevel=MODERATOR)
    def rpc_kickAvatar(self, avId, code, reason):
        """
        Summary: Kicks the client associated with the provided [avId].

        Parameters:
            [int avId]    = The ID of the avatar to direct the kick to.
            [int code]    = The code for the kick.
            [str reason]  = The reason for the kick.

        Example response: None
        """
        channel = avId + (1001L<<32)
        self.rpc_kickChannel(channel, code, reason)
