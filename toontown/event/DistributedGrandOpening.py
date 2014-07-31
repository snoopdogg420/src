from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM

from toontown.movie.GrandOpeningMovie import GrandOpeningMovie


class DistributedGrandOpening(DistributedObject, FSM):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'DistributedGrandOpening')

        # We need a way to access this object globally:
        cr.grandOpening = self

        self.scene = None
        self.movie = None

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        geom = self.cr.playGame.hood.loader.geom
        self.scene = geom.attachNewNode('grandOpeningScene')

        # TODO: Create the scenery.

        self.movie = GrandOpeningMovie(self.scene)

    def delete(self):
        self.demand('Off')

        if self.movie is not None:
            self.movie.stop()
            self.movie = None

        if self.scene is not None:
            self.scene.removeNode()
            self.scene = None

        DistributedObject.delete(self)

    def enterOff(self):
        if self.scene:
            self.scene.reparentTo(hidden)

    def exitOff(self):
        if self.scene:
            geom = self.cr.playGame.hood.loader.geom
            self.scene.reparentTo(geom)
