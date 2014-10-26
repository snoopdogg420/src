from CatalogItemList import CatalogItemList
from CatalogInvalidItem import CatalogInvalidItem
from CatalogFurnitureItem import CatalogFurnitureItem
from CatalogChatItem import CatalogChatItem
from CatalogClothingItem import CatalogClothingItem
from CatalogEmoteItem import CatalogEmoteItem
from CatalogWallpaperItem import CatalogWallpaperItem
from CatalogWindowItem import CatalogWindowItem
from CatalogFlooringItem import CatalogFlooringItem
from CatalogMouldingItem import CatalogMouldingItem
from CatalogWainscotingItem import CatalogWainscotingItem
from CatalogPoleItem import CatalogPoleItem
from CatalogPetTrickItem import CatalogPetTrickItem
from CatalogBeanItem import CatalogBeanItem
from CatalogGardenItem import CatalogGardenItem
from CatalogRentalItem import CatalogRentalItem
from CatalogGardenStarterItem import CatalogGardenStarterItem
from CatalogNametagItem import CatalogNametagItem
from CatalogToonStatueItem import CatalogToonStatueItem
from CatalogAnimatedFurnitureItem import CatalogAnimatedFurnitureItem
from CatalogAccessoryItem import CatalogAccessoryItem


class PopularItemManagerAI:
    def __init__(self, air):
        self.air = air

        self.popularItemDict = {}

    def avBoughtItem(self, item):
        # Load the current popularItems
        try:
            popularItems = simbase.backups.load('catalog', ('popular-items',), default=({}))
        except ValueError:
            return

        itemOutput = item.output()

        # Don't allow rental items!
        if 'CatalogRentalItem' in itemOutput:
            return

        if not itemOutput in popularItems:
            popularItems[itemOutput] = 1
        else:
            popularItems[itemOutput] += 1

        # Save it.
        try:
            simbase.backups.save('catalog', ('popular-items',), (popularItems))
        except ValueError:
            pass

    def requestPopularItems(self):
        # Load the current popularItems
        try:
            self.popularItemDict = simbase.backups.load('catalog', ('popular-items',), default=({}))
        except ValueError:
            pass

        sortedItems = [(x,y) for y,x in sorted([(y,x) for x,y in self.popularItemDict.items()],reverse=True)]

        finalItems = []
        if len(sortedItems) <= 12:
            for item in sortedItems:
                item = eval(item[0])
                finalItems.append(item)
        else:
            for i in xrange(12):
                item = eval(sortedItems[i][0])
                finalItems.append(item)

        catalog = CatalogItemList(finalItems)
        return catalog.getBlob()

