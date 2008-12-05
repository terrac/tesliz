import data.util
import tactics.Affect

class AffectHolder():
    def __init__(self,unit):
        self.itemmap = dict()
        self.unit = unit
    def add(self,item):

#        if self.itemmap.has_key(item.type):
#            self.itemmap[item.type].teardown(self.unit)
        self.itemmap[item.type] = item
        
        tactics.util.resetAttributes(self.unit)
    def do(self,item):
        item.setup(self.unit)
    def remove(self,type):
        am =self.itemmap[type]
        tactics.util.resetAttributes(self.unit)
        #am.teardown(self.unit)
        del self.itemmap[type]
    def has(self,type):
        return self.itemmap.has_key(type)
    def setupAll(self):
        for item in self.itemmap.values():
            item.setup(self.unit)
    def get(self,type):
        if self.itemmap.has_key(type):
            return self.itemmap[type]