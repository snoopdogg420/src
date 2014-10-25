from pandac.PandaModules import NodePath, TextNode
from toontown.catalog import CatalogGlobals
from toontown.catalog.CatalogItemPanel import CatalogItemPanel
from toontown.toonbase import ToontownGlobals


class CatalogItemPage(NodePath):
    def __init__(self, parent, category, pageNum):
        NodePath.__init__(self, parent.attachNewNode(category))

        self.parent = parent
        self.pageNum = pageNum
        self.category = category
        self.catalogItems = []
        self.itemFrames = []
        self.textNode = None

    def addCatalogItem(self, item):
        if not item in self.catalogItems:
            self.catalogItems.append(item)

    def setCatalogItems(self, catalogItems):
        self.catalogItems = catalogItems

    def generatePage(self):
        pageText = '%s - %s' % (self.category, self.pageNum)
        self.textNode = TextNode(pageText)
        self.textNode.setText(pageText)
        self.textNode.setFont(ToontownGlobals.getInterfaceFont())
        self.textNode = self.attachNewNode(self.textNode)
        self.textNode.setPos(*CatalogGlobals.ItemPageTextLoc)
        self.textNode.setScale(CatalogGlobals.ItemPageTextScale)
        self.textNode.setColor(0, 0, 0, 1)
        for (x, item) in enumerate(self.catalogItems):
            itemFrame = CatalogItemPanel(parent=self, parentCatalogScreen=self.parent, item=item)
            itemFrame.load()
            itemFrame.setPos(*CatalogGlobals.CatalogPropPos[x])
            self.itemFrames.append(itemFrame)

    def lockItems(self):
        for itemFrame in self.itemFrames:
            itemFrame.lockItem()

    def updateItems(self, gifting):
        for itemFrame in self.itemFrames:
            itemFrame.updateButtons(gifting)

    def cleanup(self):
        for item in self.catalogItems:
            if hasattr(item, 'destroy'):
                item.destroy()

        for itemFrame in self.itemFrames:
            itemFrame.destroy()

        NodePath.removeNode(self)