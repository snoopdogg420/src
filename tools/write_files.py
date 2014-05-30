import argparse
import bz2
import os
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument('--src-dir', default='tools/build',
                    help='The directory of the Toontown Infinite build.')
parser.add_argument('--dest-dir', default='C:/xampp/htdocs/download',
                    help='The directory in which to store the compressed files.')
parser.add_argument('includes', nargs='*', default=['GameData.bin'],
                    help='The files to include in the main directory.')
args = parser.parse_args()


def compressFile(filepath, subdir=''):
    with open(filepath, 'rb') as f:
        data = f.read()
    filename = os.path.basename(filepath)
    bz2Filename = os.path.splitext(filename)[0] + '.bz2'
    bz2Filepath = os.path.join(args.dest_dir, subdir, bz2Filename)
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


print 'Writing files...'

for include in args.includes:
    filepath = os.path.join(args.src_dir, include)
    bz2Filename = os.path.splitext(include)[0] + '.bz2'
    bz2Filepath = os.path.join(args.dest_dir, bz2Filename)
    bz2Hash = hashlib.md5()
    if os.path.exists(bz2Filepath):
        try:
            bufferSize = 128 * bz2Hash.block_size
            with bz2.BZ2File(bz2Filepath, 'r') as f:
                block = f.read(bufferSize)
                while block:
                    bz2Hash.update(block)
                    block = f.read(bufferSize)
        except:
            pass
    bz2Hash = bz2Hash.hexdigest()
    if getFileMD5Hash(filepath) != bz2Hash:
        compressFile(filepath)
        print 'Compressing...', include
    else:
        print 'Skipping compression...', include


resourcesDir = os.path.join(args.src_dir, 'resources')
for filename in os.listdir(resourcesDir):
    if not filename.startswith('phase_'):
        continue
    if not filename.endswith('.mf'):
        continue
    filepath = os.path.join(resourcesDir, filename)
    bz2Filename = os.path.splitext(filename)[0] + '.bz2'
    bz2Filepath = os.path.join(args.dest_dir, 'resources', bz2Filename)
    bz2Hash = hashlib.md5()
    if os.path.exists(bz2Filepath):
        try:
            bufferSize = 128 * bz2Hash.block_size
            with bz2.BZ2File(bz2Filepath, 'r') as f:
                block = f.read(bufferSize)
                while block:
                    bz2Hash.update(block)
                    block = f.read(bufferSize)
        except:
            pass
        bz2Hash = bz2Hash.hexdigest()
    if getFileMD5Hash(filepath) != bz2Hash:
        compressFile(filepath, subdir='resources')
        print 'Compressing...', filename
    else:
        print 'Skipping compression...', filename

print 'Done writing files.'
