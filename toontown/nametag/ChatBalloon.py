from pandac.PandaModules import *


class ChatBalloon(NodePath):
    TEXT_Y_OFFSET = -0.05
    CHAT_BUBBLE_X_PADDING = 0.5
    CHAT_BUBBLE_Z_PADDING = 0.5

    def __init__(self, model, modelWidth, modelHeight, chatTextNode,
                 foreground=VBase4(0, 0, 0, 1), background=VBase4(1, 1, 1, 1)):
        NodePath.__init__(self, 'chatBalloon')

        # Create a chat balloon:
        chatBalloon = model.copyTo(self)
        chatBalloon.setColor(background)
        chatBalloon.setTransparency(background[3] < 1)

        # Set the TextNode color:
        chatTextNode.setTextColor(foreground)

        # Attach the TextNode:
        chatText = self.attachNewNode(chatTextNode)
        chatText.setTransparency(foreground[3] < 1)
        chatText.setAttrib(DepthWriteAttrib.make(0))

        # Resize the chat balloon as necessary:
        middle = chatBalloon.find('**/middle')
        top = chatBalloon.find('**/top')
        chatTextWidth = chatTextNode.getWidth()
        chatTextHeight = chatTextNode.getHeight()
        paddedWidth = chatTextWidth + (ChatBalloon.CHAT_BUBBLE_X_PADDING*2)
        chatBalloon.setSx(paddedWidth / modelWidth)
        paddedHeight = chatTextHeight + (ChatBalloon.CHAT_BUBBLE_Z_PADDING*2)
        middle.setSz(paddedHeight)

        # Position the TextNode:
        chatText.setPos(chatBalloon.getBounds().getCenter())
        chatText.setY(ChatBalloon.TEXT_Y_OFFSET)
        chatText.setX(chatText, -(chatTextWidth/2))

        # Compensate for the top:
        middle.setSz(paddedHeight - 1.25)
        top.setZ(middle, 1)
