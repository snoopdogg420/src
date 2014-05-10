from toontown.achievements import Achievements

class AchievementsManagerAI():
    def __init__(self, air):
        self.air = air
        self.enabled = False
        
        if self.air.wantAchievements:
            self.enabled = True
        
    def toonMadeFriend(self, avId):
        if not self.enabled:
            return
        
        av = self.air.doId2do.get(avId)
        if not av:
            return
        
        possibleAchievements = Achievements.getAchievementsOfType(Achievements.FriendAchievement)
        
        for achievementId in possibleAchievements:
            if not achievementId in av.getAchievements():
                if Achievements.AchievementsDict[achievementId].hasComplete(av):
                    av.addAchievement(achievementId)
                    
    def toonPlayedMinigame(self, av):
        if not self.enabled:
            return
        
        possibleAchievements = Achievements.getAchievementsOfType(Achievements.TrolleyAchievement)
        
        for achievementId in possibleAchievements:
            if not achievementId in av.getAchievements():
                if Achievements.AchievementsDict[achievementId].hasComplete(av):
                    av.addAchievement(achievementId)
                    
    def toonGotQuest(self, avId):
        if not self.enabled:
            return
        
        av = self.air.doId2do.get(avId)
        if not av:
            return