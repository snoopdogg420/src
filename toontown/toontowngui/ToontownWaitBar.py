from direct.gui.DirectWaitBar import DirectWaitBar

class ToontownWaitBar(DirectWaitBar):

    def update(self, value):
        self['value'] = value

        if base.firstLoadDone:
            base.graphicsEngine.syncFrame()
            base.graphicsEngine.renderFrame()
