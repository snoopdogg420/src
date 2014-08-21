from direct.gui.DirectWaitBar import DirectWaitBar

class ToontownWaitBar(DirectWaitBar):

    def update(self, value):
        self['value'] = value