
import mental.action as action
from mental.background import *
from tactics.Singleton import *
from tactics.datautil import *
import copy

s = Singleton()

class Mind:

    
        
    state = {"angry":0, "happy":0}
    
    def __init__(self,list = None,map = None):
        self.map = map
        self.list = list
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
        if self.map:
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
                      
class Run:
    #only brodcasts to same player and only if that unit is talking
    def __init__(self,name, list2 = None):
        self.name = name
        if isinstance(list2,list):
            self.list2 = list2
        else:
            self.getList = list2
    
    def getList(self,unitbroadcastto,unitbroadcasting):
        return self.list
    def Player(self,unitbroadcastto,unitbroadcasting):
        return unitbroadcasting.player.unitlist
    def Self(self,unitbroadcastto,unitbroadcasting):
        return [unitbroadcastto]
    def All(self,unitbroadcastto,unitbroadcasting):
        return s.unitmap.values()
    def broadcast(self, text,unitbroadcastto, unitbroadcasting):
        #if self.unit == unit:
        for x in self.getList(self,unitbroadcastto,unitbroadcasting):                
            try:
                x.mental.map[self.name].broadcast(text, unitbroadcastto,unitbroadcasting)
            except Exception, e:
                print str(e) + str(x) + str(x.mental.map)



                
class Tree:
    def __init__(self, value, type = 0):
        self.map = dict() 
        self.value = value
        self.type = type
    def __len__(self):
        return self.map.__len__() +1

    def has_key(self,a):
        return self.map.has_key(a)
    def __getitem__(self, key):
        return self.map.__getitem__(key)
    
    def __setitem__(self, key, value):
        self.map.__setitem__( key, value)
    
    def __delitem__(self, key):        
        self.map.__delitem__(key)
    
    def __iter__(self):
        return self.map.__iter__()
    def __str__( self ):
        return str(self.value) +" "+str(self.map.__str__())
    def values(self):
        return self.map.values()   
    def keys(self):
        return self.map.keys()
    def add(self, string):
        x = Tree(string)
        self.map[string] =x        
        return x     
#class KnowledgeBase:
#    def __init__(self):
#        self.map = dict()
#    def addKnowledge(self, text, base, place="General"):   
#        if not self.map.has_key(place):
#            self.map[place] = Tree(place)
#        if not self.map[place].has_key(base):
#            self.map[place][base] = Tree(base)     
#        self.map[place][base] = Tree(text)
#    def getKnowledge(self, base, place="General"):
#        return self.map[place][base].value
#    def getKnowledgeList(self, base, place=["General"]):
#        for x in place:
#            if self.map.has_key(x):               
#                return self.map[x][base]
#    def getRandomFromKnowledgeList(self, base, place=["General"]):
#        map = self.getKnowledgeList(base, place)
#        if len(map) == 0:
#            return map.value
#        return map[random.randrange(0,len(map))].value
# 
   
#1 = parent
#0 = leaf
class KnowledgeBase:
    def __init__(self):
        self.map = Tree("general",1)

    def getTypeMap(self, place, baselist):
        
        for base in baselist:            
            map = self.getParent(base, self.map)

            map = self.getParent(place, map)
            if map:
                break    
        return map

        
    def addTree(self,parent,child):
        p = self.getParent(parent,self.map)
        if not p:
            blah
        p[child]= Tree(child,1)
        
    
    #def getParent(self,parent):
        #return self.getParent(parent,self.map)
        
    def getParent(self,parent,map):
        if not map:
            return
        if map.value==parent and map.type == 1:
            return map
        else:
            for x in map.values():
                y =self.getParent(parent, x)
                if y != None:
                    return y    
    def addKnowledge(self, text, parent,place="general"):
        bmap = self.getParent(place,self.map)
        pmap = self.getParent(parent,bmap)
        if not bmap:
            print place
        if not pmap:
            pmap = Tree(parent,1)
            bmap[parent] = pmap
        
            #return False
             
        pmap[text] = Tree(text,0)
#    def getKnowledge(self, base, parent="general"):
#        return self.map[place][base].value
#    def getKnowledgeList(self, base, place=["general"]):
#        for x in place:
#            if self.map.has_key(x):               
#                return self.map[x][base]
    def getRandomFromParent(self, place,base):
        map = self.getTypeMap(place, base)
        
        if len(map) == 1:
            return map.value
        return map.values()[random.randrange(0,len(map.values()))].value
    def printMap(self, map = None):
        if not map:
            map = self.map
        print map
        for x in map.values():
            self.printMap(x)

