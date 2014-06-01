import xml.etree.ElementTree as ET
import argparse
import hashlib
import os
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('--src-dir', default='build',
                    help='The directory of the Toontown Infinite build.')
parser.add_argument('--dest-dir', default='C:/xampp/htdocs/download',
                    help='The directory in which to store the patcher.')
parser.add_argument('--client-agent', default='108.170.49.170',
                    help='The IP address of the Client Agent to connect to.')
parser.add_argument('--account-server', default='toontowninfinite.com',
                    help='The address of the Toontown Infinite account server.')
parser.add_argument('--launcher-version', default='1.0.0.0',
                    help='The current version of the Toontown Infinite launcher.')
parser.add_argument('includes', nargs='*', default=['GameData.bin'],
                    help='The files to include in the main directory.')
args = parser.parse_args()


def getFileMD5Hash(filepath):
    md5 = hashlib.md5()
    readBlock = lambda: f.read(128 * md5.block_size)
    with open(filepath, 'rb') as f:
        for chunk in iter(readBlock, b''):
            md5.update(chunk)
    return md5.hexdigest()


def getFileInfo(filepath):
    return (
        os.path.basename(filepath),
        os.path.getsize(filepath),
        getFileMD5Hash(filepath)
    )


rootFiles = []
for include in args.includes:
    filepath = os.path.join(args.src_dir, include)
    rootFiles.append(getFileInfo(filepath))
    print 'Including...', include

resourcesFiles = []
resourcesDir = os.path.join(args.src_dir, 'resources')
for filename in os.listdir(resourcesDir):
    if not filename.startswith('phase_'):
        continue
    if not filename.endswith('.mf'):
        continue
    filepath = os.path.join(resourcesDir, filename)
    resourcesFiles.append(getFileInfo(filepath))
    print 'Including...', filename

print 'Writing patcher.xml...'

# First, add the root:
patcherRoot = ET.Element('patcher')

# Next, add the Toontown Infinite launcher version:
launcherversion = ET.SubElement(patcherRoot, 'launcherversion')
launcherversion.text = args.launcher_version

# Then add the account server address:
accountserver = ET.SubElement(patcherRoot, 'accountserver')
accountserver.text = args.account_server

# Then add the Client Agent IP:
clientagent = ET.SubElement(patcherRoot, 'clientagent')
clientagent.text = args.client_agent

# If we don't have Git on our path, let's attempt to add it:
paths = (
    '{0}\\Git\\bin'.format(os.environ['ProgramFiles']),
    '{0}\\Git\\cmd'.format(os.environ['ProgramFiles'])
)
for path in paths:
    if path not in os.environ['PATH']:
        os.environ['PATH'] += ';' + path

# Add the git revision:
revision = ET.SubElement(patcherRoot, 'revision')
revision.text = subprocess.Popen(
    ['git', 'rev-parse', 'HEAD'],
    stdout=subprocess.PIPE,
    cwd=args.src_dir).stdout.read().strip()[:7]

# Add the most recent commit message:
revision = ET.SubElement(patcherRoot, 'message')
revision.text = subprocess.Popen(
    ['git', 'log', '-1', '--pretty=%B'],
    stdout=subprocess.PIPE,
    cwd=args.src_dir).stdout.read().strip()

# Next, add the root directory:
root = ET.SubElement(patcherRoot, 'directory')
root.set('name', '')

# Add all of the root files:
for filename, size, hash in rootFiles:
    _filename = ET.SubElement(root, 'file')
    _filename.set('name', filename)
    _size = ET.SubElement(_filename, 'size')
    _size.text = str(size)
    _hash = ET.SubElement(_filename, 'hash')
    _hash.text = str(hash)

# Next, add the resources directory:
resourcesRoot = ET.SubElement(patcherRoot, 'directory')
resourcesRoot.set('name', 'resources')

# Add all of the resources files:
for filename, size, hash in resourcesFiles:
    _filename = ET.SubElement(resourcesRoot, 'file')
    _filename.set('name', filename)
    _size = ET.SubElement(_filename, 'size')
    _size.text = str(size)
    _hash = ET.SubElement(_filename, 'hash')
    _hash.text = str(hash)
	
# Finally, write the product:
filepath = os.path.join(args.dest_dir, 'patcher.xml')
ET.ElementTree(patcherRoot).write(filepath)

print 'Done writing patcher.xml'
