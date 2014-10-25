from pandac.PandaModules import NodePath
from direct.gui.DirectButton import DirectButton
from toontown.catalog import CatalogGlobals


class CatalogArrowButton(NodePath):
    def __init__(self, parent, nodeName, clickEvent):
        NodePath.__init__(self, parent.attachNewNode(nodeName))

        self.clickEvent = clickEvent

        self.normalNode = CatalogGlobals.CatalogNodePath.find('**/arrow_UP_'+nodeName).copyTo(self)
        self.clickedNode = CatalogGlobals.CatalogNodePath.find('**/arrow_DN_'+nodeName).copyTo(self)
        self.hoverNode = CatalogGlobals.CatalogNodePath.find('**/arrow_OVR_'+nodeName).copyTo(self)

        self.arrowButton = DirectButton(parent=self, relief=None, image=(self.normalNode, self.clickedNode, self.hoverNode), command=self.clickEvent)

    def cleanup(self):
        self.arrowButton.destroy()

        NodePath.removeNode(self)