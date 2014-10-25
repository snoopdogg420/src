from pandac.PandaModules import NodePath, Vec4
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectButton import DirectButton
from toontown.catalog.CatalogTabButton import CatalogTabButton
from toontown.catalog.CatalogArrowButton import CatalogArrowButton
from toontown.catalog.CatalogRadioButton import CatalogRadioButton
from toontown.catalog import CatalogGlobals
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


class CatalogGUI(NodePath, DirectObject):
    def __init__(self, phone, doneEvent=None):
        NodePath.__init__(self, aspect2d.attachNewNode('CatalogGUI'))
        DirectObject.__init__(self)

        CatalogGlobals.CatalogNodePath.find('**/CATALOG_GUI_BKGD').copyTo(self)
        self.setScale(CatalogGlobals.CatalogBKGDScale)

        self.phone = phone
        self.doneEvent = doneEvent

        self.arrowButtons = {}
        self.createArrowButtons()

        self.currentTab = None
        self.tabButtons = {}
        self.createTabButtons()

        self.radioButtons = []
        # self.createRadioButtons()

        self.activePage = 0
        self.gifting = -1

        guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
        hangupGui = guiItems.find('**/hangup')
        hangupRolloverGui = guiItems.find('**/hangup_rollover')
        self.hangup = DirectButton(self, relief=None, pos=(2.28, 0, -1.3),
                                   image=[hangupGui, hangupRolloverGui, hangupRolloverGui, hangupGui],
                                   text=['', TTLocalizer.CatalogHangUp, TTLocalizer.CatalogHangUp],
                                   text_fg=Vec4(1), text_scale=0.07, text_pos=(0.0, 0.14),
                                   command=self.hangUp)
        guiItems.removeNode()

    def setCurrentTab(self, tab):
        self.currentTab = tab

    def getCurrentTab(self):
        return self.currentTab

    def setActivePage(self, activePage):
        self.activePage = activePage

    def getActivePage(self):
        return self.activePage

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
        tabList = []
        for tab in self.tabButtons:
            tabList.append(self.tabButtons[tab])

        for tab in self.tabButtons:
            self.tabButtons[tab].setOtherTabs(tabList)

    def popularTabClicked(self):
        messenger.send('wakeup')

    def furnitureTabClicked(self):
        messenger.send('wakeup')

    def emoteTabClicked(self):
        messenger.send('wakeup')

    def phrasesTabClicked(self):
        messenger.send('wakeup')

    def clothingTabClicked(self):
        messenger.send('wakeup')

    def nametagTabClicked(self):
        messenger.send('wakeup')

    def specialTabClicked(self):
        messenger.send('wakeup')

    def createArrowButtons(self):
        self.arrowButtons['LEFT_ARROW'] = CatalogArrowButton(self, 'LT',
                                                             self.leftArrowClicked)
        self.arrowButtons['RIGHT_ARROW'] = CatalogArrowButton(self, 'RT',
                                                              self.rightArrowClicked)

    def leftArrowClicked(self):
        messenger.send('wakeup')
        if self.currentTab:
            self.currentTab.moveLeft()

    def rightArrowClicked(self):
        messenger.send('wakeup')
        if self.currentTab:
            self.currentTab.moveRight()

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

    def enableBothArrows(self):
        for arrow in self.arrowButtons:
            self.arrowButtons[arrow].show()

    def disableBothArrows(self):
        for arrow in self.arrowButtons:
            self.arrowButtons[arrow].hide()

    def disableLeftArrow(self):
        self.arrowButtons['LEFT_ARROW'].hide()

    def disableRightArrow(self):
        self.arrowButtons['RIGHT_ARROW'].hide()

    def show(self):
        self.accept('CatalogItemPurchaseRequest', self.__handlePurchaseRequest)
        base.setBackgroundColor(Vec4(0.570312, 0.449219, 0.164062, 1.0))
        NodePath.show(self)
        render.hide()

    def hide(self):
        self.ignore('CatalogItemPurchaseRequest')
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        NodePath.hide(self)
        render.show()

    def unload(self):
        self.hide()

        for arrow in self.arrowButtons:
            self.arrowButtons[arrow].cleanup()

        for tab in self.tabButtons:
            self.tabButtons[tab].cleanup()

        for radio in self.radioButtons:
            radio.cleanup()

        self.hangup.destroy()

        self.destroy()

    def destroy(self):
        NodePath.removeNode(self)

    def hangUp(self):
        self.unload()
        print self.doneEvent
        messenger.send(self.doneEvent)

    def __handlePurchaseRequest(self, item):
        item.requestPurchase(self.phone, self.__handlePurchaseResponse)

    def __handlePurchaseResponse(self, retCode, item):
        self.lockItems()

    def lockItems(self):
        for tab in self.tabButtons:
            self.tabButtons[tab].lockItems()

    def updateItems(self):
        for tab in self.tabButtons:
            self.tabButtons[tab].updateItems(self.gifting)
