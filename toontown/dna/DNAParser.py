import DNALoader
from DNAStorage import DNAStorage

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader.DNALoader(dnaStorage)
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    return dnaLoader.loadDNAFile(file)

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader.DNALoader(dnaStorage)
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    return dnaLoader.loadDNAFileAI(file)

def loadDNABulk(dnaStorage, files):
    pass # TODO