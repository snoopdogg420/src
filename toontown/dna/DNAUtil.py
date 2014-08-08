from pandac.PandaModules import *

def dgiExtractString8(dgi):
    return dgi.extractBytes(dgi.getUint8())

def dgiExtractColor(dgi):
    return tuple(dgi.getUint8() / 255. for _ in xrange(4))

