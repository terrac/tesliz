import ogre.gui.CEGUI as CEGUI
from tactics.Singleton import *

class CEGUIManager:
    def __init__(self):
        s.cegui = self
        self.winMgr = CEGUI.WindowManager.getSingleton()
        
    def hide(self):
        win =self.winMgr.getWindow("root_wnd")
        for x in range(0,win.ChildCount):
            win.getChildAtIdx(x).setVisible(False)
            #print name
            #win.removeChildWindow(name)
    
    
    def show(self):
        win =self.winMgr.getWindow("root_wnd")
        for x in range(0,win.ChildCount):
            win.getChildAtIdx(x).setVisible(True)
    def getStaticImage(self,name,resourceloc):
        ceguiTexture =CEGUI.System.getSingleton().getRenderer().createTexture(name,resourceloc)
        imageSet = CEGUI.ImagesetManager.getSingleton().createImageset(name+"image", ceguiTexture)
        imageSet.defineImage("RttImage", CEGUI.Rect(0.0, 0.0, ceguiTexture.getWidth(), ceguiTexture.getHeight()), CEGUI.Vector2(0.0, 0.0))
        
        staticImg = s.cegui.winMgr.createWindow("TaharezLook/StaticImage", name+"imageset")
        

        staticImg.setProperty("Image", CEGUI.PropertyHelper.imageToString(imageSet.getImage("RttImage")))
        return staticImg
    def clicked(self,e):
        #We don't want to click through the cegui
        return True