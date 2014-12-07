from direct.distributed.DistributedNode import DistributedNode
from pandac.PandaModules import CollisionSphere, CollisionNode, TextNode
from pandac.PandaModules import BillboardEffect, Vec3, Point3
from direct.interval.IntervalGlobal import Parallel, Sequence, Func, Wait
from direct.interval.IntervalGlobal import LerpScaleInterval
from toontown.effects.DustCloud import DustCloud
from toontown.toonbase import ToontownGlobals
from toontown.event.ExperimentBarrelBase import ExperimentBarrelBase


class DistributedExperimentBarrel(ExperimentBarrelBase, DistributedNode):
    notify = directNotify.newCategory('DistributedExperimentBarrel')
    BARREL_SCALE = 0.5
    SPHERE_RADIUS = 3.8

    def __init__(self, cr):
        ExperimentBarrelBase.__init__(self)
        DistributedNode.__init__(self, cr)

        self.barrel = None
        self.icon = None
        self.collSphere = None
        self.collNode = None
        self.collNodePath = None
        self.animTrack = None

    def announceGenerate(self):
        DistributedNode.announceGenerate(self)

        self.reparentTo(render)
        self.loadBarrel()
        self.loadIcon()
        self.loadCollisions()

        self.accept(self.uniqueName('enterBarrelSphere'), self.__handleEnterSphere)

    def delete(self):
        if self.barrel:
            self.barrel.removeNode()

        if self.icon:
            self.icon.removeNode()

        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None

        self.ignore(self.uniqueName('enterBarrelSphere'))

        DistributedNode.delete(self)

    def loadBarrel(self):
        self.barrel = loader.loadModel('phase_4/models/cogHQ/gagTank')
        self.barrel.reparentTo(self)
        self.barrel.setH(self, 180)
        self.barrel.setScale(self.BARREL_SCALE)
        self.barrel.hide()

        dustCloud = DustCloud(fBillboard=0)
        dustCloud.setBillboardAxis(2.0)
        dustCloud.setZ(3)
        dustCloud.setScale(1.2)
        dustCloud.createTrack()
        Sequence(Func(dustCloud.reparentTo, self.barrel),
                 Parallel(dustCloud.track,
                          Func(self.barrel.show)),
                 Func(dustCloud.destroy)).start()

    def loadIcon(self):
        pass # TODO

    def loadCollisions(self):
        self.collSphere = CollisionSphere(0, 0, 0, self.SPHERE_RADIUS)
        self.collSphere.setTangible(0)
        self.collNode = CollisionNode(self.uniqueName('BarrelSphere'))
        self.collNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.barrel.attachNewNode(self.collNode)
        self.collNodePath.hide()

    def __handleEnterSphere(self, collEntry):
        self.requestGrab()

    def requestGrab(self):
        self.sendUpdate('requestGrab', [base.localAvatar.doId])

    def setGrab(self, avId):
        if avId == base.localAvatar.doId:
            self.ignore(self.uniqueName('enterBarrelSphere'))
            self.barrel.setColorScale(0.5, 0.5, 0.5, 1)
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None
        self.animTrack = Sequence(LerpScaleInterval(self.barrel,
                                                    0.2, 1.1 * self.BARREL_SCALE,
                                                    blendType='easeInOut'),
                                  LerpScaleInterval(self.barrel,
                                                    0.2,
                                                    self.BARREL_SCALE,
                                                    blendType='easeInOut'),
                                  Func(self.barrel.setScale,
                                       self.BARREL_SCALE))
        self.animTrack.start()
