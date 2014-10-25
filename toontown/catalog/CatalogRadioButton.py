from pandac.PandaModules import NodePath
from direct.gui.DirectButton import DirectButton
from toontown.catalog import CatalogGlobals


class CatalogRadioButton(NodePath):
    def __init__(self, parent, nodeName, clickEvent):
        NodePath.__init__(self, parent.attachNewNode(nodeName))

        self.radioButtons = []
        self.clickEvent = clickEvent

        self.normalNode = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'_UP').copyTo(self)
        self.clickedNode = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'_DN').copyTo(self)
        self.hoverNode = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'_OVR').copyTo(self)

        self.statusIndicator = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'Radio_ON').copyTo(self)
        self.statusIndicator.hide()

        self.radioButton = DirectButton(parent=self, relief=None, image=(self.normalNode, self.clickedNode, self.hoverNode), command=self.enable)

    def setOthers(self, radioButtons):
        self.radioButtons = radioButtons

    def enable(self):
        for radioButton in self.radioButtons:
            radioButton.disable()

        self.statusIndicator.show()
        self.clickEvent()

    def disable(self):
        self.statusIndicator.hide()

    def cleanup(self):
        self.radioButton.destroy()

        NodePath.removeNode(self)