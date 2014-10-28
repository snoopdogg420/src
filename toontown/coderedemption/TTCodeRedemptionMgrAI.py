from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.catalog import CatalogItem, CatalogPoleItem, CatalogBeanItem, CatalogChatItem, CatalogAccessoryItem
from toontown.toonbase import ToontownGlobals

import time

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTCodeRedemptionMgrAI")
    
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def giveAwardToToonResult(self, todo0, todo1):
        pass

    def redeemCode(self, context, code):
        avId = self.air.getAvatarIdFromSender()
        if (code == "Beans"):
            self.requestCodeRedeem(context, CatalogBeanItem.CatalogBeanItem(15000, tagCode = 2).getBlob())
        elif (code == "NewRod"):
            self.requestCodeRedeem(context, CatalogPoleItem.CatalogPoleItem(1).getBlob())
        elif (code == "NewPhraseChat"):
            self.requestCodeRedeem(context, CatalogChatItem.CatalogChatItem(4130).getBlob())
        elif (code == "KevinsHat"):
            self.requestCodeRedeem(context, CatalogAccessoryItem.CatalogAccessoryItem(176).getBlob())
        else:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 1, 0])
        
    def requestCodeRedeem(self, context, item):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        item = CatalogItem.getItem(item)
        if item.getDeliveryTime():
            if len(av.onOrder) > 5:
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 4])
                return
            if len(av.mailboxContents) + len(av.onOrder) >= ToontownGlobals.MaxMailboxContents:
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 3])
                return
            if (item in av.onOrder):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 13])
                return
            if (item.reachedPurchaseLimit(av)):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 13])
                return
            item.deliveryDate = int(time.time()/60) + 0.01
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 0, 0])
        else:
            if len(av.onOrder) > 5:
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 4])
                return
            if len(av.mailboxContents) + len(av.onOrder) >= ToontownGlobals.MaxMailboxContents:
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 3])
                return
            if (item in av.onOrder):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 13])
                return
            if (item.reachedPurchaseLimit(av)):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 4, 13])
                return
            item.deliveryDate = int(time.time()/60) + 0.01
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, 0, 0])

    def redeemCodeResult(self, todo0, todo1, todo2):
        pass

