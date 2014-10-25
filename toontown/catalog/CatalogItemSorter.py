from CatalogFurnitureItem import CatalogFurnitureItem # Furniture
from CatalogChatItem import CatalogChatItem # Phrase
from CatalogClothingItem import CatalogClothingItem # Clothing
from CatalogEmoteItem import CatalogEmoteItem # Emotion
from CatalogWallpaperItem import CatalogWallpaperItem # Furniture
from CatalogWindowItem import CatalogWindowItem # Furniture
from CatalogFlooringItem import CatalogFlooringItem # Furniture
from CatalogMouldingItem import CatalogMouldingItem # Furniture
from CatalogWainscotingItem import CatalogWainscotingItem # Furniture
from CatalogPoleItem import CatalogPoleItem # Special
from CatalogPetTrickItem import CatalogPetTrickItem # Special
from CatalogBeanItem import CatalogBeanItem # Furniture
from CatalogGardenItem import CatalogGardenItem # Special
from CatalogRentalItem import CatalogRentalItem # Special
from CatalogGardenStarterItem import CatalogGardenStarterItem # Special
from CatalogNametagItem import CatalogNametagItem # Nametag
from CatalogToonStatueItem import CatalogToonStatueItem # Special
from CatalogAnimatedFurnitureItem import CatalogAnimatedFurnitureItem # Furniture
from CatalogAccessoryItem import CatalogAccessoryItem # Clothing


class CatalogItemSorter:
    SPECIAL_ITEMS = (CatalogToonStatueItem, CatalogPoleItem, CatalogGardenStarterItem,
                     CatalogGardenItem, CatalogRentalItem, CatalogPetTrickItem)
    NAMETAG_ITEMS = (CatalogNametagItem,)
    PHRASE_ITEMS = (CatalogChatItem,)
    CLOTHING_ITEMS = (CatalogAccessoryItem, CatalogClothingItem)
    EMOTION_ITEMS = (CatalogEmoteItem,)
    FURNITURE_ITEMS = (CatalogFurnitureItem, CatalogWallpaperItem, CatalogWindowItem,
                       CatalogFlooringItem, CatalogMouldingItem, CatalogWainscotingItem,
                       CatalogBeanItem, CatalogAnimatedFurnitureItem)

    def __init__(self, itemList):
        self.itemList = itemList

        self.sortedItems = {
          'UNSORTED': [],
          'SPECIAL': [],
          'CLOTHING': [],
          'PHRASES': [],
          'EMOTIONS': [],
          'FURNITURE': [],
          'NAMETAG': []
        }

    def sortItems(self):
        for item in self.itemList:
            if self.__isSpecial(item):
                self.sortedItems['SPECIAL'].append(item)
            elif self.__isNametag(item):
                self.sortedItems['NAMETAG'].append(item)
            elif self.__isClothing(item):
                self.sortedItems['CLOTHING'].append(item)
            elif self.__isPhrase(item):
                self.sortedItems['PHRASES'].append(item)
            elif self.__isEmotion(item):
                self.sortedItems['EMOTIONS'].append(item)
            elif self.__isFurniture(item):
                self.sortedItems['FURNITURE'].append(item)
            else:
                self.sortedItems['UNSORTED'].append(item)
        return self.sortedItems

    def __isSpecial(self, item):
        return isinstance(item, CatalogItemSorter.SPECIAL_ITEMS)

    def __isClothing(self, item):
        return isinstance(item, CatalogItemSorter.CLOTHING_ITEMS)

    def __isPhrase(self, item):
        return isinstance(item, CatalogItemSorter.PHRASE_ITEMS)

    def __isNametag(self, item):
        return isinstance(item, CatalogItemSorter.NAMETAG_ITEMS)

    def __isEmotion(self, item):
        return isinstance(item, CatalogItemSorter.EMOTION_ITEMS)

    def __isFurniture(self, item):
        return isinstance(item, CatalogItemSorter.FURNITURE_ITEMS)