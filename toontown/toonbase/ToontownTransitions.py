from direct.showbase.Transitions import Transitions

class ToontownTransitions(Transitions):
    IrisModelName = 'phase_3/models/misc/iris'
    FadeModelName = 'phase_3/models/misc/fade'

    def fadeIn(self, t=0.5, finishIval=None):

        base.graphicsEngine.syncFrame()
        base.graphicsEngine.renderFrame()

        if (t == 0):
            self.noTransitions()
            self.loadFade()
            self.fade.detachNode()
        else:
            self.transitionIval = self.getFadeInIval(t, finishIval)
            self.transitionIval.start()

