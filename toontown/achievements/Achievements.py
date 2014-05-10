class FriendAchievement():
    
    def __init__(self, neededFriends=1):
        self.neededFriends = neededFriends
    
    def hasComplete(self, av):
        avatarsFriends = av.getFriendsList()
        
        if len(avatarsFriends) >= self.neededFriends:
            return 1
        
        return 0
    
class TrolleyAchievement():
    def hasComplete(self, av):
        return 1

class SuitsAchievement():
    
    def __init__(self, neededSuits=1):
        self.neededSuits = neededSuits
        
    def hasComplete(self, av):
        avatarsRadar = av.getCogCount()
        
        return 0
    
def getAchievementsOfType(type):
    return type2AchievementIds.get(type)

AchievementsDict = (FriendAchievement(),
                    FriendAchievement(neededFriends=10),
                    FriendAchievement(neededFriends=50),
                    TrolleyAchievement())
type2AchievementIds = {FriendAchievement: [0, 1, 2],
                       TrolleyAchievement: [3]}