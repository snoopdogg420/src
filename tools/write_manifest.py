#!/usr/bin/env python2
import argparse
import collections
import hashlib
import json
import os
from xml.etree import ElementTree


parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', default='patcher.xml',
                    help='The name of the generated manifest file.')
parser.add_argument('--ancestor',
                    help='The generated manifest file will be based off of '
                         'this one.')
parser.add_argument('--launcher-version', default='1.0.0',
                    help='The Toontown Infinite game launcher version.')
parser.add_argument('--account-server', default='toontowninfinite.com',
                    help='The address of the Toontown Infinite account server.')
parser.add_argument('--client-agent', default='gameserver.toontowninfinite.com',
                    help='The address of the Client Agent in which the game '
                         'will connect to.')
parser.add_argument('--server-version', default='infinite-dev',
                    help='The server version corresponding to this patch.')
parser.add_argument('--resources-revision',
                    help='A 7-character commit hash from the '
                         'ToontownInfinite/resources repository corresponding '
                         'to this patch.')
parser.add_argument('files', nargs='*',
                    help='The file to include in the generated manifest file.')
args = parser.parse_args()


def getFileHash(filepath):
    hash = hashlib.md5()
    with open(filepath, 'rb') as f:
        readChunk = lambda: f.read(128 * hash.block_size)
        for chunk in iter(readChunk, ''):
            hash.update(chunk)
    return hash.hexdigest()


def getFileInfo(filepath):
    return (os.path.basename(filepath), os.path.getsize(filepath),
            getFileHash(filepath))


class ManifestDirectory:
    def __init__(self, name):
        self.name = name

        self.directories = []
        self.files = []

    def getName(self):
        return self.name

    def addDirectory(self, directory):
        self.directories.append(directory)

    def getDirectories(self):
        return self.directories

    def getDirectory(self, name):
        for directory in self.directories:
            if directory.getName() == name:
                return directory

    def hasDirectory(self, name):
        for directory in self.directories:
            if directory.getName() == name:
                return True
        return False

    def addFile(self, file):
        self.files.append(file)

    def getFiles(self):
        return self.files


class ManifestFile:
    def __init__(self, name, size, hash):
        self.name = name
        self.size = size
        self.hash = hash

    def getName(self):
        return self.name

    def getSize(self):
        return self.size

    def getHash(self):
        return self.hash


# First, construct the tree:
root = ManifestDirectory('.')
for filepath in args.files:
    # We don't want Windows-style paths:
    filepath = filepath.replace('\\', '/')

    # Find our parent directory:
    parent = root
    dirname = os.path.dirname(filepath)
    if dirname:
        for _dirname in dirname.split('/'):
            if not parent.hasDirectory(_dirname):
                parent.addDirectory(ManifestDirectory(_dirname))
            parent = parent.getDirectory(_dirname)

    # Add the file to the parent:
    parent.addFile(
        ManifestFile(os.path.basename(filepath), os.path.getsize(filepath),
                     getFileHash(filepath)))

# Next, begin writing the manifest:


class ManifestXMLGenerator:
    def __init__(self, output):
        self.output = output

        self.root = ElementTree.Element('patcher')

    def addSubElement(self, name, text):
        element = ElementTree.SubElement(self.root, name)
        element.text = text

    def addDirectory(self, directory, parent=None):
        if parent is None:
            parent = self.root
        element = ElementTree.SubElement(parent, 'directory')
        element.set('name', directory.getName())
        for _directory in directory.getDirectories():
            self.addDirectory(_directory, parent=element)
        for file in directory.getFiles():
            self.addFile(file, parent=element)

    def addFile(self, file, parent):
        element = ElementTree.SubElement(parent, 'file')
        element.set('name', file.getName())
        size = ElementTree.SubElement(element, 'size')
        size.text = str(file.getSize())
        hash = ElementTree.SubElement(element, 'hash')
        hash.text = file.getHash()

    def write(self):
        ElementTree.ElementTree(self.root).write(self.output)


class ManifestJSONGenerator:
    def __init__(self, output):
        self.output = output

        self.root = collections.OrderedDict()

    def addSubElement(self, name, text):
        self.root[name] = text

    def addDirectory(self, directory, parent=None):
        if parent is None:
            parent = self.root
        element = collections.OrderedDict()
        element['directories'] = collections.OrderedDict()
        element['files'] = []
        parent[directory.getName()] = element
        for _directory in directory.getDirectories():
            self.addDirectory(_directory, parent=element['directories'])
        for file in directory.getFiles():
            self.addFile(file, parent=element['files'])

    def addFile(self, file, parent):
        element = collections.OrderedDict()
        element['name'] = file.getName()
        element['size'] = file.getSize()
        element['hash'] = file.getHash()
        parent.append(element)

    def write(self):
        with open(self.output, 'w') as f:
            json.dump(self.root, f)


print 'Writing %s...' % args.output

format = os.path.splitext(args.output)[1]
if format == '.xml':
    generator = ManifestXMLGenerator(args.output)
elif format == '.json':
    generator = ManifestJSONGenerator(args.output)
else:
    raise NotImplementedError('Format not supported: ' + format)

generator.addSubElement('launcher-version', args.launcher_version)
generator.addSubElement('account-server', args.account_server)
generator.addSubElement('client-agent', args.client_agent)
generator.addSubElement('server-version', args.server_version)
generator.addSubElement('resources-revision', args.resources_revision)
generator.addDirectory(root)
generator.write()

print 'Done writing %s.' % args.output
