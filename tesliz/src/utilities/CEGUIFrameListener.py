import SampleFramework as sf
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI

def convertButton(oisID):
    if oisID == OIS.MB_Left:
        return CEGUI.LeftButton
    elif oisID == OIS.MB_Right:
        return CEGUI.RightButton
    elif oisID == OIS.MB_Middle:
        return CEGUI.MiddleButton
    else:
        return CEGUI.LeftButton
 
class CEGUIFrameListener(sf.FrameListener, OIS.MouseListener, OIS.KeyListener):
 
    def __init__(self, renderWindow, camera):
       sf.FrameListener.__init__(self, renderWindow, camera, True, True)
       OIS.MouseListener.__init__(self)
       OIS.KeyListener.__init__(self)
       self.cont = True
       self.Mouse.setEventCallback(self)
       self.Keyboard.setEventCallback(self)
 
 
    def frameStarted(self, evt):
        self.Keyboard.capture()
        self.Mouse.capture()
        return self.cont and not self.Keyboard.isKeyDown(OIS.KC_ESCAPE)
 
    def quit(self, evt):
        self.cont = False
        return True
 
    # MouseListener
    def mouseMoved(self, evt):
       CEGUI.System.getSingleton().injectMouseMove(evt.get_state().X.rel, evt.get_state().Y.rel)
       return True
 
    def mousePressed(self, evt, id):
       
       return CEGUI.System.getSingleton().injectMouseButtonDown(convertButton(id))
 
    def mouseReleased(self, evt, id):
       CEGUI.System.getSingleton().injectMouseButtonUp(convertButton(id))
       return True
 
    # KeyListener
    def keyPressed(self, evt):
       ceguiSystem = CEGUI.System.getSingleton()
       ceguiSystem.injectKeyDown(evt.key)
       ceguiSystem.injectChar(evt.text)
       return True
 
    def keyReleased(self, evt):
       CEGUI.System.getSingleton().injectKeyUp(evt.key)
       return True
