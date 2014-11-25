from direct.directnotify.DirectNotifyGlobal import directNotify
import urlparse


class ToontownRPCClient:
    notify = directNotify.newCategory('ToontownRPCClient')

    def __init__(self, endpoint):
        # Parse the endpoint:
        url = urlparse.urlparse(endpoint)

        # We only support the http scheme:
        if url.scheme != 'http':
            self.notify.error('Invalid scheme for endpoint: ' + str(url.scheme))

        # Parse the hostname, and port:
        self.hostname = url.hostname or 'localhost'
        self.port = url.port or 8080
