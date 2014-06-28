#!/usr/bin/env python2
import os
import sys

import StringIO
import copy
import json
import shutil
import subprocess
import tarfile


print 'Starting the deployment process...'

missingFiles = False
for f in ('deploy.json', 'infinitecipher'):
    if sys.platform == 'win32':
        f += '.exe'
    if f not in os.listdir('.'):
        print 'WARNING: Missing file: {0}!'.format(f)
        missingFiles = True
if missingFiles:
    sys.exit(1)

print 'Reading deploy configuration...'
with open('deploy.json', 'r') as f:
    deployData = json.load(f)

if sys.platform == 'win32':
    with open('../PPYTHON_PATH', 'r') as f:
        pythonPath = f.read()
else:
    pythonPath = '/usr/bin/python2'

platform = deployData['platform']
if platform not in ('win32',):  # Supported platforms
    print 'Unsupported platform:', platform
    sys.exit(2)

distribution = deployData['distribution']

# Create a 'src' directory containing the desired branch's source files:
branch = deployData['branch']
sys.stdout.write('Collecting source code from branch: ' + branch + '... 0%')
sys.stdout.flush()
os.chdir('..')
branches = subprocess.Popen(
    ['git', 'rev-parse', '--abbrev-ref', '--branches', 'HEAD'],
    stdout=subprocess.PIPE).stdout.read().split()
if branch not in branches:
    print "No local branch named:", branch
    sys.exit(3)
if os.path.exists('deployment/src'):
    shutil.rmtree('deployment/src')
os.mkdir('deployment/src')
td = subprocess.Popen(
    ['git', 'archive', branch],
    stdout=subprocess.PIPE).stdout.read()
tss = StringIO.StringIO(td)
tf = tarfile.TarFile(fileobj=tss)
directories = []
members = tf.getmembers()
for (i, ti) in enumerate(members):
    if ti.isdir():
        directories.append(ti)
        ti = copy.copy(ti)
        ti.mode = 0o700
    tf.extract(ti, 'deployment/src')
    percentage = int((float(i+1)/len(members)) * 100)
    sys.stdout.write(
        '\rCollecting source code from branch: ' + branch +
        '... {0}%'.format(percentage))
    sys.stdout.flush()
directories.sort(key=lambda a: a.name)
directories.reverse()
for ti in directories:
    dirpath = os.path.join('deployment/src', ti.name)
    try:
        tf.chown(ti, dirpath)
        tf.utime(ti, dirpath)
        tf.chmod(ti, dirpath)
    except tarfile.ExtractError as e:
        if tf.errorlevel > 1:
            raise
        else:
            tf._dbg(1, 'tarfile: %s' % e)
sys.stdout.write('\n')
sys.stdout.flush()

# Export the resources from the desired resources branch to 'src/resources':
resourcesBranch = deployData['resources-branch']
sys.stdout.write('Collecting resources from branch: ' +
                 resourcesBranch + '... 0%')
sys.stdout.flush()
os.chdir('resources')
branches = subprocess.Popen(
    ['git', 'rev-parse', '--abbrev-ref', '--branches', 'HEAD'],
    stdout=subprocess.PIPE).stdout.read().split()
if resourcesBranch not in branches:
    print "No local resources branch named:", resourcesBranch
    sys.exit(3)
td = subprocess.Popen(
    ['git', 'archive', resourcesBranch],
    stdout=subprocess.PIPE).stdout.read()
tss = StringIO.StringIO(td)
tf = tarfile.TarFile(fileobj=tss)
os.chdir('../deployment')
directories = []
members = tf.getmembers()
for (i, ti) in enumerate(members):
    if ti.isdir():
        directories.append(ti)
        ti = copy.copy(ti)
        ti.mode = 0o700
    tf.extract(ti, 'src/resources')
    percentage = int((float(i+1)/len(members)) * 100)
    sys.stdout.write(
        '\rCollecting source code from branch: ' + resourcesBranch +
        '... {0}%'.format(percentage))
    sys.stdout.flush()
directories.sort(key=lambda a: a.name)
directories.reverse()
for ti in directories:
    dirpath = os.path.join('src/resources', ti.name)
    try:
        tf.chown(ti, dirpath)
        tf.utime(ti, dirpath)
        tf.chmod(ti, dirpath)
    except tarfile.ExtractError as e:
        if tf.errorlevel > 1:
            raise
        else:
            tf._dbg(1, 'tarfile: %s' % e)
sys.stdout.write('\n')
sys.stdout.flush()

serverVersion = deployData['version-prefix'] + deployData['version']
configDir = deployData['config-dir']
vfsMounts = deployData['vfs-mounts']
modules = deployData['modules']
mainModule = deployData['main-module']

print 'Platform:', platform
print 'Distribution:', distribution
print 'Branch:', branch
print 'Resources branch:', resourcesBranch
print 'Server version:', serverVersion
print 'Configuration directory:', configDir
print 'Virtual file system ({0}):'.format(len(vfsMounts))
for vfsMount in vfsMounts:
    print '  {0}'.format(vfsMount)
print 'Modules ({0}):'.format(len(modules))
for module in modules:
    print '  {0}'.format(module)
print 'Main module:', mainModule

cmd = (pythonPath + ' ../tools/prepare_client.py' +
       ' --distribution ' + distribution +
       ' --build-dir build' +
       ' --src-dir src' +
       ' --server-ver ' + serverVersion +
       ' --build-mfs' +
       ' --resources-dir src/resources' +
       ' --config-dir ' + configDir +
       ' --include NonRepeatableRandomSourceUD.py' +
       ' --include NonRepeatableRandomSourceAI.py' +
       ' --exclude ServiceStart.py')
for vfsMount in vfsMounts:
    cmd += ' --vfs ' + vfsMount
for module in modules:
    cmd += ' ' + module
os.system(cmd)

if sys.platform == 'win32':
    output = 'GameData.pyd'
else:
    output = 'GameData.so'
cmd = (pythonPath + ' ../tools/build_client.py' +
       ' --output ' + output +
       ' --main-module ' + mainModule +
       ' --build-dir build')
for module in modules:
    cmd += ' ' + module
os.system(cmd)

os.system('./infinitecipher GameData.pyd GameData.bin')
