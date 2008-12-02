import ogre.renderer.OGRE as ogre
from tactics.Singleton import *

NEXTID = 1

def tempName():
    global NEXTID
    id = NEXTID
    NEXTID += 1
    return 't%d'%id


class OgreText(object):
    """Class for displaying text in Ogre above a Movable."""
    def __init__(self, movable, camera, text=''):
        self.movable = movable
        self.camera = camera
        self.text = ''
        self.enabled = True

        ovm = ogre.OverlayManager.getSingleton()
        self.overlay = ov = ovm.create(tempName())
        self.container = c = ovm.createOverlayElement('Panel', tempName())
        ov.add2D(c)
        self.textArea = t = ovm.createOverlayElement('TextArea', tempName())
        t.setDimensions(1.0, 1.0)
        t.setMetricsMode(ogre.GMM_PIXELS)
        t.setPosition(0, 0)
        t.setParameter('font_name', 'BlueHighway')
        t.setParameter('char_height', '16')
        t.setParameter('horz_align', 'center')
        t.setColour(ogre.ColourValue(1.0, 1.0, 1.0))
        c.addChild(t)
        ov.show()

        self.setText(text)

    def __del__(self):
        self.destroy()

    def destroy(self):
        if hasattr(self, 'dead'): return
        if s.unitmap.has_key(self.movable.getName()) and s.unitmap[self.movable.getName()].text == self:
            s.unitmap[self.movable.getName()].text = None
        
        self.dead = True
        self.overlay.hide()
        ovm = ogre.OverlayManager.getSingleton()
        self.container.removeChild(self.textArea.name)
        self.overlay.remove2D(self.container)
        ovm.destroyOverlayElement(self.textArea.name)
        ovm.destroyOverlayElement(self.container.name)
        ovm.destroy(self.overlay.name)
        if hasattr(s.app.camera,"initialOrientation") and s.app.camera.initialOrientation:
            s.app.camera.setOrientation(s.app.camera.initialOrientation)
        s.app.camera.initialOrientation = None
    

    def enable(self, f):
        self.enabled = f
        if f:
            self.overlay.show()
        else:
            self.overlay.hide()

    def setText(self, text):
        self.text = text
        self.textArea.setCaption(ogre.UTFString(text))

    def update(self):
        if not self.enabled : return

        # get the projection of the object's AABB into screen space
        bbox = self.movable.getWorldBoundingBox(True);
        mat = self.camera.getViewMatrix();
        corners = bbox.getAllCorners();

        min_x, max_x, min_y, max_y = 1.0, 0.0, 1.0, 0.0
        # expand the screen-space bounding-box so that it completely encloses 
        # the object's AABB
        for corner in corners:
            # multiply the AABB corner vertex by the view matrix to 
            # get a camera-space vertex
            corner = mat * corner;
            # make 2D relative/normalized coords from the view-space vertex
            # by dividing out the Z (depth) factor -- this is an approximation
            x = corner.x / corner.z + 0.5
            y = corner.y / corner.z + 0.5

            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y
            
        # we now have relative screen-space coords for the
        # object's bounding box; here we need to center the
        # text above the BB on the top edge. The line that defines
        # this top edge is (min_x, min_y) to (max_x, min_y)

    # self.container.setPosition(min_x, min_y);
        # Edited by alberts: This code works for me
        self.container.setPosition(1-max_x, min_y);
        # 0.1, just "because"
        self.container.setDimensions(max_x - min_x, 0.1);
