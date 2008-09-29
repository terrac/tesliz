from mental.mind import *
from mental.timer import *
#from mental.mi
from mental.grammar import *
from tactics.Singleton import *
 
s = Singleton()

class Chatbox:
    listholder = []
    def add(self,text,unit):        
        item =CEGUI.ListboxTextItem (text+":"+unit.getName())        
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listholder.append(item)
        
        self.list.addItem(item)         
    def __init__(self):
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        self.list = winMgr.createWindow("TaharezLook/Listbox", "chatbox")
        sheet.addChildWindow(self.list)
        self.list.setText("actionlist")
        self.list.setPosition(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.7)))
        self.list.setSize(CEGUI.UVector2(cegui_reldim(0.4), cegui_reldim( 0.2)))                
        self.list.setAlwaysOnTop(True)
class AIsettings:
    def __init__(self):
        s.chatbox = Chatbox()
        fighter = Fighter()       
        s.grammar = Grammar()
        #s.grammar.addLine("is weak to", fighter)
        #s.grammar.addLine("arrives", fighter)
        s.grammar.addLine("leaves", fighter)
        
        follower = RunPlayer("follower")
        s.grammar.addLine("follow me", follower)
        
        
        convo = RunAll("conversation")
        s.grammar.addLine("has occurred", convo)
        
        s.knowledge = KnowledgeBase()
        
        s.knowledge.addTree("general","environment")
        s.knowledge.addTree("general", "people")
        s.knowledge.addTree("people", "bloodthirsty")
        
        s.knowledge.addTree("general", "words")
        s.knowledge.addTree("environment","revolution")
        s.knowledge.addTree("environment","nobility")                
        
        s.knowledge.addKnowledge("Your mother is a hamster","battlecry")
        s.knowledge.addKnowledge("For the revolution!","battlecry","revolution")
        s.knowledge.addKnowledge("Down with the nobility!","battlecry","revolution")
        s.knowledge.addKnowledge("Kill your landlord!","battlecry","revolution")
        s.knowledge.addKnowledge("My son has died in your war!","battlecry","revolution")
        s.knowledge.addKnowledge("Waaaaaaaaaaaaaaaaaaarrrr","battlecry","bloodthirsty")
        s.knowledge.addKnowledge("Your bones will decorate my living room","battlecry","bloodthirsty")
        s.knowledge.addKnowledge("You liberal scum die","battlecry","nobility")
        s.knowledge.addKnowledge("Protect the homeland","battlecry","nobility")
        
        s.knowledge.addTree("nobility","lina")
        s.knowledge.addKnowledge("","waiting")
        s.knowledge.addKnowledge("waiting","revolution","lina")
        s.knowledge.printMap()
#    def broadcast(self,text,name = None):
        
    
    
 
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
        