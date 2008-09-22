
import mental.action as action
from mental.background import *
from tactics.Singleton import *
from tactics.datautil import *
import copy

s = Singleton()

class Mind:

    
        
    state = {"angry":0, "happy":0}
    map = None
#    def __init__(self,minds = []):
#        self.minds = minds
#    
#        
#    
#
#    def broadcast(self,item,unit = None):
#        if unit:
#            s.chatbox.add(unit.getName()+": "+item)
#        else:
#            s.chatbox.add(item)
#            
#        for u in self.minds:
#            u.broadcast(item,unit)
#    def addMind(self,mind):
#        self.minds.append(mind)
#        
    def getMentalCommands(self):
        
        list = []
        for x in self.map.values():
            y = x.getMentalCommands()
            if y:
                list = list + y
        return list

class Fighter(Mind):
#    def __init__(self):
#        Mind.__init__(self)
        
        
     
    def broadcast(self, item, unit):                
       #super(Fighter, self).broadcast(item)
       
       combat = unit.mental.map["combat"]           
       if "arrives" in item and len(combat.bqueue) == 0:
           s.log("arrives", self)
           eunit = s.unitmap[item.split()[0]]

           combat.setup(unit, eunit) 
                      
