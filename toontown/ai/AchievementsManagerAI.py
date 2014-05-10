from toontown.achievements import Achievements

class AchievementsManagerAI():
    def __init__(self, air):
        self.air = air
        
    def toonMadeFriend(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        
        possibleAchievements = Achievements.getAchievementsOfType(Achievements.FriendAchievement)
        
        for achievementId in possibleAchievements:
            if not achievementId in av.getAchievements():
                if Achievements.AchievementsDict[achievementId].hasComplete(av):
                    av.addAchievement(achievementId)
                    
    def toonPlayedMinigame(self, av):
        possibleAchievements = Achievements.getAchievementsOfType(Achievements.TrolleyAchievement)
        
        for achievementId in possibleAchievements:
            if not achievementId in av.getAchievements():
                if Achievements.AchievementsDict[achievementId].hasComplete(av):
                    av.addAchievement(achievementId)
                    
    def toonGotQuest(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return