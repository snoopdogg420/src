from pandac.PandaModules import *


class ChatBalloon:
    def __init__(self, model):
        self.model = model

    def create(self, chatText, font, foreground=VBase4(0, 0, 0, 1),
        background=VBase4(1, 1, 1, 1), wordWrap=10, button=None):
        pass