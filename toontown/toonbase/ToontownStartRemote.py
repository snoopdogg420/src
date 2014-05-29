import os


username = os.environ['ttiUsername']
password = os.environ['ttiPassword']


from pandac.PandaModules import *


accountServerEndpoint = ConfigVariableString('account-server-endpoint', 'https://www.toontowninfinite.com/api/').getValue()

http = HTTPClient()
http.setVerifySsl(0)


def executeHttpRequest(url, message):
    channel = http.makeChannel(True)
    rf = Ramfile()
    spec = DocumentSpec(accountServerEndpoint + '/' + url)
    if channel.getDocument(spec) and channel.downloadToRam(rf):
        return rf.getData()


response = executeHttpRequest(
    'login?n={0}&p={1}'.format(username, password),
    username + password)



import json


try:
    response = json.loads(response)
except ValueError:
    print 'Invalid username and/or password. Please try again.'
if not response['success']:
    print response['reason']
else:
    os.environ['TTI_PLAYCOOKIE'] = response['token']


    # Start the game:
    import toontown.toonbase.ToontownStart
