class Grammar:
    def __init__(self):
        
        self.startMap = dict()
        self.endMap = dict()
        
    def broadcast(self,text):
        list = text.split()
        slist = set()
        elist = set()
        for u in list:
            if self.startMap.has_key(u):
                slist = slist.union(self.startMap[u])
            if self.endMap.has_key(u):
                elist =elist.union(self.endMap[u])
        f = slist.intersection(elist)
        for v in f:
            v.broadcast(text)



    def addLine(self,line,mind):
        list = line.split()
        if not self.startMap.has_key(list[0]):
            self.startMap[list[0]] = set()
        if not self.endMap.has_key(list[0]):
            self.endMap[list[len(list)-1]] = set()    
            
        self.startMap[list[0]].add(mind)
        self.endMap[list[len(list)-1]].add(mind)
        