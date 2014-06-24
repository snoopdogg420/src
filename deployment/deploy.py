#!/usr/bin/env python2
import json
import os


print 'Starting the deployment process...'


with open('deploy.json', 'r') as f:
    deployData = json.load(f)

with open('../PPYTHON_PATH', 'r') as f:
    ppythonPath = f.read()

distribution = deployData['distribution']
branch = deployData['branch']
resourcesBranch = deployData['resources-branch']
serverVersion = deployData['version-prefix'] + deployData['version']
configDir = deployData['config-dir']
vfsMounts = deployData['vfs-mounts']

print 'Distribution:', distribution
print 'Branch:', branch
print 'Resources branch:', resourcesBranch
print 'Server version:', serverVersion
print 'Configuration directory:', configDir
print 'Virtual file system ({0}):'.format(len(vfsMounts))
for vfsMount in vfsMounts:
    print '  {0}'.format(vfsMount)

cmd = (ppythonPath + ' ../tools/prepare_client.py '
       '--distribution ' + distribution + ' --build-dir build --src-dir .. '
       '--server-ver ' + serverVersion + ' --build-mfs '
       '--resources-dir ../resources --config-dir ' + configDir +
       ' --include NonRepeatableRandomSourceUD.py'
       ' --include NonRepeatableRandomSourceAI.py'
       ' --exclude ServiceStart.py')
for vfsMount in vfsMounts:
    cmd += ' --vfs {0}'.format(vfsMount)
os.system(cmd)
