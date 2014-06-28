#!/usr/bin/env python2
import StringIO
import copy
import json
import os
import shutil
import subprocess
import sys
import tarfile


print 'Starting the deployment process...'


print 'Reading deploy configuration...'
with open('deploy.json', 'r') as f:
    deployData = json.load(f)

with open('../PPYTHON_PATH', 'r') as f:
    ppythonPath = f.read()

platform = deployData['platform']
if platform not in ('win32',):  # Supported platforms
    print 'Unsupported platform:', platform
    sys.exit(1)

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
    sys.exit(2)
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
        '\rCollecting source code from branch:' + branch +
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
    sys.exit(2)
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
        '\rCollecting source code from branch:' + resourcesBranch +
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

print 'Platform:', platform
print 'Distribution:', distribution
print 'Branch:', branch
print 'Resources branch:', resourcesBranch
print 'Server version:', serverVersion
print 'Configuration directory:', configDir
print 'Virtual file system ({0}):'.format(len(vfsMounts))
for vfsMount in vfsMounts:
    print '  {0}'.format(vfsMount)

cmd = ''
if sys.platform == 'win32':
    cmd += ppythonPath + ' '
cmd += ('../tools/prepare_client.py'
        ' --distribution ' + distribution +
        ' --build-dir build' +
        ' --src-dir ..' +
        ' --server-ver ' + serverVersion +
        ' --build-mfs' +
        ' --resources-dir ../resources' +
        ' --config-dir ' + configDir +
        ' --include NonRepeatableRandomSourceUD.py' +
        ' --include NonRepeatableRandomSourceAI.py' +
        ' --exclude ServiceStart.py')
for vfsMount in vfsMounts:
    cmd += ' --vfs ' + vfsMount
os.system(cmd)
