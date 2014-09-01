from pandac.PandaModules import *
from toontown.nametag import NametagGlobals
from toontown.nametag.NametagFloat3d import NametagFloat3d


class NametagFloat2d(NametagFloat3d):
    def doBillboardEffect(self):
        pass

    def update(self):
        NametagFloat3d.update(self)

        if self.active or (self.getChatText() and (self.getChatButton() != NametagGlobals.noButton)):
            self.updateClickRegion()
        else:
            self.region.setActive(False)

    def setClickRegion(self, left, right, bottom, top):
        # Get a transform matrix to position the points correctly according to
        # the nametag node:
        transform = self.contents.getNetTransform()

        # Get the actual matrix of the transform above:
        mat = transform.getMat()

        # Transform the specified points to the new matrix:
        camSpaceTopLeft = mat.xformPoint(Point3(left, 0, top))
        camSpaceBottomRight = mat.xformPoint(Point3(right, 0, bottom))

        screenSpaceTopLeft = Point2(camSpaceTopLeft[0], camSpaceTopLeft[2])
        screenSpaceBottomRight = Point2(camSpaceBottomRight[0], camSpaceBottomRight[2])

        left, top = screenSpaceTopLeft
        right, bottom = screenSpaceBottomRight

        self.region.setFrame(left, right, bottom, top)
        self.region.setActive(True)
