import copy
class Traits():
    def __init__ ( self,listclasses):
        self.listclasses = listclasses
    def __str__(self):
        return str(self.listclasses)        
    def getClassList(self):
        return self.listclasses
    def __getitem__(self, key):
        return self.listclasses[key]
        
    def __setitem__(self, key, value):
        self.listclasses[key] = value
    def getAbilities(self,unit):
        cmap = dict()
        for i in self.listclasses:
            if not self.isAvailable(i,unit):
                continue
             
            cmap[self.getRep(i,unit)] =i 
     
        return cmap
    def isAvailable(self,abil,unit):
        return True
    def getRep(self,abil,unit):
        return abil.name
    def useAbility(self,abil,unit):
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
    
    def __str__(self):
        return str(self.listclasses)+"\n"+str(self.listnumbers)
    def __init__ ( self,listclasses,listnumbers):
        self.listclasses = listclasses
        self.listnumbers = listnumbers
        
                        
    def isAvailable(self,abil,unit):
        return self.listnumbers[self.listclasses.index(abil)]
    def getRep(self,abil,unit):
        i = self.listnumbers[self.listclasses.index(abil)]
        return abil.name + str(i)    
    def useAbility(self,abil,unit):
        i = self.listclasses.index(abil)
        self.listnumbers[i] = self.listnumbers[i] -1
        if self.listnumbers[i] > -1:
            return True
  
    
    
class ItemTraits(Traits):
    
    
    def __init__ ( self,listclasses,player = None):
        self.listclasses = listclasses
        self.player = player
        
               
    def isAvailable(self,abil,unit):
        return self.player.items.itemNum(abil.name)
    def getRep(self,abil,unit):
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
    
    
    def __init__ ( self,listclasses):
        self.listclasses = listclasses
        
        
               
    def isAvailable(self,abil,unit):
        return unit.attributes.magical.points >= abil.magicpoints
    def getRep(self,abil,unit):
        i = abil.magicpoints
        return abil.name + str(i)   
    
    def useAbility(self,abil,unit):
        if unit.attributes.magical.points >= abil.magicpoints:
            unit.attributes.magical.points -= abil.magicpoints
            return True
        
           
                   
        