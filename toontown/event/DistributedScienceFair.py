from direct.actor.Actor import Actor
from direct.distributed.DistributedObject import DistributedObject


class DistributedScienceFair(DistributedObject):
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        self.tent = loader.loadModel('phase_4/models/events/event_tent.bam')
        self.tent.reparentTo(render)
        self.tent.setPosHpr(0, 0, 0, 270, 0, 0)

        self.redFlag = Actor(loader.loadModel('phase_4/models/events/event_flag_mod_idle_red.bam'))
        self.redFlag.loadAnims({'waving': 'phase_4/models/events/event_flag_chan_wave1.bam'})
        self.redFlag.reparentTo(self.tent.find('**/flag1_jnt'))
        self.redFlag.loop('waving')

        self.blueFlag = Actor(loader.loadModel('phase_4/models/events/event_flag_mod_idle_blue.bam'))
        self.blueFlag.loadAnims({'waving': 'phase_4/models/events/event_flag_chan_wave1.bam'})
        self.blueFlag.reparentTo(self.tent.find('**/flag2_jnt'))
        self.blueFlag.loop('waving')

        self.tent2 = loader.loadModel('phase_4/models/events/event_tent.bam')
        self.tent2.reparentTo(render)
        self.tent2.setPosHpr(85.91, 149.76, 2.61, 327.99, 0, 0)

        #self.tent3 = Actor(loader.loadModel('phase_4/models/events/tele_anim02_repaired.bam'))
        #self.tent3.reparentTo(render)
        #self.tent3.setPosHpr(0, 0, 0, 0, 0, 0)
        #CHAN TRY AND FIGURE THIS BULL SHIT OUT! IT'S A SINGLE BAM FILE WITH AN ANIMATION AND A MODEL. IT DOESN'T LOAD THE ANIMATION IN GAME! ;-;

    def delete(self):
        if self.tent2 is not None:
            self.tent2.removeNode()
            self.tent2 = None

        if self.blueFlag is not None:
            self.blueFlag.cleanup()
            self.blueFlag = None

        if self.redFlag is not None:
            self.redFlag.cleanup()
            self.redFlag = None

        if self.tent is not None:
            self.tent.removeNode()
            self.tent = None

        DistributedObject.delete(self)
