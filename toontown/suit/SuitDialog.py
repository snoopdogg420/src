import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
notify = DirectNotifyGlobal.directNotify.newCategory('SuitDialog')

def getBrushOffIndex(suitName):
    if SuitBrushOffs.has_key(suitName):
        brushoffs = SuitBrushOffs[suitName]
    else:
        brushoffs = SuitBrushOffs[None]
    choice = random.choice(brushoffs)
    return brushoffs.index(choice)


def getBrushOffText(suitName, index):
    if SuitBrushOffs.has_key(suitName):
        brushoffs = SuitBrushOffs[suitName]
    else:
        brushoffs = SuitBrushOffs[None]
    return brushoffs[index]


SuitBrushOffs = OTPLocalizer.SuitBrushOffs
