from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
import time

from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.effects import DustCloud
from toontown.nametag.NametagGlobals import *
from toontown.toonbase import TTLocalizer


def getDustCloudIval(toon):
    dustCloud = DustCloud.DustCloud(fBillboard=0)
    dustCloud.setBillboardAxis(2.0)
    dustCloud.setZ(3)
    dustCloud.setScale(0.4)
    dustCloud.createTrack()
    if getattr(toon, 'laffMeter', None):
        toon.laffMeter.color = toon.style.getWhiteColor()
    seq = Sequence(Wait(0.5), Func(dustCloud.reparentTo, toon), dustCloud.track, Func(dustCloud.destroy))
    if getattr(toon, 'laffMeter', None):
        seq.append(Func(toon.laffMeter.adjustFace, toon.hp, toon.maxHp))
    return seq


class DistributedNPCYang(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

        self.pickColorGui = None
        self.pickColorGuiDoneEvent = 'pickColorGuiDone'

        self.nextCollision = 0

        self.fsm = ClassicFSM.ClassicFSM(
            'NPCYin',
            [
                State.State('off', self.enterOff, self.exitOff, ['pickColor']),
                State.State('pickColor', self.enterPickColor, self.exitPickColor, ['off'])
            ], 'off', 'off')
        self.fsm.enterInitialState()

        self.title = None
        self.yesButton = None
        self.noButton = None

        self.buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        self.upButton = self.buttonModels.find('**//InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')

    def disable(self):
        self.ignoreAll()

        if self.title:
            self.title.destroy()
            self.title = None

        if self.yesButton:
            self.yesButton.destroy()
            self.yesButton = None

        if self.noButton:
            self.noButton.destroy()
            self.noButton = None

        if self.buttonModels:
            self.buttonModels.removeNode()
            self.buttonModels = None

        if self.upButton:
            self.upButton.removeNode()
            self.upButton = None

        if self.downButton:
            self.downButton.removeNode()
            self.downButton = None

        if self.rolloverButton:
            self.rolloverButton.removeNode()
            self.rolloverButton = None

        if self.pickColorGui:
            self.pickColorGui.destroy()
            self.pickColorGui = None

        self.nextCollision = 0

        DistributedNPCToonBase.disable(self)

    def initToonState(self):
        self.setAnimState('neutral', 1.05, None, None)
        self.setPosHpr(101, -14, 4, -305, 0, 0)

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        self.currentTime = time.time()
        if self.nextCollision <= self.currentTime:
            self.fsm.request('pickColor')
        self.nextCollision = self.currentTime + 2

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterPickColor(self):
        base.cr.playGame.getPlace().setState('stopped')
        taskMgr.doMethodLater(15, self.leave, 'npcSleepTask-%s' % self.doId)
        self.setChatAbsolute('', CFSpeech)
        if base.localAvatar.style.getAnimal() != 'bear':
            self.setChatAbsolute(TTLocalizer.YangNotBear, CFSpeech|CFTimeout)
            self.fsm.request('off')
            base.cr.playGame.getPlace().setState('walk')
        elif base.localAvatar.style.headColor == 0x00:
            self.setChatAbsolute(TTLocalizer.YangAlreadyWhite, CFSpeech|CFTimeout)
            self.fsm.request('off')
            base.cr.playGame.getPlace().setState('walk')
        else:
            self.popupPickColorGUI()

    def exitPickColor(self, task=None):
        taskMgr.remove('npcSleepTask-%s' % self.doId)
        if self.title:
            self.title.destroy()
            self.title = None
        if self.yesButton:
            self.yesButton.destroy()
            self.yesButton = None
        if self.noButton:
            self.noButton.destroy()
            self.noButton = None

        if task is not None:
            return task.done

    def popupPickColorGUI(self):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.YangPickColor, CFSpeech)
        base.setCellsActive(base.bottomCells, 0)

        self.title = DirectLabel(
            aspect2d, relief=None, text=TTLocalizer.YangTitle,
            text_pos=(0, 0), text_fg=(1, 0, 0, 1), text_scale=0.09,
            text_font=ToontownGlobals.getSignFont(),
            pos=(0, 0, -0.55), text_shadow=(1, 1, 1, 1))
        self.yesButton = DirectButton(
            relief=None, text=TTLocalizer.lYes,
            text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23),
            text_scale=0.8, image=(self.upButton, self.downButton, self.rolloverButton),
            image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(-0.275, 0, -0.75), scale=0.15,
            command=lambda self=self: self.d_requestTransformation())
        self.noButton = DirectButton(
            relief=None, text=TTLocalizer.lNo,
            text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23),
            text_scale=0.8, image=(self.upButton, self.downButton, self.rolloverButton),
            image_color=(1, 0, 0, 1), image_scale=(20, 1, 11), pos=(0.275, 0, -0.75), scale=0.15,
            command=lambda self=self: self.leave())

    def doTransformation(self, avId):
        av = self.cr.doId2do.get(avId)
        if not av:
            return
        if av.style.getAnimal() != 'bear':
            return
        self.dustCloudIval = getDustCloudIval(av)
        self.dustCloudIval.start()

        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.YangEnjoy, CFSpeech|CFTimeout)
        base.setCellsActive(base.bottomCells, 1)

    def d_requestTransformation(self):
        self.sendUpdate('requestTransformation', [])
        self.fsm.request('off')
        base.cr.playGame.getPlace().setState('walk')

    def leave(self, task=None):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.YangGoodbye, CFSpeech|CFTimeout)
        self.fsm.request('off')
        base.cr.playGame.getPlace().setState('walk')
        base.setCellsActive(base.bottomCells, 1)

        if task is not None:
            return task.done
