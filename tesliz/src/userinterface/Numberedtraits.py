#from data.traits.Generictraits import *
class NumberedTraits(object):
    
    cmap = dict()
    listclasses = None
    listnumbers = None
    def __init__ ( self,listclasses,listnumbers):
        self.listclasses = listclasses
        self.listnumbers = listnumbers
               
         
    
    
    def getAbilities(self):
        retlist = []
        for i in range(0,len(self.listclasses)):
            if self.listnumbers[i] == 0:
                continue
            
            string = self.listclasses[i].getName() + str(self.listnumbers[i]) 
            self.cmap[string] = i
            retlist.append(string)
        return retlist
    
    def useAbility(self,text):
        i = self.cmap[str(text)]
        self.listnumbers[i] = self.listnumbers[i] -1
        return self.listclasses[i]