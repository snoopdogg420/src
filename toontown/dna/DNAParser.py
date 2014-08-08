import DNALoader
from DNAStorage import DNAStorage

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader.DNALoader()
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    return dnaLoader.loadDNAFile(dnaStorage, file)

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader.DNALoader()
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    return dnaLoader.loadDNAFileAI(dnaStorage, file)

def loadDNABulk(dnaStorage, files):
    pass # TODO