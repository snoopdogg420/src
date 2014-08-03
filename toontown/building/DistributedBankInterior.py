from direct.distributed.ClockDelta import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm import ClassicFSM, State
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import random

import ToonInteriorColors
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *


class DistributedBankInterior(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.dnaStore = cr.playGame.dnaStore

        self.inVault = False
        self.vaultCollNodePath = None

        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedBankInterior',
            [
                State.State('off', self.enterOff, self.exitOff,
                            ['vaultClosed', 'vaultOpening', 'vaultOpen', 'vaultClosing']),
                State.State('vaultClosed', self.enterVaultClosed, self.exitVaultClosed,
                            ['vaultOpening']),
                State.State('vaultOpening', self.enterVaultOpening, self.exitVaultOpening,
                            ['vaultOpen']),
                State.State('vaultOpen', self.enterVaultOpen, self.exitVaultOpen,
                            ['vaultClosing']),
                State.State('vaultClosing', self.enterVaultClosing, self.exitVaultClosing,
                            ['vaultClosed'])
            ], 'off', 'off')
        self.fsm.enterInitialState()

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        self.setup()

    def disable(self):
        self.ignoreAll()

        self.interior.removeNode()
        del self.interior

        if self.collNodePath is not None:
            self.collNodePath.removeNode()
            self.collNodePath = None

        del self.vaultOpenSfx
        del self.vaultCloseSfx

        DistributedObject.disable(self)

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def setState(self, name, timestamp):
        self.fsm.request(name, [globalClockDelta.localElapsedTime(timestamp)])

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterVaultClosed(self, timestamp):
        vaultDoor = render.find('**/vault_door')
        vaultDoor.setH(0)

        if self.inVault:
            self.clearVault()

    def exitVaultClosed(self):
        pass

    def enterVaultOpening(self, timestamp):
        vaultDoor = render.find('**/vault_door')

        doorTrack = Sequence()

        # First, spin the vault lock dial:
        dial = vaultDoor.find('**/vault_door_front_dial')
        doorTrack.append(LerpHprInterval(dial, 2, Vec3(0, 0, -2160), startHpr=(0, 0, 0), blendType='easeOut', fluid=1))

        # Then, open the vault door:
        doorTrack.append(LerpHprInterval(vaultDoor, 3, Vec3(-120, 0, 0), startHpr=Vec3(0, 0, 0), blendType='easeOut'))

        # We need the sound effect to play in parallel:
        track = Parallel(SoundInterval(self.vaultOpenSfx, node=vaultDoor), doorTrack)
        track.start(timestamp)

    def exitVaultOpening(self):
        pass

    def enterVaultOpen(self, timestamp):
        vaultDoor = render.find('**/vault_door')
        vaultDoor.setH(-120)

    def exitVaultOpen(self):
        pass

    def enterVaultClosing(self, timestamp):
        vaultDoor = render.find('**/vault_door')

        doorTrack = Sequence()

        # First, close the vault door:
        doorTrack.append(LerpHprInterval(vaultDoor, 3, Vec3(0, 0, 0), startHpr=Vec3(-120, 0, 0), blendType='easeOut'))

        # Then, spin the vault lock dial:
        dial = vaultDoor.find('**/vault_door_front_dial')
        doorTrack.append(LerpHprInterval(dial, 2, Vec3(0, 0, 2160), startHpr=(0, 0, 0), blendType='easeOut', fluid=1))

        # We need the sound effect to play in parallel:
        track = Parallel(SoundInterval(self.vaultCloseSfx, node=vaultDoor), doorTrack)
        track.start(timestamp)

    def exitVaultClosing(self):
        pass

    def __handleEnterVaultBox(self, collEntry=None):
        self.inVault = True

        if self.fsm.getCurrentState().getName() == 'vaultClosed':
            self.clearVault()

    def __handleExitVaultBox(self, collEntry=None):
        self.inVault = False

    def clearVault(self):
        place = base.cr.playGame.getPlace()
        place.setState('stopped')
        self.teleportTrack = Sequence()
        self.teleportTrack.append(Func(base.localAvatar.b_setAnimState, 'TeleportOut'))
        self.teleportTrack.append(Wait(3.5))
        self.teleportTrack.append(Func(base.localAvatar.setPos, Point3(0, 0, 0)))
        self.teleportTrack.append(Func(base.localAvatar.b_setAnimState, 'TeleportIn'))
        self.teleportTrack.append(Wait(2.25))
        self.teleportTrack.append(Func(place.setState, 'walk'))
        self.teleportTrack.start()

    def randomDNAItem(self, category, findFunc):
        codeCount = self.dnaStore.getNumCatalogCodes(category)
        index = self.randomGenerator.randint(0, codeCount - 1)
        code = self.dnaStore.getCatalogCode(category, index)
        return findFunc(code)

    def replaceRandomInModel(self, model):
        baseTag = 'random_'
        npc = model.findAllMatches('**/' + baseTag + '???_*')
        for i in xrange(npc.getNumPaths()):
            np = npc.getPath(i)
            name = np.getName()
            b = len(baseTag)
            category = name[b + 4:]
            key1 = name[b]
            key2 = name[b + 1]
            if key1 == 'm':
                model = self.randomDNAItem(category, self.dnaStore.findNode)
                newNP = model.copyTo(np)
                if key2 == 'r':
                    self.replaceRandomInModel(newNP)
            elif key1 == 't':
                texture = self.randomDNAItem(category, self.dnaStore.findTexture)
                np.setTexture(texture, 100)
                newNP = np
            if key2 == 'c':
                if category == 'TI_wallpaper' or category == 'TI_wallpaper_border':
                    self.randomGenerator.seed(self.zoneId)
                    newNP.setColorScale(self.randomGenerator.choice(self.colors[category]))
                else:
                    newNP.setColorScale(self.randomGenerator.choice(self.colors[category]))

    def chooseDoor(self):
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        return door

    def setup(self):
        self.dnaStore = base.cr.playGame.dnaStore

        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)

        self.interior = loader.loadModel('phase_4/models/modules/ttc_bank_interior.bam')
        self.interior.reparentTo(render)

        self.vaultOpenSfx = loader.loadSfx('phase_4/audio/sfx/vault_door_open.ogg')
        self.vaultCloseSfx = loader.loadSfx('phase_4/audio/sfx/vault_door_close.ogg')

        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        self.replaceRandomInModel(self.interior)

        door = self.chooseDoor()
        doorOrigin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(doorOrigin)
        doorOrigin.setScale(0.8, 0.8, 0.8)
        doorOrigin.setPos(doorOrigin, 0, -0.025, 0)
        doorColor = self.randomGenerator.choice(self.colors['TI_door'])
        DNADoor.setupDoor(doorNP, self.interior, doorOrigin, self.dnaStore, str(self.block), doorColor)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)

        del self.colors
        del self.dnaStore
        del self.randomGenerator

        room = render.find('**/vault_walls')
        minPoint, maxPoint = room.getTightBounds()
        offset = 1  # We want a slight offset
        maxPoint -= offset
        collBox = CollisionBox(minPoint, maxPoint)
        collBox.setTangible(0)
        collNode = CollisionNode(self.uniqueName('vaultBox'))
        collNode.setIntoCollideMask(BitMask32(1))
        collNode.addSolid(collBox)
        self.collNodePath = render.attachNewNode(collNode)
        radius = ((maxPoint-minPoint) / 2).getZ()
        self.collNodePath.setPos(-11.2 + (offset/2), 14 + radius + offset, 0)

        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()

        self.accept(self.uniqueName('entervaultBox'), self.__handleEnterVaultBox)
        self.accept(self.uniqueName('exitvaultBox'), self.__handleExitVaultBox)
