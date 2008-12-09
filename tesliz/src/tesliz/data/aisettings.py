from mental.mind import *
from mental.timer import *
#from mental.mi
from mental.grammar import *
from tactics.Singleton import *
import utilities.OgreText
from tactics.chatbox import * 
 
s = Singleton()


class AIsettings:
    def __init__(self):
        s.chatbox = Chatbox()
        fighter = Fighter()       
        s.grammar = Grammar()
        #s.grammar.addLine("is weak to", fighter)
        #s.grammar.addLine("arrives", fighter)
        s.grammar.addLine("leaves", fighter)
        
        follower = Run("follower",Run.Player)
        s.grammar.addLine("follow me", follower)
        
        
        convo = Run("conversation",Run.Self)
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
        s.knowledge.addKnowledge("The robots took my job","battlecry","revolution")
        s.knowledge.addKnowledge("My son has died in your war!","battlecry","revolution")
        s.knowledge.addKnowledge("Waaaaaaaaaaaaaaaaaaarrrr","battlecry","bloodthirsty")
        s.knowledge.addKnowledge("Your bones will decorate my living room","battlecry","bloodthirsty")
        s.knowledge.addKnowledge("You liberal scum die","battlecry","nobility")
        s.knowledge.addKnowledge("Protect the homeland","battlecry","nobility")
        
        s.knowledge.addTree("nobility","lina")
        #s.knowledge.addKnowledge("I have been waiting for this","waiting")
        execlist = ExecuteList([BroadcastM("I have been waiting for this","myside"),BroadcastM("your spouse is in danger","self")])
        s.knowledge.addKnowledge(execlist,"revolution","lina")
        
 
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
        