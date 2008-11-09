from tactics.Singleton import *
import utilities.OgreText 
 

class Chatbox:
    listholder = []
    def add(self,text,unit ):        
        item =CEGUI.ListboxTextItem (text+":"+unit.getName())        
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listholder.append(item)
        
        self.list.addItem(item)
        ogretext = utilities.OgreText.OgreText(unit.node.getAttachedObject(0),s.app.camera,text)
        ogretext.enable(True)
        unit.text =ogretext
        ori = s.app.camera.getOrientation()
        if not s.app.camera.initialOrientation:
            s.app.camera.initialOrientation = ori
        if s.eventpausing:
            s.app.camera.lookAt(unit.node.getPosition())        
            s.framelistener.paused = True
        
                 
    def __init__(self):
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        self.list = winMgr.createWindow("TaharezLook/Listbox", "chatbox")
        sheet.addChildWindow(self.list)
        self.list.setText("actionlist")
        self.list.setPosition(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.7)))
        self.list.setSize(CEGUI.UVector2(cegui_reldim(0.4), cegui_reldim( 0.2)))                
        self.list.setAlwaysOnTop(True)