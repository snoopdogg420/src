from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task.Task import Task
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

        self.sockets = []
        self.connections = {}

        self.pollTask = None

        # Parse the endpoint URL:
        url = urlparse.urlparse(endpoint)
        if url.scheme != 'http':
            self.notify.error('invalid endpoint URL scheme: ' + url.scheme)

        hostname = url.hostname or 'localhost'
        port = url.port or 8080

        # Create a listener socket to watch for incoming connections:
        self.listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenerSocket.setblocking(0)
        self.listenerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listenerSocket.bind((hostname, port))
        self.listenerSocket.listen(5)

    def start(self):
        # If we don't have a dedicated task chain, create one:
        if not taskMgr.hasTaskChain('RPCServer'):
            taskMgr.setupTaskChain('RPCServer', numThreads=1,
                                   threadPriority=TP_normal, frameBudget=0.001,
                                   frameSync=True)

        # Start polling:
        self.pollTask = taskMgr.add(self.poll, 'pollTask', taskChain='RPCServer')

    def stop(self):
        if self.pollTask is None:
            return

        taskMgr.remove(self.pollTask)
        self.pollTask = None

        for connection in self.connections:
            connection.close()

        self.sockets = []
        self.connections = {}

    def poll(self, task=None):
        try:
            r = select.select([self.listenerSocket] + self.sockets, [], [])[0]
        except:
            # One or more of our sockets might have become invalid.

            # If our listener socket has, we can't continue:
            self.listenerSocket.fileno()

            # Otherwise, discard the socket(s) that have, and wait for the next
            # poll iteration:
            for k, v in self.sockets.items():
                try:
                    v.fileno()
                    v.getpeername()
                except:
                    del self.sockets[k]

            return Task.cont

        if self.listenerSocket in r:
            try:
                conn = self.listenerSocket.accept()[0]
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    return Task.cont
                raise e
            self.sockets.append(conn)
            self.connections[conn.fileno()] = ToontownRPCConnection(conn, self.handler)

        for sock in r:
            fileno = sock.fileno()
            connection = self.connections.get(fileno)
            if connection is None:
                continue
            try:
                connection.dispatchUntilEmpty()
            except:
                pass
            finally:
                connection.close()
                self.sockets.remove(sock)
                del self.connections[fileno]

        if task is not None:
            return Task.cont
