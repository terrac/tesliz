import data.util
import tactics.Affect
import manager.util

class AffectHolder():
    def __init__(self,unit):
        self.itemmap = dict()
        self.unit = unit
    def add(self,item):

#        if self.itemmap.has_key(item.type):
#            self.itemmap[item.type].teardown(self.unit)
        self.itemmap[item.type] = item
        
        manager.util.resetAttributes(self.unit)
    def do(self,item):
        item.setup(self.unit)
    def remove(self,type):
        am =self.itemmap[type]
        manager.util.resetAttributes(self.unit)
        #am.teardown(self.unit)
        del self.itemmap[type]
    def removeAll(self):
        self.itemmap.clear()
            
    def has(self,type):
        return self.itemmap.has_key(type)
    def setupAll(self):
        for item in self.itemmap.values():
            item.setup(self.unit)
    def get(self,type):
        if self.itemmap.has_key(type):
            return self.itemmap[type]
    def __getitem__(self, key):    
        return self.get(key)
    def getMap(self):
        return self.itemmap
    def __str__(self):
        return str(self.itemmap)