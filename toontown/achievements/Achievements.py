ANY_LAFF=138

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
    
class VPAchievement():
    
    def __init__(self, neededLaff=ANY_LAFF, solo=False):
        self.neededLaff = neededLaff
        self.solo = solo
    
    def hasComplete(self, laff, solo):
        complete = 1
        
        if self.neededLaff != ANY_LAFF:
            if laff:
                complete = 1
            else:
                complete = 0
                
        if self.solo:
            if solo:
                complete = 1
            else:
                complete = 0
            
        return complete
    
def getAchievementsOfType(type):
    return type2AchievementIds.get(type)

AchievementsDict = (FriendAchievement(),
                    FriendAchievement(neededFriends=10),
                    FriendAchievement(neededFriends=50),
                    TrolleyAchievement(),
                    VPAchievement(),
                    VPAchievement(neededLaff=1),
                    VPAchievement(solo=True),
                    VPAchievement(neededLaff=1, solo=True))
type2AchievementIds = {FriendAchievement: [0, 1, 2],
                       TrolleyAchievement: [3],
                       VPAchievement: [4, 5, 6, 7]}