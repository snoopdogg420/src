from pandac.PandaModules import *


class ChatBalloon(NodePath):
    TEXT_X_OFFSET = -0.05
    TEXT_Y_OFFSET = -0.05

    # Proportion of the Z offset based on the default line height, and the new
    # line height:
    TEXT_Z_OFFSET = -(4.0/33.0)

    TEXT_MIN_WIDTH = 1.75
    TEXT_MIN_HEIGHT = 1.0

    TEXT_GLYPH_SCALE = 1.05
    TEXT_GLYPH_SHIFT = -0.05

    CHAT_BALLOON_X_PADDING = 0.65
    CHAT_BALLOON_Z_PADDING = 0.65

    BUTTON_SCALE = 6
    BUTTON_SHIFT = (-0.2, 0, 0.6)

    def __init__(self, model, modelWidth, modelHeight, textNode,
                 foreground=VBase4(0, 0, 0, 1), background=VBase4(1, 1, 1, 1),
                 button=None):
        NodePath.__init__(self, 'chatBalloon')

        self.model = model
        self.modelWidth = modelWidth
        self.modelHeight = modelHeight
        self.textNode = textNode
        self.foreground = foreground
        self.background = background

        # Set the TextNode color:
        self.textNode.setTextColor(foreground)

        # Create a chat balloon:
        self.balloon = model.copyTo(self)
        self.balloon.setColor(background)
        self.balloon.setTransparency(background[3] < 1)

        # Attach the TextNode:
        self.textNodePath = self.attachNewNode(self.textNode)
        self.textNodePath.setTransparency(foreground[3] < 1)
        self.textNodePath.setAttrib(DepthWriteAttrib.make(0))

        # Resize the chat balloon as necessary:
        middle = self.balloon.find('**/middle')
        top = self.balloon.find('**/top')
        textWidth = self.textNode.getWidth()
        if textWidth < ChatBalloon.TEXT_MIN_WIDTH:
            textWidth = ChatBalloon.TEXT_MIN_WIDTH
        paddedWidth = textWidth + (ChatBalloon.CHAT_BALLOON_X_PADDING*2)
        self.balloon.setSx(paddedWidth / modelWidth)
        textHeight = textNode.getHeight()
        if textHeight < ChatBalloon.TEXT_MIN_HEIGHT:
            textHeight = ChatBalloon.TEXT_MIN_HEIGHT
        paddedHeight = textHeight + (ChatBalloon.CHAT_BALLOON_Z_PADDING*2)
        middle.setSz(paddedHeight - 1.5)  # Compensate for the top, as well.
        top.setZ(middle, 1)

        # Position the TextNode:
        self.textNodePath.setPos(self.balloon.getBounds().getCenter())
        self.textNodePath.setY(ChatBalloon.TEXT_Y_OFFSET)
        self.textNodePath.setX(self.textNodePath, -(textWidth/2))
        if textWidth == ChatBalloon.TEXT_MIN_WIDTH:
            centerX = (ChatBalloon.TEXT_MIN_WIDTH-self.textNode.getWidth()) / 2
            self.textNodePath.setX(self.textNodePath, centerX)
        self.textNodePath.setZ(top, -ChatBalloon.CHAT_BALLOON_Z_PADDING + ChatBalloon.TEXT_Z_OFFSET)
        if textHeight == ChatBalloon.TEXT_MIN_HEIGHT:
            centerZ = (ChatBalloon.TEXT_MIN_HEIGHT-self.textNode.getHeight()) / 2
            self.textNodePath.setZ(self.textNodePath, -centerZ)
        self.textNodePath.setX(self.textNodePath, ChatBalloon.TEXT_X_OFFSET)

        # Add a button if one is given:
        if button is not None:
            buttonNodePath = button.copyTo(self)
            buttonNodePath.setPos(self.textNodePath, textWidth, 0, -textHeight)
            buttonNodePath.setPos(buttonNodePath, ChatBalloon.BUTTON_SHIFT)
            buttonNodePath.setScale(ChatBalloon.BUTTON_SCALE)

    def setForeground(self, foreground):
        self.foreground = foreground
        self.textNode.setTextColor(self.foreground)
        self.textNodePath.setTransparency(self.foreground[3] < 1)

    def getForeground(self):
        return self.foreground

    def setBackground(self, background):
        self.background = background
        self.balloon.setColor(self.background)
        self.balloon.setTransparency(self.background[3] < 1)

    def getBackground(self):
        return self.background
