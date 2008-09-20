from mental.mind import *
from mental.timer import *
#from mental.mi
from mental.grammar import *
from tactics.Singleton import *
 
s = Singleton()

class Chatbox:
    def add(self,list,name):        
        item =CEGUI.ListboxTextItem (name)        
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listholder.append(item)
        list.addItem(item)         
    def __init__(self):
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        list = winMgr.createWindow("TaharezLook/Listbox", "chatbox")
        sheet.addChildWindow(list)
        list.setText("actionlist")
        list.setPosition(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.7)))
        list.setSize(CEGUI.UVector2(cegui_reldim(0.4), cegui_reldim( 0.2)))                
        list.setAlwaysOnTop(True)
class Mental:
    def __init__(self):
        s.chatbox = Chatbox()
        
   
    listholder = []
    
    
        #fighter = Fighter()
#        fighter.unitlist.append(s.unitmap["lina"])
#        grammar= Grammar()
#        timer = Timer()
#        s.mental = Mind()
#        s.mental.minds = [timer,grammar]
#        grammar.addLine("is weak to", fighter)
#        grammar.addLine("arrives", fighter)
#        grammar.addLine("leaves", fighter)

        #                angry/calm happy/sad
#        s.mental.state = {"angry":0,"happy":0}
        