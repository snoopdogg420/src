from pandac.PandaModules import NodePath
from toontown.catalog.CatalogTabButton import CatalogTabButton
from toontown.catalog.CatalogArrowButton import CatalogArrowButton
from toontown.catalog.CatalogRadioButton import CatalogRadioButton
from toontown.catalog import CatalogGlobals


class CatalogGUI(NodePath):
    def __init__(self):
        NodePath.__init__(self, aspect2d.attachNewNode('CatalogGUI'))

        CatalogGlobals.CatalogNodePath.find('**/CATALOG_GUI_BKGD').copyTo(self)
        self.setScale(CatalogGlobals.CatalogBKGDScale)

        self.tabButtons = {}
        self.createTabButtons()

        self.arrowButtons = {}
        self.createArrowButtons()

        self.radioButtons = []
        self.createRadioButtons()

    def createTabButtons(self):
        # We need to create the tabs in reverse order...
        self.tabButtons['SPECIAL_TAB'] = CatalogTabButton(self, 'BTN7',
                                                          self.specialTabClicked)
        self.tabButtons['NAMETAG_TAB'] = CatalogTabButton(self, 'BTN6',
                                                          self.nametagTabClicked)
        self.tabButtons['CLOTHING_TAB'] = CatalogTabButton(self, 'BTN5',
                                                           self.clothingTabClicked)
        self.tabButtons['PHRASES_TAB'] = CatalogTabButton(self, 'BTN4',
                                                          self.phrasesTabClicked)
        self.tabButtons['EMOTE_TAB'] = CatalogTabButton(self, 'BTN3',
                                                        self.emoteTabClicked)
        self.tabButtons['FURNITURE_TAB'] = CatalogTabButton(self, 'BTN2',
                                                            self.furnitureTabClicked)
        self.tabButtons['POPULAR_TAB'] = CatalogTabButton(self, 'BTN1',
                                                          self.popularTabClicked)

    def popularTabClicked(self):
        pass

    def furnitureTabClicked(self):
        pass

    def emoteTabClicked(self):
        pass

    def phrasesTabClicked(self):
        pass

    def clothingTabClicked(self):
        pass

    def nametagTabClicked(self):
        pass

    def specialTabClicked(self):
        pass

    def createArrowButtons(self):
        self.arrowButtons['LEFT_ARROW'] = CatalogArrowButton(self, 'LT',
                                                             self.leftArrowClicked)
        self.arrowButtons['RIGHT_ARROW'] = CatalogArrowButton(self, 'RT',
                                                              self.rightArrowClicked)

    def leftArrowClicked(self):
        pass

    def rightArrowClicked(self):
        pass

    def createRadioButtons(self):
        byNameRadioButton = CatalogRadioButton(self, 'ByName',
                                               self.byNameRadioButtonClicked)
        byCostRadioButton = CatalogRadioButton(self, 'ByCost',
                                               self.byCostRadioButtonClicked)

        self.radioButtons.append(byNameRadioButton)
        self.radioButtons.append(byCostRadioButton)

        for radioButton in self.radioButtons:
            radioButton.setOthers(self.radioButtons)

        byNameRadioButton.enable()

    def byNameRadioButtonClicked(self):
        pass

    def byCostRadioButtonClicked(self):
        pass