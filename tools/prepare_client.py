#!/usr/bin/env python2
import argparse
import os
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('--server-ver', default='infinite-dev',
                    help='The server version corresponding to this build.')
parser.add_argument('--build-dir', default='build',
                    help='The directory to store the build files in.')
parser.add_argument('--src-dir', default='..',
                    help='The path to the Toontown Infinite source code.')
parser.add_argument('--include', '-i', action='append',
                    help='Explicitly include this file in the build.')
parser.add_argument('--exclude', '-x', action='append',
                    help='Explicitly exclude this file from the build.')
parser.add_argument('--config-file', action='append',
                    help='Include this config file in game_data.py.')
parser.add_argument('--vfs-mount', action='append',
                    help='Add this file to the list of files to be mounted in '
                         'the virtual file system when the game is launched.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown'],
                    help='The internal modules to be included in the build.')
args = parser.parse_args()

print 'Preparing the client...'

# We'll need a clean directory to store our build files in:
if os.path.exists(args.build_dir):
    shutil.rmtree(args.build_dir)
os.mkdir(args.build_dir)

# Copy the desired internal modules into the build directory in their
# "minified" form:
for module in args.modules:
    print 'Copying module...', module

    for root, folders, files in os.walk(os.path.join(args.src_dir, module)):
        outputDir = root.replace(args.src_dir, args.build_dir)
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        for filename in files:
            if filename not in args.include:
                if not filename.endswith('.py'):
                    continue
                if filename.endswith('UD.py'):
                    continue
                if filename.endswith('AI.py'):
                    continue
                if filename in args.exclude:
                    continue
            shutil.copy(os.path.join(root, filename), os.path.join(outputDir, filename))

# Write game_data.py -- a compile-time generated collection of data to be used
# when the game is launched:
print 'Generating game_data.py...'

# Collect the config pages:
configPages = []

for filepath in args.config_file:
    with open(os.path.join(args.src_dir, filepath)) as f:
        lines = f.readlines()

        # Strip each line, and replace definitions of server-version with our
        # own:
        for i, line in enumerate(lines):
            lines[i] = line.strip()
            if line.startswith('server-version '):
                lines[i] = 'server-version ' + args.server_ver

        configPages.append('\n'.join(lines))

if args.vfs_mount is not None:
    # We need to add a config page containing our virtual file system mounts:
    data = '# Virtual file system:\n'
    data += 'model-path /\n'
    for vfsMount in args.vfs_mount:
        data += 'vfs-mount %s /\n' % vfsMount
    configPages.append(data)

# Next, collect the DC file data:
dcData = ''
dclassDir = os.path.join(args.src_dir, 'astron/dclass')
for filename in sorted(os.listdir(dclassDir)):
    if not filename.endswith('.dc'):
        continue
    with open(os.path.join(dclassDir, filename), 'r') as f:
        for line in f.readlines():
            if 'import ' not in line:
                dcData += line

# Finally, write game_data.py:
gameData = 'CONFIG = %r\nDC = %r\n'
with open(os.path.join(args.build_dir, 'game_data.py'), 'w') as f:
    f.write(gameData % (configPages, dcData.strip()))

print 'Done preparing the client.'
