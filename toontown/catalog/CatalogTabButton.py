from pandac.PandaModules import NodePath
from direct.gui.DirectButton import DirectButton
from toontown.catalog import CatalogGlobals


class CatalogTabButton(NodePath):
    def __init__(self, parent, nodeName, clickEvent):
        NodePath.__init__(self, parent.attachNewNode(nodeName))

        self.clickEvent = clickEvent

        self.clickedNode = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'_DN').copyTo(self)
        self.hoverNode = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'_OVR').copyTo(self)

        self.tabButton = DirectButton(parent=self, relief=None, image=(self.clickedNode, self.clickedNode, self.hoverNode), command=self.clickEvent)
