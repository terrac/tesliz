
import mental.action as action
from mental.background import *
from tactics.Singleton import *
from tactics.datautil import *
import copy

s = Singleton()

class Mind:

    
        
    state = {"angry":0,"happy":0}
    def __init__(self,minds = []):
        self.minds = minds
    
        
    def broadcast(self,item):
        for u in self.minds:
            u.broadcast(item)

    def broadcast(self,item,unit):
        s.chatbox.add(unit.getName()+": "+item)
        self.broadcast(item)
    def addMind(self,mind):
        self.minds.append(mind)
        
    def getMentalCommands(self):
        list = []
        for x in self.minds:
            list =list +x.getMentalCommands()
        return list

class Fighter(Mind):
    def __init__(self,unit):
        Mind.__init__(self)
        self.cfightvalue = 0
        self.unit = unit
        self.bqueue =[]
    def broadcast(self,item):                
       #super(Fighter, self).broadcast(item)
       
       if "arrives" in item and len(self.bqueue) == 0:
           print "arrives"
           eunit = s.unitmap[item.split()[0]] 
           if self.cfightvalue and self.cfightvalue-eunit.value >10:
               return False
           else:
                unit = self.unit
                combat = Combat(unit,action.Attack)
                
                s.framelistener.addToBackground(self,combat)
                s.framelistener.clearActions(unit)
                return
           
