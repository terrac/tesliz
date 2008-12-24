from tactics.Singleton import *
import utilities.OgreText 
 

class Chatbox:
    listholder = []
    def add(self,text,unit ,time):
        
        
        self.addText(unit.getName())
        self.addText(text)
        
        text =wrap(text, 40)
        
        otext = unit.getName()+"\n"+text
                
        try:
            ogretext = utilities.OgreText.OgreText(unit.node.getAttachedObject(0),otext)
        except:# we shouldn't be adding text if the unit is gone
            return
        ogretext.enable(True)
        unit.setText(ogretext)
        ori = s.app.camera.getOrientation()
        if not s.app.camera.initialOrientation:
            s.app.camera.initialOrientation = ori
        s.framelistener.addTimed(time,ogretext)
#        if s.eventpausing:
#            s.app.camera.lookAt(unit.node.getPosition())        
#            s.framelistener.paused = True
        
                 
    def __init__(self):
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        name ="chatbox" 
        if winMgr.isWindowPresent(name):            
            chatbox = winMgr.getWindow(name)
        else:
            chatbox = winMgr.createWindow("TaharezLook/Listbox", name)
        sheet.addChildWindow(chatbox)
        chatbox.setText("actionlist")
        chatbox.setPosition(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.7)))
        chatbox.setSize(CEGUI.UVector2(cegui_reldim(0.4), cegui_reldim( 0.2)))                
        #chatbox.setAlwaysOnTop(True)
        self.chatbox = chatbox

    def addText(self, text):
        item = CEGUI.ListboxTextItem(text)
        item.AutoDeleted = False # Fix to ensure that items are not deleted by the CEGUI system
        self.listholder.append(item)
        self.chatbox.addItem(item)
        self.chatbox.ensureItemIsVisible(item)

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )
