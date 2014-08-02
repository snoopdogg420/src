from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

from otp.otpbase import OTPGlobals
from toontown.effects import DustCloud


class DistributedBankCollectable(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.grabbed = False
        self.nodePath = None
        self.bankCollectable = None
        self.collNodePath = None
        self.grabSound = None
        self.rotateIval = None
        self.floatIval = None
        self.flyTrack = None

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        self.nodePath = NodePath(self.uniqueName('bankCollectable'))
        self.nodePath.setScale(0.9)

        self.bankCollectable = self.nodePath.attachNewNode('bankCollectable')

        collSphere = CollisionSphere(0, 0, 0, 2)
        collSphere.setTangible(0)
        collNode = CollisionNode(self.uniqueName('bankCollectableSphere'))
        collNode.setIntoCollideMask(OTPGlobals.WallBitmask)
        collNode.addSolid(collSphere)
        self.collNodePath = self.nodePath.attachNewNode(collNode)

        model = loader.loadModel('phase_5.5/models/estate/jellybeanJar.bam')
        model.setTransparency(TransparencyAttrib.MDual, 1)
        model.find('**/jellybeansinbowl').setColorScale(1, 1, 1, 0.5)
        model.reparentTo(self.bankCollectable)

        self.grabSound = loader.loadSfx('phase_4/audio/sfx/SZ_DD_treasure.ogg')

        self.nodePath.wrtReparentTo(render)

        jellybeanjar = self.bankCollectable.find('**/jellybeanjar')
        self.rotateTrack = LerpHprInterval(jellybeanjar, 5, Vec3(360, 0, 0))
        self.rotateTrack.loop()

        self.floatTrack = Sequence()
        self.floatTrack.append(LerpPosInterval(self.nodePath, 2, Point3(-22, 27.5, 2), startPos=Point3(-22, 27.5, 1.5)))
        self.floatTrack.append(LerpPosInterval(self.nodePath, 2, Point3(-22, 27.5, 1.5), startPos=Point3(-22, 27.5, 2)))
        self.floatTrack.loop()

        glow = jellybeanjar.copyTo(self.bankCollectable)
        glow.setScale(1.1)

        glowTrack = Sequence()
        glowTrack.append(LerpColorScaleInterval(glow, 2.5, Vec4(0.6, 0.6, 0, 0.6), startColorScale=Vec4(0.4, 0.4, 0, 0.6)))
        glowTrack.append(LerpColorScaleInterval(glow, 2.5, Vec4(0.4, 0.4, 0, 0.6), startColorScale=Vec4(0.6, 0.6, 0, 0.6)))
        glowTrack.loop()

        self.accept(self.uniqueName('enterbankCollectableSphere'), self.__handleEnterSphere)

    def disable(self):
        self.ignoreAll()

        DistributedObject.disable(self)

    def delete(self):
        # When the bank collectable is deleted, and has not been grabbed, do a
        # poof effect:
        if not self.grabbed:
            dustCloud = DustCloud.DustCloud(fBillboard=0)
            dustCloud.setBillboardAxis(2.0)
            dustCloud.setZ(4)
            dustCloud.setScale(0.4)
            dustCloud.createTrack()
            dustCloud.reparentTo(render)
            dustCloud.setPos(self.nodePath.getPos())
            Sequence(dustCloud.track, Func(dustCloud.destroy)).start()

        if self.flyTrack is not None:
            self.flyTrack.finish()
            self.flyTrack = None

        if self.floatTrack is not None:
            self.floatTrack.finish()
            self.floatTrack = None

        if self.rotateTrack is not None:
            self.rotateTrack.finish()
            self.rotateTrack = None

        if self.nodePath is not None:
            self.nodePath.removeNode()
            self.nodePath = None

        DistributedObject.delete(self)

    def grab(self, avId):
        self.__handleGrab(avId)

    def d_requestGrab(self):
        self.sendUpdate('requestGrab', [])

    def __handleUnexpectedExit(self):
        if self.flyTrack:
            self.flyTrack.finish()
            self.flyTrack = None

    def __handleEnterSphere(self, collEntry=None):
        self.d_requestGrab()

    def __handleGrab(self, avId):
        self.collNodePath.stash()

        self.grabbed = True

        av = self.cr.doId2do.get(avId)
        if not av:
            self.nodePath.removeNode()
            self.nodePath = None
            return

        base.playSfx(self.grabSound, node=self.nodePath)

        self.nodePath.wrtReparentTo(av)
        if self.flyTrack:
            self.flyTrack.finish()
            self.flyTrack = None

        unexpectedExitEvent = av.uniqueName('disable')
        self.accept(unexpectedExitEvent, self.__handleUnexpectedExit)

        track = Sequence(
            LerpPosInterval(
                self.nodePath, 1, pos=Point3(0, 0, 3),
                startPos=self.nodePath.getPos(), blendType='easeInOut'),
            Func(self.nodePath.detachNode),
            Func(self.ignore, unexpectedExitEvent))
        self.flyTrack = Sequence(track, name=self.uniqueName('flyTrack'))
        self.flyTrack.start()
