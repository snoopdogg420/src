from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase import PythonUtil


class ToontownRPCDispatcher:
    notify = directNotify.newCategory('ToontownRPCDispatcher')

    def __init__(self, handler):
        self.handler = handler

    def dispatch(self, request):
        """
        Handle a JSON-RPC 2.0 request.
        """
        if (not isinstance(request.method, basestring)) or \
           (not isinstance(request.params, (tuple, list, dict))):
            request.error(-32600, 'Invalid Request')
            return

        # Grab the method from the handler:
        method = getattr(self.handler, 'rpc_' + request.method, None)
        if method is None:
            request.error(-32601, 'Method not found')
            return

        # Find the token in the params, authenticate it, and then remove it
        # from the params:
        token = None
        if isinstance(request.params, dict):
            token = request.params.get('token')
            del request.params['token']
        elif len(request.params) > 0:
            token = request.params[0]
            params = request.params[1:]
        if not isinstance(token, basestring):
            request.error(-32000, 'No token provided')
            return
        error = self.handler.authenticate(token, method)
        if error is not None:
            # Authentication wasn't successful. Send the error:
            request.error(*error)
            return

        # Finally, attempt to call the method:
        try:
            if method.deferResult:
                # This function wishes to handle the response itself. Pass the
                # request to it so it is capable of doing so:
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
            # the result ourselves:
            if not method.deferResult:
                request.result(result)
