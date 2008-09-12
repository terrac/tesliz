
import mental.action as action
from mental.background import *
from tactics.Singleton import *
from tactics.datautil import *
import copy

s = Singleton()

class Mind:
    
    
    def __init__(self):
        self.minds = []
        self.state = "normal"
        self.unitlist= []
    def broadcast(self,item):
        for u in self.minds:
            u.broadcast(item)


    def addMind(self,mind):
        self.minds.append(mind)

class Fighter(Mind):
    def __init__(self):
        Mind.__init__(self)
        self.cfightvalue = 0

        self.bqueue =[]
    def broadcast(self,item):                
       #super(Fighter, self).broadcast(item)
       
       if "arrives" in item and len(self.bqueue) == 0:
           print "arrives"
           eunit = s.unitmap[item.split()[0]] 
           if self.cfightvalue and self.cfightvalue-eunit.value >10:
               return False
           else:
                for unit in self.unitlist:
                    combat = Combat(unit,action.Attack)
                    
                    s.framelistener.addToBackground(self,combat)
                    s.framelistener.clearActions(unit)
                    return
               
