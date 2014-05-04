from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import random

class ToontownLoadingScreen:
    def __init__(self):
        self.__expectedCount = 0
        self.__count = 0
        self.gui = loader.loadModel('phase_3/models/gui/progress-background.bam')
        self.title = DirectLabel(guiId='ToontownLoadingScreenTitle', parent=self.gui, relief=None, pos=(base.a2dRight/5, 0, 0.235), text='', textMayChange=1, text_scale=0.08, text_fg=(0.03, 0.83, 0, 1), text_align=TextNode.ALeft, text_font=ToontownGlobals.getSignFont())
        self.waitBar = self.waitBar = DirectWaitBar(guiId='ToontownLoadingScreenWaitBar', parent=self.gui, frameSize=(base.a2dLeft+(base.a2dRight/4.95), base.a2dRight-(base.a2dRight/4.95), -0.03, 0.03), pos=(0, 0, 0.15), text='')
        self.toon = None
        
    def destroy(self):
        self.title.destroy()
        self.gui.removeNode()
        if self.toon:
            self.toon.delete()
        
    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + '\n' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def begin(self, range, label, gui, tipCategory):
        self.waitBar['range'] = range
        self.title['text'] = label
        self.__count = 0
        self.__expectedCount = range
        if gui:
            if base.localAvatarStyle:
                from toontown.toon import Toon
                self.toon = Toon.Toon()
                self.toon.setDNA(base.localAvatarStyle)
                self.toon.loop('bored', fromFrame=135, toFrame=135)
                self.toon.getGeomNode().setDepthWrite(1)
                self.toon.getGeomNode().setDepthTest(1)
                self.toon.setHpr(205, 0, 0)
                self.toon.setScale(0.18)
                self.toon.setPos(base.a2dBottomRight.getX()/1.25, 0, -0.034)
                self.toon.reparentTo(self.waitBar)
                self.waitBar['frameSize'] = (base.a2dLeft+(base.a2dRight/8.15), base.a2dRight-(base.a2dRight/2.57), -0.03, 0.03)
            self.title.reparentTo(base.a2dpBottomLeft, NO_FADE_SORT_INDEX)
            self.title.setPos(0.24, 0, 0.23)
            self.gui.setPos(0, -0.1, 0)
            self.gui.reparentTo(aspect2d, NO_FADE_SORT_INDEX)
        else:
            self.title.reparentTo(base.a2dpBottomLeft, NO_FADE_SORT_INDEX)
            self.gui.reparentTo(hidden)
        self.waitBar.reparentTo(base.a2dpBottomCenter, NO_FADE_SORT_INDEX)
        self.waitBar.update(self.__count)

    def end(self):
        self.waitBar.finish()
        self.waitBar.reparentTo(self.gui)
        self.title.reparentTo(self.gui)
        self.gui.reparentTo(hidden)
        if self.toon:
            self.toon.reparentTo(hidden)
        return (self.__expectedCount, self.__count)

    def abort(self):
        self.gui.reparentTo(hidden)

    def tick(self):
        self.__count = self.__count + 1
        self.waitBar.update(self.__count)
