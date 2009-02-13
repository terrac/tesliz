import ogre.gui.CEGUI as CEGUI
from tactics.Singleton import *
rootwindow = "root_wnd"

listbox = "TaharezLook/Listbox"
combobox = "TaharezLook/Combobox"
frame = "TaharezLook/FrameWindow"
button = "TaharezLook/Button"
editbox = "TaharezLook/Editbox"
statictext = "TaharezLook/StaticText"
multieditbox = "TaharezLook/MultiLineEditbox"

def getNewWindow( name,type = "TaharezLook/Listbox",winname = None,posx = None,posy = None,sizex = None,sizey= None, text = None):

    winMgr = CEGUI.WindowManager.getSingleton()
    
    if winMgr.isWindowPresent(name):
        CEGUI.WindowManager.getSingleton().destroyWindow(name)

    
    list = winMgr.createWindow(type, name)
    if winname:
        if isinstance(winname, str):            
            sheet = CEGUI.WindowManager.getSingleton().getWindow( winname  )
        else:
            sheet = winname
        sheet.addChildWindow(list)
    if not posx is None:
        list.setPosition(CEGUI.UVector2(cegui_reldim(posx), cegui_reldim(posy)))
    if not sizex is None:
        list.setSize(CEGUI.UVector2(cegui_reldim(sizex), cegui_reldim( sizey)))
    setLayoutCallbacks(list)
    if text:
        list.setText(text)
    return list

def setLayoutCallbacks(window):
    window.subscribeEvent(CEGUI.Window.EventMouseClick, s.cegui, "clicked")
    if isinstance(window, CEGUI.FrameWindow):
        window.subscribeEvent(CEGUI.FrameWindow.EventCloseClicked,s.cegui,"closeClicked")
def recursiveSet(window,function):
    print window.getName()
    function(window)
    for x in range(0,window.getChildCount()):
        child = window.getChildAtIdx(x)
        recursiveSet(child,function)
def addItem(selfc,list,name,index = None):        
    item =CEGUI.ListboxTextItem (name)        
    item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system
    if not hasattr(selfc, "listholder") or not selfc.listholder:
         selfc.listholder = []
    selfc.listholder.append(item)
    item.setSelectionBrushImage("TaharezLook", "MultiListSelectionBrush")
    if index is None:
        list.addItem(item)
    else:
        list.insertItem(item,list.getListboxItemFromIndex(index))
    return item
    
def destroyWindow(text):
    winMgr = CEGUI.WindowManager.getSingleton()
    winMgr.destroyWindow(text)
