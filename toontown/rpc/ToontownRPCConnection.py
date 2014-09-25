from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase import PythonUtil
from direct.stdpy import threading
from direct.stdpy import threading2
import httplib
import json
import socket
import time


class ToontownRPCRequest:
    def __init__(self, connection, id=None):
        self.connection = connection
        self.id = id

    def result(self, result):
        # If this isn't a notification, send the response:
        if self.id is not None:
            self.connection.writeJSONResponse({'result': result}, id=self.id)

    def error(self, code, message):
        self.connection.writeJSONError(code, message, id=self.id)


class ToontownRPCConnection:
    notify = directNotify.newCategory('ToontownRPCConnection')

    def __init__(self, socket, handler):
        self.socket = socket
        self.handler = handler

        self.readBuffer = ''

        self.socketLock = threading.Lock()
        self.readLock = threading.RLock()
        self.writeLock = threading.RLock()

        self.writeQueue = []
        self.writeSemaphore = threading.Semaphore(0)
        self.writeThread = threading.Thread(target=self.__writeThread)
        self.writeThread.start()

    def __readHeaders(self):
        self.readLock.acquire()

        # Read data until we find the '\r\n\r\n' terminator:
        while '\r\n\r\n' not in self.readBuffer:
            try:
                self.readBuffer += self.socket.recv(2048)
            except:
                self.readLock.release()
                return {}

            if not self.readBuffer:
                # It looks like we have nothing to read.
                self.readLock.release()
                return {}

        # Collect the data before the terminator:
        terminatorIndex = self.readBuffer.find('\r\n\r\n')
        data = self.readBuffer[:terminatorIndex]

        # Truncate the remaining data:
        self.readBuffer = self.readBuffer[terminatorIndex + 4:]

        # We're done working with the read buffer, so:
        self.readLock.release()

        # Return the parsed headers in the form of a dictionary:
        return self.__parseHeaders(data)

    def __parseHeaders(self, data):
        headers = {}

        for i, line in enumerate(data.split('\n')):
            line = line.rstrip('\r')

            if i == 0:
                # This is the HTTP request.
                words = line.split(' ')
                if len(words) != 3:
                    self.writeHTTPError(400)
                    return {}

                command, _, version = words

                if command != 'POST':
                    self.writeHTTPError(501)
                    return {}

                if version not in ('HTTP/1.0', 'HTTP/1.1'):
                    self.writeHTTPError(505)
                    return {}
            else:
                # This is an HTTP header.
                words = line.split(': ')
                if len(words) != 2:
                    self.writeHTTPError(400)
                    return {}

                headers[words[0].lower()] = words[1]

        return headers

    def read(self, timeout=None):
        self.socketLock.acquire()
        self.socket.settimeout(timeout)

        # Read our HTTP headers:
        headers = self.__readHeaders()

        if not headers:
            # It looks like we have nothing to read.
            self.socketLock.release()
            return ''

        # We need a content-length in order to read POST data:
        contentLength = headers.get('content-length', '')
        if (not contentLength) or (not contentLength.isdigit()):
            self.writeHTTPError(400)
            self.socketLock.release()
            return ''

        contentLength = int(contentLength)

        # Read data until we have enough in our read buffer:
        self.readLock.acquire()

        while len(self.readBuffer) < contentLength:
            try:
                self.readBuffer += self.socket.recv(2048)
            except:
                self.readLock.release()
                self.socketLock.release()
                return ''

            if not self.readBuffer:
                # It looks like we have nothing to read:
                self.readLock.release()
                self.socketLock.release()
                return ''

        # Collect the content:
        data = self.readBuffer[:contentLength]

        # Truncate the remaining data:
        self.readBuffer = self.readBuffer[contentLength + 1:]

        self.readLock.release()
        self.socketLock.release()

        return data

    def __writeNow(self, data, timeout=None):
        self.writeLock.acquire()
        self.socket.settimeout(timeout)

        # Ensure the data ends with a new line:
        if not data.endswith('\n'):
            data += '\n'

        while data:
            try:
                sent = self.socket.send(data)
            except:
                break
            if sent == 0:
                break
            data = data[sent:]

        self.writeLock.release()

    def __writeThread(self):
        while True:
            self.writeSemaphore.acquire()

            # Ensure we have a request in the queue:
            if not self.writeQueue:
                continue

            request = self.writeQueue.pop(0)

            abort = request.get('abort')
            if abort is not None:
                # Clear the write queue, and stop:
                self.writeQueue = []
                abort.set()
                break

            # Write the data immediately:
            data = request.get('data')
            if data:
                self.__writeNow(data, timeout=request.get('timeout'))

    def write(self, data, timeout=None):
        self.writeQueue.append({'data': data, 'timeout': timeout})
        self.writeSemaphore.release()

    def close(self):
        abort = threading2.Event()
        self.writeQueue.append({'abort': abort})
        self.writeSemaphore.release()
        abort.wait()

        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.socket.close()

    def writeHTTP(self, body, contentType='text/plain', code=200):
        # First, look up a description for the code:
        description = httplib.responses.get(code)

        # Prepare the response:
        response = 'HTTP/1.1 %d %s\r\n' % (code, description)

        # Add the standard headers:
        response += 'Date: %s\r\n' % time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        response += 'Server: TTI-RPCServer/0.1\r\n'

        # Add the content headers:
        response += 'Content-Length: %d\r\n' % len(body)
        if contentType is not None:
            response += 'Content-Type: %s\r\n' % contentType

        # Add the body:
        response += '\r\n' + body

        # Finally, send it out:
        self.write(response, timeout=5)

    def writeHTTPError(self, code):
        self.notify.warning('Received a bad HTTP request: ' + str(code))
        body = '%d %s' % (code, httplib.responses.get(code))
        self.writeHTTP(body, code=code)

    def writeJSON(self, object):
        try:
            body = json.dumps(object)
        except TypeError:
            self.writeJSONError(-32603, 'Internal error')
            return
        self.writeHTTP(body, contentType='application/json')

    def writeJSONResponse(self, response, id=None):
        response.update({'jsonrpc': '2.0', 'id': id})
        self.writeJSON(response)

    def writeJSONError(self, code, message, id=None):
        self.notify.warning('Received a bad JSON request: %d %s' % (code, message))
        response = {'error': {'code': code, 'message': message}}
        self.writeJSONResponse(response, id=id)

    def dispatch(self, methodName, params=(), id=None):
        # Grab the method from the handler:
        method = getattr(self.handler, 'rpc_' + methodName, None)
        if method is None:
            self.writeJSONError(-32601, 'Method not found', id=id)
            return

        # Find the token in the params, and remove it:
        token = None
        if isinstance(params, dict):
            token = params.get('token')
            del params['token']
        elif len(params) > 0:
            token = params[0]
            params = params[1:]
        if not isinstance(token, basestring):
            self.writeJSONError(-32000, 'No token provided', id=id)
            return

        # Authenticate the provided token:
        error = self.handler.authenticate(token, method)
        if error is not None:
            # Authentication wasn't successful. Send the error:
            self.writeJSONError(*error, id=id)
            return

        # Attempt to call the method:
        request = ToontownRPCRequest(self, id=id)
        try:
            if method.deferResult:
                # This function is going to handle the response itself. Pass
                # the request over to it:
                if isinstance(params, dict):
                    method(request, **params)
                else:
                    method(request, *params)
            else:
                if isinstance(params, dict):
                    result = method(**params)
                else:
                    result = method(*params)
        except:
            request.error(-32603, PythonUtil.describeException())
        else:
            # If the method isn't going to handle the response itself, send out
            # the result:
            if not method.deferResult:
                request.result(result)

    def dispatchUntilEmpty(self):
        while True:
            data = self.read(timeout=5)

            if not data:
                # We have nothing left to read.
                break

            try:
                request = json.loads(data)
            except ValueError:
                self.writeJSONError(-32700, 'Parse error')
                continue

            method = request.get('method')
            params = request.get('params') or ()
            id = request.get('id')

            if not isinstance(method, basestring):
                self.writeJSONError(-32600, 'Invalid Request', id=id)
                continue

            if not isinstance(params, (tuple, list, dict)):
                self.writeJSONError(-32600, 'Invalid Request', id=id)
                continue

            dispatchThread = threading.Thread(
                target=self.dispatch, args=[method, params, id])
            dispatchThread.start()
