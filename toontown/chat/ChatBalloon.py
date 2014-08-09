from pandac.PandaModules import *


class ChatBalloon(NodePath):
    TEXT_Y_OFFSET = -0.05
    TEXT_Z_OFFSET = -0.2
    CHAT_BALLOON_X_PADDING = 0.65
    CHAT_BALLOON_Z_PADDING = 0.65
    CHAT_BALLOON_MIN_WIDTH = 3.0
    CHAT_BALLOON_MIN_HEIGHT = 2.6

    def __init__(self, model, modelWidth, modelHeight, chatTextNode,
                 foreground=VBase4(0, 0, 0, 1), background=VBase4(1, 1, 1, 1)):
        NodePath.__init__(self, 'chatBalloon')

        # Set the TextNode color:
        chatTextNode.setTextColor(foreground)

        # Create a chat balloon:
        chatBalloon = model.copyTo(self)
        chatBalloon.setColor(background)
        chatBalloon.setTransparency(background[3] < 1)

        # Attach the TextNode:
        chatText = self.attachNewNode(chatTextNode)
        chatText.setTransparency(foreground[3] < 1)
        chatText.setAttrib(DepthWriteAttrib.make(0))

        # Resize the chat balloon as necessary:
        middle = chatBalloon.find('**/middle')
        top = chatBalloon.find('**/top')
        chatTextWidth = chatTextNode.getWidth()
        chatTextHeight = chatTextNode.getHeight()
        paddedWidth = chatTextWidth + (ChatBalloon.CHAT_BALLOON_X_PADDING*2)
        if paddedWidth < ChatBalloon.CHAT_BALLOON_MIN_WIDTH:
            paddedWidth = ChatBalloon.CHAT_BALLOON_MIN_WIDTH
            chatTextWidth += 0.15
        chatBalloon.setSx(paddedWidth / modelWidth)
        paddedHeight = chatTextHeight + (ChatBalloon.CHAT_BALLOON_Z_PADDING*2)
        if paddedHeight < ChatBalloon.CHAT_BALLOON_MIN_HEIGHT:
            paddedHeight = ChatBalloon.CHAT_BALLOON_MIN_HEIGHT
        middle.setSz(paddedHeight - 1.5)  # Compensate for the top, as well.
        top.setZ(middle, 1)

        # Position the TextNode:
        chatText.setPos(chatBalloon.getBounds().getCenter())
        chatText.setX(chatText, -(chatTextWidth/2))
        chatText.setY(ChatBalloon.TEXT_Y_OFFSET)
        chatText.setZ(top, -ChatBalloon.CHAT_BALLOON_Z_PADDING + ChatBalloon.TEXT_Z_OFFSET)
