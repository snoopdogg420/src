from pandac.PandaModules import *


class MarginCell(NodePath):
    def __init__(self):
        NodePath.__init__(self, 'cell')

        self.active = False
        self.content = None

    def setActive(self, active):
        self.active = active

    def getActive(self):
        return self.active

    def setContent(self, content):
        if self.content is not None:
            self.content.setCell(None)
            if hasattr(self, 'contentNodePath'):
                self.contentNodePath.removeNode()
                del self.contentNodePath
            self.content.marginVisibilityChanged()

        if content is not None:
            content.setLastCell(self)
            content.setCell(self)
            self.contentNodePath = self.attachNewNode(content)
            content.marginVisibilityChanged()

        self.content = content

    def getContent(self):
        return self.content
