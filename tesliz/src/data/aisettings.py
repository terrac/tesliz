from mental.mind import *
#from mental.mi
from mental.grammar import *
from tactics.Singleton import *
 
s = Singleton()

class Mental:
    def __init__(self):             
        fighter = Fighter()
        fighter.unitlist.append(s.unitmap["lina"])
        s.mental =grammar= Grammar()
        grammar.addLine("is weak to", fighter)
        grammar.addLine("arrives", fighter)
        grammar.addLine("leaves", fighter)
        
        