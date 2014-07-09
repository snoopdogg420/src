class HolidayManagerAI:
    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
        self.xpMultiplier = 1

    def isHolidayRunning(self, *args):
        return True
        #TODO: this function needs to actually check holidays

    def isMoreXpHolidayRunning(self):
        return False

    def getXpMultiplier(self):
        return self.xpMultiplier