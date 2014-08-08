from direct.task.Task import Task
from pandac.PandaModules import *

from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals


class Nametag2d(Nametag.Nametag):
    def __init__(self):
        Nametag.Nametag.__init__(self)

        self.arrow = None

        self.hideThought()
        self.contents.setScale(0.25)
        self.setChatWordWrap(8)

    def getChatBalloonModel(self):
        return NametagGlobals.chatBalloon2dModel

    def getChatBalloonWidth(self):
        return NametagGlobals.chatBalloon2dWidth

    def getChatBalloonHeight(self):
        return NametagGlobals.chatBalloon2dHeight

    def getThoughtBalloonModel(self):
        return NametagGlobals.thoughtBalloonModel

    def getThoughtBalloonWidth(self):
        return NametagGlobals.thoughtBalloonWidth

    def getThoughtBalloonHeight(self):
        return NametagGlobals.thoughtBalloonHeight

    def tick(self, task):
        return Task.cont

    def destroy(self):
        Nametag.Nametag.destroy(self)

        if self.arrow:
            self.arrow.removeNode()
            self.arrow = None
