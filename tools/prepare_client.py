import argparse
import os
import subprocess
import shutil
import pytz


parser = argparse.ArgumentParser()
parser.add_argument('--distribution', default='en', help='The distribution token.')
parser.add_argument('--build-dir', default='build', help='The directory to store the build files in.')
parser.add_argument('--src-dir', default='..', help='The directory of the Toontown Infinite source code.')
parser.add_argument('--server-ver', default='tti-REVISION',
                    help='An override for the server version of this build.\n'
                         'Any REVISION tokens will be replaced with the current git revision.')
parser.add_argument('--build-mfs', action='store_true', help='When present, multifiles will be built.')
parser.add_argument('--resources-dir', default='../resources', help='The directory to the Toontown Infinite resources.')
parser.add_argument('--main-module', default='infinite.base.ClientStartDist',
                    help='The module that will be used to start the game.')
parser.add_argument('modules', nargs='*', default=['shared', 'infinite'],
                    help='The Toontown Infinite modules to be included in the build.')
args = parser.parse_args()

print 'Preparing the client...'

# Create a clean build directory for us to store our build material:
if os.path.exists(args.build_dir):
    shutil.rmtree(args.build_dir)
os.mkdir(args.build_dir)
print 'Build directory = {0}'.format(args.build_dir)

# This next part is only required if the user wants the Git revision in
# their server version:
revision = ''
if 'REVISION' in args.server_ver:
    # If we don't have Git on our path, let's attempt to add it:
    paths = (
        '{0}\\Git\\bin'.format(os.environ['ProgramFiles']),
        '{0}\\Git\\cmd'.format(os.environ['ProgramFiles'])
    )
    for path in paths:
        if path not in os.environ['PATH']:
            os.environ['PATH'] += ';' + path

    # Now, let's get that revision string:
    revision = subprocess.Popen(
        ['git', 'rev-parse', 'HEAD'],
        stdout=subprocess.PIPE,
        cwd=args.src_dir).stdout.read().strip()[:7]

# Parse the server version:
serverVersion = args.server_ver.replace('REVISION', revision)
print 'serverVersion = {0}'.format(serverVersion)

# Collect the DC filepaths:
dcFiles = []
dcFilePath = args.src_dir + '\\astron'
for filename in os.listdir(dcFilePath):
    if filename.endswith('.dc'):
        dcFiles.append(os.path.join(dcFilePath, filename))
print 'dcFiles = {0}'.format(dcFiles)

# Copy the required module files:
excludes = ('NonRepeatableRandomSourceUD.py', 'NonRepeatableRandomSourceAI.py')
for module in args.modules:
    print 'Writing module...', module
    for root, folders, files in os.walk(os.path.join(args.src_dir, module)):
        outputDir = root.replace(args.src_dir, args.build_dir)
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        for filename in files:
            if not filename.endswith('.py'):
                continue
            if filename.endswith('UD.py') and (filename not in excludes):
                continue
            if filename.endswith('AI.py') and (filename not in excludes):
                continue
            if filename == 'ServiceStart.py':
                continue
            shutil.copyfile(os.path.join(root, filename), os.path.join(outputDir, filename))

# Start writing game_data:
print 'Writing game_data.py...'

configFileName = 'config_{0}.prc'.format(args.distribution)
print 'Using config file: {0}'.format(configFileName)
configData = []
with open(os.path.join(args.src_dir, 'config', configFileName)) as f:
    data = f.read()
    data = data.replace('SERVER_VERSION', serverVersion)
    configData.append(data)

from pandac.PandaModules import *
dcf = DCFile()
for dcFile in dcFiles:
    dcf.read(Filename.fromOsSpecific(dcFile))
dcStream = StringStream()
dcf.write(dcStream, True)
dcData = dcStream.getData()

zoneInfo = {}
for timezone in pytz.all_timezones:
    zoneInfo['zoneinfo/' + timezone] = pytz.open_resource(timezone).read()

gameData = 'CONFIG = %r\nDC = %r\nZONEINFO = %r\n' % (configData, dcData, zoneInfo)
with open(os.path.join(args.build_dir, 'game_data.py'), 'w') as f:
    f.write(gameData)

# Build the multifiles if wanted:
if args.build_mfs:
    print 'Building multifiles...'
    dest = os.path.join(args.build_dir, 'resources')
    os.mkdir(dest)
    dest = os.path.realpath(dest)
    os.chdir(args.resources_dir)
    for phase in os.listdir('.'):
        if not phase.startswith('phase_'):
            continue
        if not os.path.isdir(phase):
            continue
        out = os.path.join(dest, phase + '.mf')
        print 'Writing...', out
        os.system('multify -c -f {0} {1}'.format(out, phase))
else:
    print 'Skipping multifiles...'
