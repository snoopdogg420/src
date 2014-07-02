#!/usr/bin/env python2
import StringIO
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from xml.etree import ElementTree

import bz2


# We have some dependencies that aren't in the standard Python library. Notify
# the user if they are missing one:
try:
    import boto
    from boto.s3.key import Key
    from boto.cloudfront import CloudFrontConnection
except ImportError:
    print 'Missing dependency: boto'
    print 'It is recommended that you install this using Pip.'
    sys.exit(1)
try:
    import requests
except ImportError:
    print 'Missing dependency: requests'
    print 'It is recommended that you install this using Pip.'
    sys.exit(1)

print 'Starting the deployment process...'

# Stop the user if they are missing vital files:
missingFiles = False
for filename in ('deploy.json', 'infinitecipher'):
    if sys.platform == 'win32':
        # On the Windows platform if there is no extension we can infer that
        # this is an executable file. Therefore, let's append the '.exe'
        # extension:
        if not os.path.splitext(filename)[1]:
            filename += '.exe'
    if filename not in os.listdir('.'):
        print 'Missing file:', filename
        missingFiles = True
if missingFiles:
    sys.exit(1)

print 'Reading deploy configuration...'
with open('deploy.json', 'r') as f:
    deployData = json.load(f)

if sys.platform == 'win32':
    with open('../PPYTHON_PATH', 'r') as f:
        pythonPath = f.read().strip()
else:
    pythonPath = '/usr/bin/python2'

bucketName = deployData['bucket-name']
awsCfDistributionId = deployData['aws-cf-distribution-id']
awsAccessKeyId = deployData['aws-access-key-id']
if not awsAccessKeyId:
    print 'Missing AWS access key ID.'
    sys.exit(1)
awsSecretAccessKey = deployData['aws-secret-access-key']
if not awsSecretAccessKey:
    print 'Missing AWS secret access key.'
    sys.exit(1)

platform = deployData['platform']
if platform not in ('win32', 'linux'):  # Supported platforms
    print 'Unsupported platform:', platform
    sys.exit(2)

distribution = deployData['distribution']

# Check if the desired branch exists:
branch = deployData['branch']
os.chdir('..')
branches = subprocess.Popen(
    ['git', 'rev-parse', '--abbrev-ref', '--branches', 'HEAD'],
    stdout=subprocess.PIPE).stdout.read().split()
if branch not in branches:
    print "No local branch named:", branch
    sys.exit(3)

# Check if the desired resources branch exists:
resourcesBranch = deployData['resources-branch']
os.chdir('../ToontownInfiniteResources')
branches = subprocess.Popen(
    ['git', 'rev-parse', '--abbrev-ref', '--branches', 'HEAD'],
    stdout=subprocess.PIPE).stdout.read().split()
if resourcesBranch not in branches:
    print "No local resources branch named:", resourcesBranch
    sys.exit(3)

serverVersion = deployData['version-prefix'] + deployData['version']
launcherVersion = deployData['launcher-version']
accountServer = deployData['account-server']
clientAgent = deployData['client-agent']
patcherIncludes = deployData['patcher-includes']
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

# Create a 'src' directory containing the desired branch's source files:
sys.stdout.write('Collecting source code from branch: ' + branch + '... 0%')
sys.stdout.flush()
os.chdir('../ToontownInfinite')
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
sys.stdout.write('Collecting resources from branch: ' +
                 resourcesBranch + '... 0%')
sys.stdout.flush()
os.chdir('../ToontownInfiniteResources')
td = subprocess.Popen(
    ['git', 'archive', resourcesBranch],
    stdout=subprocess.PIPE).stdout.read()
tss = StringIO.StringIO(td)
tf = tarfile.TarFile(fileobj=tss)
os.chdir('../ToontownInfinite/deployment')
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

os.chdir('build')
if sys.platform == 'win32':
    os.system('..\infinitecipher {0} GameData.bin'.format(output))
else:
    os.system('../infinitecipher {0} GameData.bin'.format(output))

os.chdir('..')
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.mkdir('dist')

# Next, if a patcher.xml exists for this distribution, let's read it and assess
# what resources need to be updated. This is necessary because multifile hashes
# change each time they are compiled:
request = requests.get('http://cdn.toontowninfinite.com/{0}/{1}/patcher.xml'.format(distribution, platform))
root = ElementTree.fromstring(request.text)
everything = True
updated = []
if root.tag != 'Error':
    resourcesRevision = root.find('resources-revision')
    if resourcesRevision:
        everything = False
        resourcesRevision = resourcesRevision.text
        os.chdir('../../ToontownInfiniteResources')
        diff = subprocess.Popen(
            ['git', 'diff', '--name-only', resourcesRevision, resourcesBranch],
            stdout=subprocess.PIPE).stdout.read()
        filenames = diff.split('\n')
        for filename in filenames:
            directory = filename.split('/', 1)[0].split('\\', 1)[0]
            if directory.startswith('phase_') and (directory not in updated):
                updated.append(directory + '.mf')
        os.chdir('../ToontownInfinite/deployment')
resourcesRevision = subprocess.Popen(
    ['git', 'rev-parse', resourcesBranch],
    stdout=subprocess.PIPE).stdout.read()[:7]

cmd = (pythonPath + ' ../tools/write_patcher.py' +
       ' --build-dir build' +
       ' --dest-dir dist' +
       ' --output patcher.xml' +
       ' --launcher-version ' + launcherVersion +
       ' --account-server ' + accountServer +
       ' --client-agent ' + clientAgent +
       ' --server-version ' + serverVersion +
       ' --resources-revision ' + resourcesRevision)
for include in patcherIncludes:
    cmd += ' ' + include
os.system(cmd)


def compressFile(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    filename = os.path.basename(filepath)
    directory = filepath[6:].split(filename, 1)[0]
    if not os.path.exists(os.path.join('dist', directory)):
        os.mkdir(os.path.join('dist', directory))
    bz2Filename = os.path.splitext(filename)[0] + '.bz2'
    bz2Filepath = os.path.join('dist', directory, bz2Filename)
    f = bz2.BZ2File(bz2Filepath, 'w')
    f.write(data)
    f.close()


def getFileMD5Hash(filepath):
    md5 = hashlib.md5()
    bufferSize = 128 * md5.block_size
    with open(filepath, 'rb') as f:
        block = f.read(bufferSize)
        while block:
            md5.update(block)
            block = f.read(bufferSize)
    return md5.hexdigest()


localRoot = ElementTree.parse('dist/patcher.xml').getroot()
for directory in localRoot.findall('directory'):
    if directory.get('name') == 'resources':
        if not everything:
            for child in directory.getchildren():
                if child.get('name') not in updated:
                    size = ''
                    hash = ''
                    for _directory in root.findall('directory'):
                        if _directory.get('name') != 'resources':
                            continue
                        for _child in _directory.getchildren():
                            if _child.get('name') == child.get('name'):
                                size = child.find('size').text
                                hash = child.find('hash').text
                    child.find('size').text = size
                    child.find('hash').text = hash
        else:
            for child in directory.getchildren():
                updated.append(child.get('name'))
    else:
        directoryName = directory.get('name')
        for child in directory.getchildren():
            if everything:
                updated.append(child.get('name'))
            else:
                childName = child.get('name')
                size = 0
                hash = ''
                for _directory in root.findall('directory'):
                    for _child in _directory.getchildren():
                        if _child.get('name') == childName:
                            size = int(child.find('size').text)
                            hash = child.find('hash').text
                filepath = os.path.join(directoryName, childName)
                if os.path.getsize(os.path.join('build', filepath)) != size:
                    updated.append(filepath)
                elif getFileMD5Hash(os.path.join('build', filepath)) != hash:
                    updated.append(filepath)

# Compress the updated files:
for update in updated:
    print 'Compressing {0}...'.format(update)
    if update.startswith('phase_'):
        filepath = os.path.join('build/resources', update)
    else:
        filepath = os.path.join('build', update)
    compressFile(filepath)

print 'Uploading files to cdn.toontowninfinite.com...'
connection = boto.connect_s3(awsAccessKeyId, awsSecretAccessKey)
bucket = connection.get_bucket(bucketName)

invalidations = []

print 'Uploading... patcher.xml'
key = Key(bucket)
key.key = '{0}/{1}/patcher.xml'.format(distribution, platform)
invalidations.append(key.key)
key.set_contents_from_filename('dist/patcher.xml')
key.make_public()

for update in updated:
    update = os.path.splitext(update)[0] + '.bz2'
    print 'Uploading... ' + update
    if update.startswith('phase_'):
        update = 'resources/' + update
    key = Key(bucket)
    key.key = '{0}/{1}/'.format(distribution, platform) + update
    invalidations.append(key.key)
    key.set_contents_from_filename('dist/' + update)
    key.make_public()

connection = CloudFrontConnection(awsAccessKeyId, awsSecretAccessKey)
connection.create_invalidation_request(awsCfDistributionId, invalidations)

print 'Done uploading files.'

print 'Successfully finished the deployment process!'
