from pandac.PandaModules import *
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
import random


LOADING_SCREEN_SORT_INDEX = 4000


class ToontownLoadingScreen:

    defaultTex = 'phase_3.5/maps/loading/default.jpg'
    zone2picture = {
        ToontownGlobals.GoofySpeedway : 'phase_3.5/maps/loading/gs.jpg',
        ToontownGlobals.ToontownCentral : 'phase_3.5/maps/loading/ttc.jpg',
        ToontownGlobals.SillyStreet : 'phase_3.5/maps/loading/ttc_ss.jpg',
        ToontownGlobals.LoopyLane : 'phase_3.5/maps/loading/ttc_ll.jpg',
        ToontownGlobals.PunchlinePlace : 'phase_3.5/maps/loading/ttc_pp.jpg',
        ToontownGlobals.DonaldsDock : 'phase_3.5/maps/loading/dd.jpg',
        ToontownGlobals.BarnacleBoulevard : 'phase_3.5/maps/loading/dd_bb.jpg',
        ToontownGlobals.SeaweedStreet : 'phase_3.5/maps/loading/dd_ss.jpg',
        ToontownGlobals.LighthouseLane : 'phase_3.5/maps/loading/dd_ll.jpg',
        ToontownGlobals.DaisyGardens : 'phase_3.5/maps/loading/dg.jpg',
        ToontownGlobals.ElmStreet : 'phase_3.5/maps/loading/dg_es.jpg',
        ToontownGlobals.MapleStreet : 'phase_3.5/maps/loading/dg_ms.jpg',
        ToontownGlobals.OakStreet : 'phase_3.5/maps/loading/dg_os.jpg',
        ToontownGlobals.MinniesMelodyland : 'phase_3.5/maps/loading/mml.jpg',
        ToontownGlobals.AltoAvenue : 'phase_3.5/maps/loading/mml_aa.jpg',
        ToontownGlobals.BaritoneBoulevard : 'phase_3.5/maps/loading/mml_bb.jpg',
        ToontownGlobals.TenorTerrace : 'phase_3.5/maps/loading/mml_tt.jpg',
        ToontownGlobals.TheBrrrgh : 'phase_3.5/maps/loading/tb.jpg',
        ToontownGlobals.WalrusWay : 'phase_3.5/maps/loading/tb_ww.jpg',
        ToontownGlobals.SleetStreet : 'phase_3.5/maps/loading/tb_ss.jpg',
        ToontownGlobals.PolarPlace : 'phase_3.5/maps/loading/tb_pp.jpg',
        ToontownGlobals.DonaldsDreamland : 'phase_3.5/maps/loading/ddl.jpg',
        ToontownGlobals.LullabyLane : 'phase_3.5/maps/loading/ddl_ll.jpg',
        ToontownGlobals.PajamaPlace : 'phase_3.5/maps/loading/ddl_pp.jpg',
        ToontownGlobals.OutdoorZone : 'phase_3.5/maps/loading/oz.jpg',
        ToontownGlobals.GolfZone : 'phase_3.5/maps/loading/gz.jpg',
        ToontownGlobals.SellbotHQ : 'phase_3.5/maps/loading/sbhq.jpg',
        ToontownGlobals.CashbotHQ : 'phase_3.5/maps/loading/cbhq.jpg',
        ToontownGlobals.LawbotHQ : 'phase_3.5/maps/loading/lbhq.jpg',
        ToontownGlobals.BossbotHQ : 'phase_3.5/maps/loading/bbhq.jpg'
    }

    def __init__(self):
        self.__expectedCount = 0
        self.__count = 0
        self.gui = loader.loadModel('phase_3/models/gui/progress-background.bam')
        self.title = DirectLabel(guiId='ToontownLoadingScreenTitle', parent=self.gui, relief=None, pos=(base.a2dRight/5, 0, 0.235), text='', textMayChange=1, text_scale=0.08, text_fg=(0.03, 0.83, 0, 1), text_align=TextNode.ALeft, text_font=ToontownGlobals.getSignFont())
        self.waitBar = DirectWaitBar(guiId='ToontownLoadingScreenWaitBar', parent=self.gui, frameSize=(base.a2dLeft+(base.a2dRight/4.95), base.a2dRight-(base.a2dRight/4.95), -0.03, 0.03), pos=(0, 0, 0.15), text='')
        logoScale = 0.5625  # Scale for our locked aspect ratio (2:1).
        self.logo = OnscreenImage(
            image='phase_3/maps/toontown-logo.png',
            scale=(logoScale * 2.0, 1, logoScale))
        self.logo.reparentTo(hidden)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        scale = self.logo.getScale()
        # self.logo.setPos(scale[0], 0, -scale[2])
        self.logo.setPos(0, 0, -scale[2])
        self.toon = None

    def destroy(self):
        self.title.destroy()
        self.gui.removeNode()
        if self.toon:
            self.toon.delete()
        self.logo.removeNode()

    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + '\n' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def begin(self, range, label, gui, tipCategory, zoneId):
        self.waitBar['range'] = range
        self.title['text'] = label
        loadingScreenTex = self.zone2picture.get(ZoneUtil.getBranchZone(zoneId), self.defaultTex)
        self.background = loader.loadTexture(loadingScreenTex)
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
            self.title.reparentTo(base.a2dpBottomLeft, LOADING_SCREEN_SORT_INDEX)
            self.title.setPos(0.24, 0, 0.23)
            self.gui.setPos(0, -0.1, 0)
            self.gui.reparentTo(aspect2d, LOADING_SCREEN_SORT_INDEX)
            self.gui.setTexture(self.background, 1)
            if loadingScreenTex == self.defaultTex:
                self.logo.reparentTo(base.a2dpTopCenter, LOADING_SCREEN_SORT_INDEX)
        else:
            self.title.reparentTo(base.a2dpBottomLeft, LOADING_SCREEN_SORT_INDEX)
            self.gui.reparentTo(hidden)
            self.logo.reparentTo(hidden)
        self.waitBar.reparentTo(base.a2dpBottomCenter, LOADING_SCREEN_SORT_INDEX)
        self.waitBar.update(self.__count)

    def end(self):
        self.waitBar.finish()
        self.waitBar.reparentTo(self.gui)
        self.title.reparentTo(self.gui)
        self.gui.reparentTo(hidden)
        if self.toon:
            self.toon.reparentTo(hidden)
        self.logo.reparentTo(hidden)
        return (self.__expectedCount, self.__count)

    def abort(self):
        self.gui.reparentTo(hidden)

    def tick(self):
        self.__count = self.__count + 1
        self.waitBar.update(self.__count)
