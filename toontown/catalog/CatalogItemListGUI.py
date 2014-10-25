from toontown.catalog.CatalogItemPage import CatalogItemPage


class CatalogItemListGUI:
    def __init__(self, catalogGui):
        self.catalogGui = catalogGui
        self.items = {}
        self.pages = []

    def getPages(self):
        return self.pages

    def addItem(self, item, category):
        if category not in self.items:
            self.items[category] = []
        if not item in self.items[category]:
            self.items[category].append(item)

    def generatePages(self):
        for category in self.items.keys():
            pageNum = 1
            currPage = CatalogItemPage(self.catalogGui, category, pageNum)
            for (x, item) in enumerate(self.items[category]):
                if x % 12 == 0 and x != 0:
                    self.pages.append(currPage)
                    pageNum += 1
                    currPage = CatalogItemPage(self.catalogGui, category, pageNum)
                currPage.addCatalogItem(item)
            if not currPage in self.pages:
                self.pages.append(currPage)
        for page in self.pages:
            page.generatePage()
        return self.pages
