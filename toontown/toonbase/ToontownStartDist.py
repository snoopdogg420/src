# This is the "main" module that will start a distribution copy of
# Toontown Infinite.

# Replace some modules that do exec:
import collections
collections.namedtuple = lambda *x: tuple

# This is included in the package by the prepare_client script. It contains the
# PRC file data, (stripped) DC file, and time zone info:
import game_data

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
dcStream = StringStream(game_data.DC)

# We also need timezone stuff:
class dictloader(object):
    def __init__(self, dict):
        self.dict = dict

    def get_data(self, key):
        return self.dict.get(key.replace('\\','/'))

import pytz
pytz.__loader__ = dictloader(game_data.ZONEINFO)

# Finally, start the game:
import toontown.toonbase.ToontownStart
