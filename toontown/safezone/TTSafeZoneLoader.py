from toontown.safezone import SafeZoneLoader
from toontown.safezone import TTPlayground
from direct.actor.Actor import Actor


class TTSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TTPlayground.TTPlayground
        self.musicFile = 'phase_4/audio/bgm/TC_nbrhood.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_4/dna/toontown_central_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_4/dna/storage_TT_sz.pdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg',
                                            'phase_4/audio/sfx/SZ_TC_bird2.ogg',
                                            'phase_4/audio/sfx/SZ_TC_bird3.ogg'])
        bank = self.geom.find('**/*toon_landmark_TT_bank_DNARoot')
        doorTrigger = bank.find('**/door_trigger*')
        doorTrigger.setY(doorTrigger.getY() - 1.5)


        ### Judgement Day: The Grand Opening Massacre prototype scene ###
        ### The models below are being loaded to create the prototype scene. This should be deleted later. ###
        ### Prototype by Markgasus ###

        eventStage = loader.loadModel("phase_4/models/events/event_stage.bam")
        eventStage.reparentTo(self.geom)
        eventStage.setPos(68.08,0.67,4.025)
        eventStage.setHpr(-447.775,0,0)
        eventStage.setScale(1.2)

        balloonArchway = loader.loadModel("phase_4/models/events/balloon_archway_spiraled.bam")
        balloonArchway.reparentTo(self.geom)
        balloonArchway.setPos(80,0.67,4.025)
        balloonArchway.setHpr(-447.775,0,0)
        balloonArchway.setScale(2,2.8,1.5)

        barriers = loader.loadModel("phase_4/models/events/ttc_barriers.bam")
        barriers.reparentTo(self.geom)
        barriers.setPos(-1.2,-0.5,0)
        barriers.setHpr(-90,0,0)

        cutSection = loader.loadModel("phase_4/models/events/ttc_barriers_cutSection_mod.bam")
        cutSection.reparentTo(self.geom)
        cutSection.setPos(0,-0.81,0)

        eventTent = loader.loadModel("phase_4/models/events/event_tent.bam")
        eventTent.reparentTo(self.geom)
        eventTent.setPos(0,0,0)

        self.blueFlag = Actor('phase_4/models/events/event-flag-mod.bam', {'wave': 'phase_4/models/events/event-flag-anim.bam'})
        self.blueFlag.reparentTo(eventTent.find('**/flag1_jnt'))
        self.blueFlag.setH(90)
        self.blueFlag.loop('wave')

        #self.blueFlag.reparentTo(self.geom)
        #self.blueFlag.loop('wave')

        #redFlag = Actor('phase_4/models/events/event-flag-mod.bam', {'wave': 'phase_4/models/events/event-flag-anim.bam'})
        #redFlag.reparentTo(tent.find('**/flag2_jnt'))
        #redFlag.setH(90)
        #redFlag.loop('wave')

        self.blimpMod = loader.loadModel('phase_4/models/events/blimp_mod.bam')

        self.blimpStart = Actor(self.blimpMod)
        self.blimpStart.loadAnims({'flying': 'phase_4/models/events/blimp_chan_flying.bam'})
        self.blimpStart.reparentTo(self.geom)
        self.blimpStart.loop('flying')
        self.blimpStart.setPos(144,-188,55)
        self.blimpStart.setHpr(140,0,5)

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.birdSound

