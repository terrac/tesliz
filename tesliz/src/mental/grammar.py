import copy
from tactics.Singleton import *


s = Singleton()


class Grammar:
    def __init__(self):
        
        self.startMap = dict()
        self.endMap = dict()
        
    def broadcast(self,text,unit,broadcastto= "all"):
        if broadcastto == "all":
            unitlist = s.unitmap.values()
        elif broadcastto == "self":
            unitlist = [unit]
        else :
            unitlist = unit.player.unitlist
        list = text.split()
        slist = set()
        elist = set()
        for u in list:
            if self.startMap.has_key(u):
                slist = slist.union(self.startMap[u])
            if self.endMap.has_key(u):
                elist =elist.union(self.endMap[u])
        validhits = slist.intersection(elist)
        for mental in validhits:
            for u in unitlist:#call fighter for each unit in list
                if u.mental:
                    mental.broadcast(text,u,unit)



    def addLine(self,line,mind):
        list = line.split()
        if not self.startMap.has_key(list[0]):
            self.startMap[list[0]] = set()
        if not self.endMap.has_key(list[0]):
            self.endMap[list[len(list)-1]] = set()    
            
        self.startMap[list[0]].add(mind)
        self.endMap[list[len(list)-1]].add(mind)
        