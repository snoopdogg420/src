#!/usr/bin/env python2
import StringIO
import __builtin__
import json
import os
import shutil
import subprocess
import sys
import tarfile


# Notify the user if they are missing any Python module dependencies:
try:
    import requests
except ImportError, e:
    print 'Missing Python module dependency:', e.message[16:]
    sys.exit(1)

# Notify the user if they are missing any file dependencies:
missingFiles = []
for filename in ('deploy.json',):
    if filename.endswith('.exe') and (sys.platform != 'win32'):
        # We aren't on Windows, so remove the .exe file extension:
        filename = os.path.splitext(filename)[0]
    if not os.path.exists(filename):
        missingFiles.append(filename)
if missingFiles:
    print 'Missing file dependencies:', ', '.join(missingFiles)
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
for name in ('release', 'config-files', 'vfs-mounts', 'modules', 'main-module',
             'package-files', 'ftp-address', 'ftp-username', 'ftp-password'):
    if name not in config:
        missingVars.append(name)
if missingVars:
    print 'Missing configuration variables:', ', '.join(missingVars)
    sys.exit(4)

deploymentDir = os.path.realpath('.')
srcDir = os.path.realpath('..')
resourcesDir = os.path.realpath('../../resources')

# Ensure the specified release exists on all repositories:
release = config['release']
for repositoryDir in (srcDir, resourcesDir):
    process = subprocess.Popen(('git', 'tag'), stdout=subprocess.PIPE, cwd=repositoryDir)
    if release not in process.stdout.read().strip().split('\n'):
        print 'Invalid release:', release
        sys.exit(5)

# Ensure we can identify a valid distribution:
distribution = release[:release.find('-v')]
if distribution not in ('dev', 'test', 'en'):
    print 'Unsupported distribution:', distribution
    sys.exit(6)

# Checkout the specified Git tag on all of the repositories:


def checkout(repositoryDir, tag):
    # First, get the name of the remote:
    process = subprocess.Popen(('git', 'remote', '-v'), stdout=subprocess.PIPE, cwd=repositoryDir)
    remoteName = os.path.basename(process.stdout.read().strip().split('\n')[0].split()[1])
    if remoteName.endswith('.git'):
        remoteName = remoteName[:-4]

    # Next, create a directory for it, replacing the contents of the old one if
    # it already exists:
    if os.path.exists(remoteName):
        shutil.rmtree(remoteName)
    os.mkdir(remoteName)

    # Read the Git tag's content into an archive format:
    print "Archiving the contents of '%s' from repository '%s'..." % (tag, remoteName)
    process = subprocess.Popen(('git', 'archive', tag), stdout=subprocess.PIPE, cwd=repositoryDir)

    # Finally, extract the archive, saving the contents to disk:


    def members(members):
        for i, member in enumerate(members):
            percentage = int((float(i+1)/len(members)) * 100)
            sys.stdout.write("\rExtracting the contents of '%s' from repository '%s'..." % (tag, remoteName))
            sys.stdout.write(' ' + str(percentage) + '%')
            sys.stdout.flush()
            yield member


    with tarfile.TarFile(fileobj=StringIO.StringIO(process.stdout.read())) as f:
        f.extractall(path=remoteName, members=members(f.getmembers()))

    sys.stdout.write('\n')
    sys.stdout.flush()


checkout(srcDir, release)
checkout(resourcesDir, release)

# Prepare the client for building:
cmd = (sys.executable + ' ../tools/prepare_client.py' +
       ' --build-dir build' +
       ' --src-dir src' +
       ' --server-ver ' + release +
       ' --include NonRepeatableRandomSource*.py' +
       ' --exclude *AI.py' +
       ' --exclude *UD.py' +
       ' --exclude ServiceStart.py')
for configFile in config['config-files']:
    cmd += ' --config-file ' + configFile
for vfsMount in config['vfs-mounts']:
    cmd += ' --vfs-mount ' + vfsMount
for module in config['modules']:
    cmd += ' ' + module
os.system(cmd)

# Build the client:
cmd = (sys.executable + ' ../tools/build_client.py' +
       ' --build-dir build' +
       ' --main-module ' + config['main-module'] +
       ' GameData.zip')
os.system(cmd)

# TODO: Encrypt the client.

# Create a 'dist' directory to store the files that should be uploaded to the
# content server:
distDir = os.path.realpath('dist')
if os.path.exists(distDir):
    shutil.rmtree(distDir)
os.mkdir(distDir)

# Compile the resources into multifile archives:
print 'Compiling resources into multifile archives...'
for filename in os.listdir('resources'):
    if not filename.startswith('phase_'):
        continue
    filepath = os.path.realpath(os.path.join('resources', filename))
    if not os.path.isdir(filepath):
        continue
    filename += '.mf'
    print 'Compiling...', filename
    os.system('multify -c -f "%s" "%s"' % (os.path.join(distDir, filename), filepath))

# Download the old manifest so that we can build off of it:
ftpAddress = config['ftp-address']
with open(os.path.join(distDir, 'manifest.xml'), 'w') as f:
    response = requests.get('%s/%s/win32/patcher.xml' % (ftpAddress, distribution), stream=True)
    if response.ok:
        for chunk in response.iter_content(1024):
            if not chunk:
                break
            f.write(chunk)

# TODO: Write a manifest with the old one as its ancestor.
# TODO: Package all of the files for distribution.
# TODO: Upload.
