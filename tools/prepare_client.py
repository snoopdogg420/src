#!/usr/bin/env python2
import argparse
import fnmatch
import os
import re
import shutil


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory to store the files to be built in.')
parser.add_argument('--src-dir', default='..',
                    help="The path to the game's source code.")
parser.add_argument('--server-ver', default='infinite-dev',
                    help='The server version associated with this build.')
parser.add_argument('--include', '-i', action='append',
                    help='Explicitly include this file in the build.')
parser.add_argument('--exclude', '-x', action='append',
                    help='Explicitly exclude this file from the build.')
parser.add_argument('--config-file', action='append',
                    help='Include this file as a config page in game_data.py.')
parser.add_argument('--vfs-mount', action='append',
                    help='Add this file to the list of files to be mounted in '
                         'the virtual file system when the client is started.')
parser.add_argument('modules', nargs='*', default=['otp', 'toontown'],
                    help='The internal modules to be included in the build.')
args = parser.parse_args()

print 'Preparing the client...'

# We'll need an empty directory to store the files to be built in:
if os.path.exists(args.build_dir):
    shutil.rmtree(args.build_dir)
os.makedirs(args.build_dir)

# Copy the desired internal modules into the build directory in their
# "minified" form:

# Copy the desired internal modules into the build directory, and respect the
# included files, and the excluded files:
include_exp = re.compile('a^')
if args.include is not None:
    include_exp = re.compile('|'.join(fnmatch.translate(pat) for pat in args.include))
exclude_exp = re.compile('a^')
if args.exclude is not None:
    exclude_exp = re.compile('|'.join(fnmatch.translate(pat) for pat in args.exclude))

for module in args.modules:
    print 'Copying module...', module

    for root, _, filenames in os.walk(os.path.join(args.src_dir, module)):
        output_dir = root.replace(args.src_dir, args.build_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for filename in filenames:
            if include_exp.match(filename) is None:
                if not filename.endswith('.py'):
                    continue
                if exclude_exp.match(filename) is not None:
                    continue
            src_filepath = os.path.join(root, filename)
            dest_filepath = os.path.join(output_dir, filename)
            shutil.copy(src_filepath, dest_filepath)

# Write game_data.py -- a compile-time generated module storing data used by
# the game when it is launched:
print 'Generating game_data.py...'

# Collect the config pages:
config_pages = []

for filepath in (args.config_file or ()):
    with open(os.path.join(args.src_dir, filepath)) as f:
        lines = f.readlines()

        # Replace definitions of server-version with our own:
        for i, line in enumerate(lines):
            lines[i] = line.rstrip()
            if line.startswith('server-version '):
                lines[i] = 'server-version ' + args.server_ver

        config_pages.append('\n'.join(lines))

# We need to create a config page containing our virtual file system mounts:
data = '# Virtual file system:\n'
data += 'model-path /\n'
for vfs_mount in (args.vfs_mount or ()):
    data += 'vfs-mount %s /\n' % vfs_mount
config_pages.append(data)

# Next, collect the DC file data with imports omitted for security purposes:
dc_data = ''
dclass_dir = os.path.join(args.src_dir, 'astron/dclass')
for filename in sorted(os.listdir(dclass_dir)):
    if not filename.endswith('.dc'):
        continue
    with open(os.path.join(dclass_dir, filename), 'r') as f:
        for line in f.readlines():
            if 'import ' not in line:
                dc_data += line

# Finally, write game_data.py:
game_data = 'CONFIG = %r\nDC = %r\n'
with open(os.path.join(args.build_dir, 'game_data.py'), 'w') as f:
    f.write('CONFIG = %r\nDC = %r\n' % (config_pages, dc_data.strip()))

print 'Done preparing the client.'
