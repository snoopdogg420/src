from panda3d.core import LVector4f

def dgiExtractString8(dgi):
    return dgi.extractBytes(dgi.getUint8())

def dgiExtractColor(dgi):
    return LVector4f(dgi.getUint8() / 255. for _ in xrange(4))

