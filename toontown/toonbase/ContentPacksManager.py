from direct.directnotify.DirectNotifyGlobal import directNotify
import os
from panda3d.core import Multifile, Filename, VirtualFileSystem


CONTENT_EXT_WHITELIST = ('.jpg', '.jpeg', '.rgb', '.png', '.ogg', '.ttf')


class ContentPacksManager:
    notify = directNotify.newCategory('ContentPacksManager')
    notify.setInfo(True)

    def __init__(self, filepath):
        self.filepath = filepath

        self.vfs = VirtualFileSystem.getGlobalPtr()

        if __debug__:
            self.mountPoint = '../resources'
        else:
            self.mountPoint = '/'

        self.sortOrder = []

    def readSortData(self, filename):
        """
        Read the sort order for the specified file.
        """
        filename = os.path.join(self.filepath, filename)
        if not os.path.exists(filename):
            return
        self.sortOrder = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                if not line.startswith('- '):
                    continue
                self.sortOrder.append(line[:line.find('#')][2:])

    def writeSortData(self, filename):
        """
        Write the sort order to the specified file.
        """
        with open(os.path.join(self.filepath, filename), 'w') as f:
            for filename in self.sortOrder:
                f.write('- %s\n' % filename)

    def apply(self, filename):
        """
        Apply the specified content pack on top of the existing content.
        """
        self.notify.info('Applying %s...' % filename[len(self.filepath):])

        mf = Multifile()
        mf.openReadWrite(Filename(filename))

        # Discard content with non-whitelisted extensions:
        for subfileName in mf.getSubfileNames():
            ext = os.path.splitext(subfileName)[1]
            if ext not in CONTENT_EXT_WHITELIST:
                mf.removeSubfile(subfileName)

        self.vfs.mount(mf, self.mountPoint, 0)

    def applyAll(self):
        """
        Using a sort order if one exists, recursively apply all content packs
        in the configured content packs directory.
        """
        # First, apply the content packs in our sort order:
        for sortFilename in self.sortOrder[:]:
            filename = os.path.join(self.filepath, sortFilename).replace('\\', '/')
            if (not filename.endswith('.mf')) or (not os.path.exists(filename)):
                self.notify.warning('Invalidating %s...' % sortFilename)
                self.sortOrder.remove(sortFilename)
            else:
                self.apply(filename)

        # Next, apply the remaining content packs in the directory:
        for root, _, filenames in os.walk(self.filepath):
            for filename in filenames:
                if not filename.endswith('.mf'):
                    continue
                filename = os.path.join(root, filename).replace('\\', '/')

                # Ensure that this file isn't in our sort order (and thus not applied):
                sortFilename = filename[len(self.filepath):]
                if sortFilename in self.sortOrder:
                    continue

                self.apply(filename)

                # Add this file to our sort order:
                self.sortOrder.append(sortFilename)
