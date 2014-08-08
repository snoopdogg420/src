import DNALoader
from DNAStorage import DNAStorage

def loadDNAFile(storage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader.DNALoader()
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    return dnaLoader.loadDNAFile(storage, file)

def loadDNAFileAI(storage, file):
    dnaLoader = DNALoader.DNALoader()
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    return dnaLoader.loadDNAFileAI(storage, file)

def loadDNABulk(storage, files):
    pass # TODO