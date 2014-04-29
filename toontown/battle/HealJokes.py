from toontown.toonbase import TTLocalizer
toonHealJokes = TTLocalizer.ToonHealJokes

class HealJokes(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('HealJokes')

    def __init__(self, doneEvent):
        self.notify.debug('What goes TICK-TICK-TICK-WOOF? A watchdog!')
        self.notify.debug('A watchdog!')
        StateData.StateData.__init__(self, doneEvent)
        self.numAvatars = 0
        self.chosenAvatar = 0
        self.toon = 1
        self.loaded = 1

        return None