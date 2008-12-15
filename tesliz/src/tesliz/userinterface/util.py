import ogre.gui.CEGUI as CEGUI

def getNewWindow( name,type = "TaharezLook/Listbox",winname = None):

    winMgr = CEGUI.WindowManager.getSingleton()
    
    if winMgr.isWindowPresent(name):
        CEGUI.WindowManager.getSingleton().destroyWindow(name)

    
    list = winMgr.createWindow(type, name)
    if winname:
        sheet = CEGUI.WindowManager.getSingleton().getWindow( winname  )
        sheet.addChildWindow(list)
    
    return list
def addItem(curclass,list,name):        
    item =CEGUI.ListboxTextItem (name)        
    item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system
    if not hasattr(curclass, "listholder") or not curclass.listholder:
         curclass.listholder = []
    curclass.listholder.append(item)
    item.setSelectionBrushImage("TaharezLook", "MultiListSelectionBrush")
    list.addItem(item)
def destroyWindow(text):
    winMgr = CEGUI.WindowManager.getSingleton()
    winMgr.destroyWindow(text)
    