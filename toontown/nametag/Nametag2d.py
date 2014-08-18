from direct.task.Task import Task
from pandac.PandaModules import *

from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals


class Nametag2d(Nametag.Nametag):
    CONTENTS_SCALE = 0.25

    CHAT_TEXT_WORD_WRAP = 8

    def __init__(self):
        Nametag.Nametag.__init__(self)

        self.arrow = None

        self.hideThought()
        self.contents.setScale(Nametag2d.CONTENTS_SCALE)
        self.setChatWordWrap(Nametag2d.CHAT_TEXT_WORD_WRAP)

    def destroy(self):
        Nametag.Nametag.destroy(self)

        if self.arrow:
            self.arrow.removeNode()
            self.arrow = None

    def getChatBalloonModel(self):
        return NametagGlobals.chatBalloon2dModel

    def getChatBalloonWidth(self):
        return NametagGlobals.chatBalloon2dWidth

    def getChatBalloonHeight(self):
        return NametagGlobals.chatBalloon2dHeight

    def tick(self, task):
        return Task.done
