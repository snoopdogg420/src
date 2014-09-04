class DNABattleCell:
    COMPONENT_CODE = 21

    def __init__(self, width, height, pos):
        self.width = width
        self.height = height
        self.pos = pos

    def setWidth(self, width):
        self.width = width

    def getWidth(self):
        return self.width

    def setHeight(self, height):
        self.height = height

    def getHeight(self):
        return self.height

    def setPos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def __str__(self):
        return 'DNABattleCell width: %s height: %s pos: %s' % (self.width, self.height, self.pos)
