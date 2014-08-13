from pandac.PandaModules import *


class ChatBalloon(NodePath):
    TEXT_X_OFFSET = -0.05
    TEXT_Y_OFFSET = -0.05
    TEXT_Z_OFFSET = -(4.0/33.0)

    TEXT_MIN_WIDTH = 2.25
    TEXT_MIN_HEIGHT = 1.5

    TEXT_GLYPH_SCALE = 1.05
    TEXT_GLYPH_SHIFT = -0.05

    CHAT_BALLOON_X_PADDING = 0.65
    CHAT_BALLOON_Z_PADDING = 0.65

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
        if chatTextWidth < ChatBalloon.TEXT_MIN_WIDTH:
            chatTextWidth = ChatBalloon.TEXT_MIN_WIDTH
        chatTextHeight = chatTextNode.getHeight()
        if chatTextHeight < ChatBalloon.TEXT_MIN_HEIGHT:
            chatTextHeight = ChatBalloon.TEXT_MIN_HEIGHT
        paddedWidth = chatTextWidth + (ChatBalloon.CHAT_BALLOON_X_PADDING*2)
        chatBalloon.setSx(paddedWidth / modelWidth)
        paddedHeight = chatTextHeight + (ChatBalloon.CHAT_BALLOON_Z_PADDING*2)
        middle.setSz(paddedHeight - 1.5)  # Compensate for the top, as well.
        top.setZ(middle, 1)

        # Position the TextNode:
        chatText.setPos(chatBalloon.getBounds().getCenter())
        chatText.setX(chatText, -(chatTextWidth/2))
        if chatTextWidth == ChatBalloon.TEXT_MIN_WIDTH:
            chatText.setX(chatText, (ChatBalloon.TEXT_MIN_WIDTH-chatTextNode.getWidth()) / 2.0)
        chatText.setY(ChatBalloon.TEXT_Y_OFFSET)
        chatText.setZ(top, -ChatBalloon.CHAT_BALLOON_Z_PADDING + ChatBalloon.TEXT_Z_OFFSET)
        if chatTextHeight == ChatBalloon.TEXT_MIN_HEIGHT:
            chatText.setZ(chatText, -((ChatBalloon.TEXT_MIN_HEIGHT-chatTextNode.getHeight()) / 2.0))
        chatText.setX(chatText, ChatBalloon.TEXT_X_OFFSET)
