class HolidayManagerAI:
    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
        self.xpMultiplier = 1

    def isHolidayRunning(self, holidayId):
        if holidayId in self.currentHolidays:
            return True

    def isMoreXpHolidayRunning(self):
        return False

    def getXpMultiplier(self):
        return self.xpMultiplier