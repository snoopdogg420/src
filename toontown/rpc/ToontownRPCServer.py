from direct.directnotify.DirectNotifyGlobal import directNotify
import errno
from panda3d.core import TP_normal
import select
import socket
import urlparse

from toontown.rpc.ToontownRPCConnection import ToontownRPCConnection


class ToontownRPCServer:
    notify = directNotify.newCategory('ToontownRPCServer')

    def __init__(self, endpoint, handler):
        self.handler = handler

        # Parse the endpoint:
        url = urlparse.urlparse(endpoint)

        # We only support the http scheme:
        if url.scheme != 'http':
            self.notify.warning('Invalid scheme for endpoint: ' + str(url.scheme))

        # Parse the hostname, and port:
        self.hostname = url.hostname or 'localhost'
        self.port = url.port or 8080

        self.listenerSocket = None
        self.connections = {}

    def getUniqueName(self):
        """
        Returns a unique identifier for this instance. This is primarily used
        for creating unique task names.
        """
        return 'ToontownRPCServer-' + str(id(self))

    def start(self, useTaskChain=False):
        """
        Serve until stop() is called.
        """
        taskChain = None
        if useTaskChain and (not taskMgr.hasTaskChain('ToontownRPCServer')):
            taskChain = 'ToontownRPCServer'
            taskMgr.setupTaskChain(taskChain, numThreads=1, threadPriority=TP_normal)

        # Create a socket to listen for incoming connections:
        self.listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenerSocket.setblocking(0)
        self.listenerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listenerSocket.bind((self.hostname, self.port))
        self.listenerSocket.listen(5)

        # Start polling:
        taskName = self.getUniqueName() + '-pollTask'
        taskMgr.add(self.pollTask, taskName, taskChain=taskChain)

    def stop(self):
        """
        Stop serving.
        """
        # Stop polling:
        taskName = self.getUniqueName() + '-pollTask'
        assert taskMgr.hasTaskNamed(taskName)
        taskMgr.remove(taskName)

        # Close any open connections:
        for k, v in self.connections.items():
            v.close()
            del self.connections[k]

        # Shutdown and close the listener socket:
        try:
            self.listenerSocket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.listenerSocket.close()
        self.listenerSocket = None

    def pollOnce(self):
        """
        Poll for incoming data once.
        """
        rlist = select.select([self.listenerSocket] + self.connections.keys(), [], [])[0]

        if self.listenerSocket in rlist:
            self.handleNewConnection()

        for socket in rlist:
            connection = self.connections.get(socket)
            if connection is None:
                continue
            connection.dispatchUntilEmpty()
            connection.close()
            del self.connections[socket]

    def pollTask(self, task):
        """
        Continuously poll for incoming data.
        """
        self.pollOnce()
        return task.cont

    def handleNewConnection(self):
        """
        Handle an incoming connection.
        """
        try:
            conn = self.listenerSocket.accept()[0]
        except socket.error, e:
            if e.args[0] != errno.EWOULDBLOCK:
                raise e
        self.connections[conn] = ToontownRPCConnection(conn, self.handler)
