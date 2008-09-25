
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
            try:
                y = x.getMentalCommands()
                if y:
                    list = list + y
            except:
                pass
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
                      
class RunPlayer:
    #only brodcasts to same player and only if that unit is talking
    def __init__(self,name):
        self.name = name
    
    
    def broadcast(self,text,unit):
        #if self.unit == unit:
        for x in unit.player.unitlist:                
            try:
                x.mental.map[self.name].broadcast(text,unit)
            except Exception, e:
                print str(e)+str(x)+str(x.mental.map)
class KnowledgeBase:
    def __init__(self):
        self.map = dict()
    def addKnowledge(self,text,base,place = "General"):   
        if not self.map.has_key(place):
            self.map[place] = dict()
        if not self.map[place].has_key(base):
            self.map[place][base] = []     
        self.map[place][base].append(text)
    def getKnowledge(self,base,place = "General"):
        return self.map[place][base]
    def getKnowledgeList(self,base,place = ["General"]):
        for x in place:
            if self.map.has_key(x):
                return self.map[x][base]
    