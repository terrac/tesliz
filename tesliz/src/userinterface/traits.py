import copy
class Traits():
    def __init__ ( self,listclasses):
        self.listclasses = listclasses
        
    def getClassList(self):
        return self.listclasses

    def getAbilities(self):
        cmap = dict()
        for i in self.listclasses:
            if not self.isAvailable(i):
                continue
             
            cmap[self.getRep(i)] =i 
     
        return cmap
    def isAvailable(self,abil):
        return True
    def getRep(self,abil):
        return abil.name
    def useAbility(self,abil):
        return True
    def getLearned(self,learnednames,unit):
        learned = []
        for x in self.getClassList():
            if x.name in learnednames:
                learned.append(x)
        trait =copy.copy(self)
        trait.listclasses = learned        
        return trait

class NumberedTraits(Traits):
    
    
    def __init__ ( self,listclasses,listnumbers):
        self.listclasses = listclasses
        self.listnumbers = listnumbers
        
                        
    def isAvailable(self,abil):
        return self.listnumbers[self.listclasses.index(abil)]
    def getRep(self,abil):
        i = self.listnumbers[self.listclasses.index(abil)]
        return abil.name + str(i)    
    def useAbility(self,abil):
        i = self.listclasses.index(abil)
        self.listnumbers[i] = self.listnumbers[i] -1
        if self.listnumbers[i] > -1:
            return True
  
    
    
class ItemTraits(Traits):
    
    
    def __init__ ( self,listclasses,player = None):
        self.listclasses = listclasses
        self.player = player
        
               
    def isAvailable(self,abil):
        return self.player.items.itemNum(abil.name)
    def getRep(self,abil):
        i = self.player.items.itemNum(abil.name)
        return abil.name + str(i)   
    
    def useAbility(self,i):
        if self.player.items.itemNum(i.name):
            self.player.items.removeItem(i.name)
            return True
    def getLearned(self,learnednames,unit):
        trait = Traits.getLearned(self, learnednames, unit)
        trait.player = unit.player
        return trait 
        
        
class MagicTraits(Traits):
    
    
    def __init__ ( self,listclasses,unit):
        self.listclasses = listclasses
        self.unit = unit
        
               
    def isAvailable(self,abil):
        return self.unit.attributes.magical.points > abil.magicpoints
    def getRep(self,abil):
        i = abil.magicpoints
        return abil.name + str(i)   
    
    def useAbility(self,abil):
        if self.unit.attributes.magical.points > abil.magicpoints:
            self.unit.attributes.magical.points -= abil.magicpoints
            return True
        
           
                   
        