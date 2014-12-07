from pandac.PandaModules import NodePath, TextNode, Vec4
from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from direct.interval.IntervalGlobal import LerpColorScaleInterval, Sequence, Func
from toontown.toonbase import ToontownGlobals


class ExperimentChallengeGUI(NodePath):
    def __init__(self, description, needed, icon):
        NodePath.__init__(self, 'objective-%s' % id(self))

        self.needed = needed
        self.visible = False

        self.fadeInTrack = None
        self.fadeOutTrack = None

        gui = loader.loadModel('phase_5/models/cogdominium/tt_m_gui_csa_flyThru')
        self.background = gui.find('**/*background').copyTo(self)
        self.background.setScale(2.5)
        gui.removeNode()

        self.icon = icon.copyTo(self.background)
        self.icon.setScale(0.08)
        self.icon.setPos(-0.167, 0, -0.002)

        text = TextNode('challenge')
        text.setText('Challenge')
        text.setFont(ToontownGlobals.getSignFont())
        text.setTextColor(0.95, 0.95, 0, 1)
        self.objText = self.background.attachNewNode(text)
        self.objText.setScale(0.03)
        self.objText.setPos(-0.04, 0.0, 0.02)

        text = TextNode('description')
        text.setText(description)
        text.setFont(ToontownGlobals.getSignFont())
        text.setTextColor(0.95, 0.95, 0, 1)
        text.setAlign(TextNode.ACenter)
        self.objText = self.background.attachNewNode(text)
        self.objText.setScale(0.015)
        self.objText.setPos(0.048, 0.0, -0.009)

        self.progressBar = DirectWaitBar(guiId='ChallengeProgressBar', parent=self.background, frameSize=(-0.11, 0.11, -0.007, 0.007), pos=(0.048, 0, -0.0338), text='')
        self.progressBar['range'] = needed

        self.progressText = DirectLabel(guiId='ChallengeProgressText', parent=self.progressBar, relief=None, pos=(0, 0, -0.0048), text='', textMayChange=1, text_scale=0.014, text_fg=(0.03, 0.83, 0, 1), text_align=TextNode.ACenter, text_font=ToontownGlobals.getSignFont())

        self.updateProgress(0)

        self.reparentTo(base.a2dBottomLeft)
        self.stash()

    def updateProgress(self, count):
        self.progressBar.update(count)
        self.progressText['text'] = '%s/%s' % (count, self.needed)

    def fadeIn(self):
        if self.fadeOutTrack:
            self.fadeOutTrack.finish()
            self.fadeOutTrack = None

        self.visible = True
        self.fadeInTrack = Sequence(Func(self.unstash),
                 Func(self.setTransparency, 1),
                 LerpColorScaleInterval(self, 1, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0)),
                 Func(self.clearColorScale),
                 Func(self.clearTransparency))
        self.fadeInTrack.start()

    def fadeOut(self):
        if self.fadeInTrack:
            self.fadeInTrack.finish()
            self.fadeInTrack = None

        self.visible = False
        self.fadeOutTrack = Sequence(Func(self.setTransparency, 1),
                 LerpColorScaleInterval(self, 1, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1)),
                 Func(self.clearColorScale),
                 Func(self.clearTransparency),
                 Func(self.stash))
        self.fadeOutTrack.start()

    def fadeOutDestroy(self):
        self.visible = False
        Sequence(Func(self.setTransparency, 1),
                 LerpColorScaleInterval(self, 1, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1)),
                 Func(self.clearColorScale),
                 Func(self.clearTransparency),
                 Func(self.stash),
                 Func(self.destroy)).start()

    def destroy(self):
        self.removeNode()
