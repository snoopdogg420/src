#!/usr/bin/env python2
# This is the "main" module that will start a distribution copy of
# Toontown Infinite.

import hashlib
import sys

def __eval_hook__(*args):
    try:
        base.cr.csm.banPlayer()
    finally:
        sys.exit(28)

__builtins__.__ceval__ = __eval_hook__
__builtins__.__eeval__ = __eval_hook__

# Before we do anything we need to confirm the authenticity of python27.dll
md5 = hashlib.md5()
with open('python27.dll', 'rb') as f:
    readChunk = lambda: f.read(128 * md5.block_size)
    for chunk in iter(readChunk, ''):
        md5.update(chunk)
    hash = md5.hexdigest()

if hash != 'a332b72d3b6a4ab8ccc47b2a60df8766':
    sys.exit(27)

# This is a temp patch.
# It should be edited in the interpreter (infinite.exe).
sys.path = ['.']

# Replace some modules that do exec:
import collections
collections.namedtuple = lambda *x: tuple

# This is included in the package by the prepare_client script. It contains the
# PRC file data, (stripped) DC file, and time zone info:
import game_data
import __builtin__

# Load all of the packaged PRC config page(s):
from pandac.PandaModules import *
for i, config in enumerate(game_data.CONFIG):
    name = 'GameData config page #{0}'.format(i)
    loadPrcFileData(name, config)

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load them manually:
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountFile, mountPoint = (mount.split(' ', 2) + [None, None, None])[:2]
    mountFile = Filename(mountFile)
    mountFile.makeAbsolute()
    mountPoint = Filename(mountPoint)
    vfs.mount(mountFile, mountPoint, 0)

# Next, let's get the DC stream:
__builtin__.dcStream = StringStream(game_data.DC)

# We also need timezone stuff:
import sys, new, marshal, zlib, os

# mount the timezone info as modules
# so pytz can import them (pytz/__init__.py)

mod = sys.modules.setdefault('zoneinfo', new.module('zoneinfo'))
mod.__file__ = "zoneinfo\\__init__.pyc"

def registerTopAttr(modname, mod):
    base = modname.rsplit('.', 1)[0]
    top = modname.split('.')[-1]

    setattr(sys.modules[base], top, mod)

# mount top locations (zoneinfo/XXXXX)
locations = set(x.split('/')[1] for x in game_data.ZONEINFO.keys())
for x in locations:
    path = 'zoneinfo/' + x
    fullname = path.replace('/', '.')
    data = game_data.ZONEINFO.get(path)

    mod = sys.modules.setdefault(fullname, new.module(fullname))

    if data:
        mod.__file__ = os.path.join(path, '__init__.pyc')
        exec marshal.loads(zlib.decompress(data)) in mod.__dict__

    else:
        mod.__file__ = path + '.pyc'

    registerTopAttr(fullname, mod)

# some modules have 3 levels of depth
def handleAmerica3Levels(name):
    modname = "zoneinfo.America." + name
    mod = sys.modules.setdefault(modname, new.module(modname))
    mod.__file__ = "zoneinfo\\America\\%s\\__init__.pyc" % name

    registerTopAttr(modname, mod)

handleAmerica3Levels("Argentina")
handleAmerica3Levels("Indiana")
handleAmerica3Levels("Kentucky")
handleAmerica3Levels("North_Dakota")

# mount sub locations (zoneinfo/XXXXX/XXXXX)
for x in game_data.ZONEINFO.keys():
    if len(x.split('/')) == 2:
        continue

    path = x
    fullname = path.replace('/', '.')
    data = game_data.ZONEINFO.get(path)

    #print 'mount', path

    mod = sys.modules.setdefault(fullname, new.module(fullname))
    mod.__file__ = path + '.pyc'

    if data:
        exec marshal.loads(zlib.decompress(data)) in mod.__dict__

    registerTopAttr(fullname, mod)

# Finally, start the game:
import toontown.toonbase.ClientStart
