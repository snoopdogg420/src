from pandac.PandaModules import NodePath

from toontown.dna.DNALoader import DNALoader


def loadDNAFile(storage, filepath):
    print 'Reading DNA file...', filepath
    dnaLoader = DNALoader()
    if __debug__:
        filepath = '../resources/' + filepath
    else:
        filepath = '/' + filepath
    dnaLoader.load(storage, filepath)
    root = NodePath('root')
    dnaLoader.getTopGroup().traverse(storage, root)
    dnaLoader.destroy()
    return root


def loadDNAFileAI(storage, filepath):
    dnaLoader = DNALoader()
    if __debug__:
        filepath = '../resources/' + filepath
    else:
        filepath = '/' + filepath
    dnaLoader.load(storage, filepath)
    dnaLoader.destroy()


def loadDNABulk(storage, filepath):
    print 'Reading DNA file...', filepath
    loadDNAFileAI(storage, filepath)


class DNABulkLoader:
    def __init__(self, storage, filepaths):
        self.storage = storage
        self.filepaths = filepaths

    def destroy(self):
        self.storage = None
        self.filepaths = ()

    def load(self):
        for filepath in self.filepaths:
            print 'Reading DNA file...', filepath
            loadDNABulk(self.storage, filepath)
