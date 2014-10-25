from pandac.PandaModules import NodePath
from direct.gui.DirectButton import DirectButton
from toontown.catalog import CatalogGlobals


class CatalogTabButton(NodePath):
    def __init__(self, catalogGui, nodeName, clickEvent):
        NodePath.__init__(self, catalogGui.attachNewNode(nodeName))

        self.active = False
        self.activePage = 0
        self.catalogGui = catalogGui
        self.catalogItemPages = []
        self.otherTabs = []
        self.clickEvent = clickEvent

        self.clickedNode = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'_DN').copyTo(self)
        self.hoverNode = CatalogGlobals.CatalogNodePath.find('**/'+nodeName+'_OVR').copyTo(self)

        self.tabButton = DirectButton(parent=self, relief=None, image=(self.clickedNode, self.clickedNode, self.hoverNode), command=self.tabClicked)

    def tabClicked(self):
        if self.active:
            return
        for tab in self.otherTabs:
            tab.disableTab()
        self.active = True
        self.catalogGui.setCurrentTab(self)
        self.showPages()
        self.updateArrows()
        self.clickEvent()

    def setOtherTabs(self, otherTabs):
        self.otherTabs = otherTabs

    def setCatalogItemPages(self, catalogItemPages):
        self.catalogItemPages = catalogItemPages

    def showPages(self):
        self.hidePages()
        if self.catalogItemPages:
            self.catalogItemPages[self.activePage].show()
            self.catalogGui.setActivePage(self.activePage)

    def hidePages(self):
        for page in self.catalogItemPages:
            page.hide()

    def disableTab(self):
        if not self.active:
            return
        self.active = False
        self.hidePages()
        self.activePage = 0

    def updateArrows(self):
        self.catalogGui.enableBothArrows()
        if self.activePage == 0:
            self.catalogGui.disableLeftArrow()
        if self.activePage == len(self.catalogItemPages) - 1:
            self.catalogGui.disableRightArrow()

    def moveLeft(self):
        self.activePage -= 1
        self.showPages()
        self.updateArrows()

    def moveRight(self):
        self.activePage += 1
        self.showPages()
        self.updateArrows()

    def lockItems(self):
        for page in self.catalogItemPages:
            page.lockItems()

    def updateItems(self, gifting):
        for page in self.catalogItemPages:
            page.updateItems(gifting)

    def cleanup(self):
        for page in self.catalogItemPages:
            page.cleanup()

        self.tabButton.destroy()

        NodePath.removeNode(self)