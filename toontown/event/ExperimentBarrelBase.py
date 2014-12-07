class ExperimentBarrelBase:
    GAG_BARREL = 1
    TOONUP_BARREL = 2
    EXPERIENCE_BARREL = 3
    BARREL_TYPES = [GAG_BARREL, TOONUP_BARREL, EXPERIENCE_BARREL]

    def __init__(self):
        self.type = None

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type
