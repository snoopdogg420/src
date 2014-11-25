#!/usr/bin/env python2
import __builtin__
import base64
import json
import os
import sys
import time

from Crypto.Cipher import AES
import jsonrpclib


MAINTENANCE_MESSAGE = 'Attention Toons! Toontown Infinite is now going down for maintenance.'
MAINTENANCE_COUNTDOWN_MESSAGE = 'Attention Toons! Toontown Infinite will be going down for maintenance in %d minutes.'

# Notify the user if they are missing deploy.json:
if not os.path.exists('deploy.json'):
    print 'Missing file dependencies: deploy.json'
    sys.exit(2)

print 'Reading configuration...'
try:
    with open('deploy.json', 'r') as f:
        __builtin__.config = json.load(f)
except EnvironmentError:
    print 'Unable to read configuration...'
    sys.exit(3)

# Some configuration variables are required. Notify the user if they are
# missing any:
missingVars = []
for name in ('maintenance-countdown-duration', 'maintenance-lock-time',
             'maintenance-lock-message', 'game-rpc-endpoint',
             'game-rpc-token-secret', 'web-rpc-endpoint',
             'web-rpc-token-secret'):
    if name not in config:
        missingVars.append(name)
if missingVars:
    print 'Missing configuration variables:', ', '.join(missingVars)
    sys.exit(4)

__builtin__.gameRpc = jsonrpclib.Server(config['game-rpc-endpoint'])
__builtin__.webRpc = jsonrpclib.Server(config['web-rpc-endpoint'])

gameRpcTokenSecret = config['game-rpc-token-secret']
webRpcTokenSecret = config['web-rpc-token-secret']


def generate_token(secret, accessLevel=700):
    token = {
        'timestamp': int(time.mktime(time.gmtime())),
        'accesslevel': accessLevel
    }
    plainText = json.dumps(token)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(secret, mode=AES.MODE_CBC, IV=iv)
    plainText += '\x00' * (AES.block_size - (len(plainText)%AES.block_size))
    return base64.b64encode(iv + cipher.encrypt(plainText))


duration = config['maintenance-countdown-duration']
lockTime = config['maintenance-lock-time']
lockMessage = config['maintenance-lock-message']

# If our countdown duration is less than the lock time, then tell the account
# server to begin rejecting login attempts immediately:
if duration < lockTime:
    # webRpc.toggleMaintenance(generate_token(webRpcTokenSecret), 0, lockMessage)
    webRpc.toggleMaintenance(0, lockMessage)

# Begin the countdown:
while duration > 0:
    gameRpc.messageAll(generate_token(gameRpcTokenSecret),
                       MAINTENANCE_COUNTDOWN_MESSAGE % duration)
    if duration == lockTime:
        # Tell the account server to begin rejecting login attempts:
        # webRpc.toggleMaintenance(generate_token(webRpcTokenSecret), 0, lockMessage)
        webRpc.toggleMaintenance(0, lockMessage)
    if duration <= 5:
        # Count down every minute:
        time.sleep(60)
        duration -= 1
    elif duration % 5:
        # Count down to the nearest multiple of 5 in minutes:
        time.sleep((duration%5) * 60)
        duration -= duration % 5
    else:
        # Count down every 5 minutes:
        duration.sleep(300)
        duration -= 5

gameRpc.messageAll(generate_token(gameRpcTokenSecret), MAINTENANCE_MESSAGE)
