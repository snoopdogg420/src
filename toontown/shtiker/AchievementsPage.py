import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer

class AchievementsPage(ShtikerPage.ShtikerPage):
    
    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.avatar = None
        
    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.AchievementsPageTitle, text_scale=0.12, textMayChange=1, pos=(0, 0, 0.62))
        
    def setAvatar(self, av):
        self.avatar = av