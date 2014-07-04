#!/usr/bin/env python2
import json
import os
from pandac.PandaModules import *


username = os.environ['ttiUsername']
password = os.environ['ttiPassword']
distribution = ConfigVariableString('distribution', 'dev').getValue()


accountServerEndpoint = ConfigVariableString(
    'account-server-endpoint',
    'https://toontowninfinite.com/api/').getValue()

http = HTTPClient()
http.setVerifySsl(0)


def executeHttpRequest(url, message):
    channel = http.makeChannel(True)
    rf = Ramfile()
    spec = DocumentSpec(accountServerEndpoint + '/' + url)
    if channel.getDocument(spec) and channel.downloadToRam(rf):
        return rf.getData()


response = executeHttpRequest(
    'login?n={0}&p={1}&dist={2}'.format(username, password, distribution),
    username + password + distribution)




try:
    response = json.loads(response)
except ValueError:
    print "Couldn't verify account credentials."
else:
    if not response['success']:
        print response['reason']
    else:
        os.environ['TTI_PLAYCOOKIE'] = response['token']

        # Start the game:
        import toontown.toonbase.ClientStart
