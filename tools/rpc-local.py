from jsonrpclib import Server
import time
import json
import os
from Crypto.Cipher import AES
import base64


RPC_SERVER_SECRET = '6163636f756e7473'


client = Server('http://127.0.0.1:8080/')


def generate_token(accessLevel):
    """
    Generate an RPC server token with the given access level.
    """
    token = {'timestamp': int(time.mktime(time.gmtime())), 'accesslevel': accessLevel}
    data = json.dumps(token)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(RPC_SERVER_SECRET, mode=AES.MODE_CBC, IV=iv)
    data += '\x00' * (16 - (len(data)%AES.block_size))
    token = cipher.encrypt(data)
    return base64.b64encode(iv + token)


while True:
    methodCall = raw_input('>')
    if methodCall.endswith('()'):
        extraParam = 'generate_token(700)'
    else:
        extraParam = 'generate_token(700), '
    methodCall = 'client.' + methodCall[:methodCall.find('(') + 1] + extraParam + methodCall[methodCall.find('(') + 1:]
    try:
        exec('print ' + methodCall)
    except Exception, e:
        print e
