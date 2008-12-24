import copy
from tactics.Singleton import *
from mental.mind import *

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
#class Grammar:
#    def __init__(self):
#        self.verbl = ["occurred"]
#        self.nounl = ["revolution"]
#        self.articlel = ["the","a"]
#        #self.
#        #self.patternlist = ["article noun verb adverb article noun"]
#        self.root = Tree(None)
#        self.root.add("article").add("noun").add("verb").add("adverb").add("article").add("noun")
#        self.map = dict()
#        #self.list.append([dog,run])
#    def broadcast(self,text,unit,broadcastto= "all"):
#        if broadcastto == "all":
#            unitlist = s.unitmap.values()
#        elif broadcastto == "self":
#            unitlist = [unit]
#        else :
#            unitlist = unit.player.unitlist
#        map = self.getMap(text)
#        
#        for x in self.map.keys():
#            if self.mapEquals(map,x):
#                for y in x:
#                    for u in unitlist:#call fighter for each unit in list
#                        if u.mental:
#                            y.broadcast(text,u,unit)
#        
#    def mapEquals(self,x,y):
#        a = x.keys();
#        b = y.keys();
#        if len(a) != len(b):
#            return False
#        for c in a:
#            if not c in b:
#                return False
#        return True
#    def getMap(self,text):
#        next = self.root
#        stra = text.split()
#        stringmap = Tree(text)
#        for x in stra:
#            found = False
#            for a in next.values():
#                list =getattr(self,a.value+"l")
#                if x in list:
#                    next = a
#                    if stringmap.has_key(a.value):                        
#                        stringmap[a.value].append(x)
#                    else:
#                        stringmap[a.value] = [x]
#                    found = True  
#                    break
#            if not found and len(next) > 1:
#                next = next.values()[0]
#        
#        return stringmap
#
#    def addLine(self, line,mind):
#        x = self.getMap(line)
#        if self.map.has_key(x):
#            self.map[x].append(mind)
#        else:
#            self.map[x] = [mind]
#            if not verb:
#                if x.endswith("ing"):
#                    x = x[0:-3]
#                elif x.endswith("s"):
#                    x = x[0:-1]
#                elif x.endswith("ed"):
#                    x = x[:-2]
#                if x in self.verbl:
#                    verb = x
#            else:
#                if x in self.nounl:
#                    noun = x
#        if not verb    