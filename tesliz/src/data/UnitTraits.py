import data.traits.generictraits
 
import userinterface.traits  

class UnitTraits():
    def __init__(self,unit):
        self.map = dict()
        self.Primary = None
        self.map["Secondary"] = None
        self.map["Reaction"] = None
        self.map["Movement"] = None
        self.map["Support"] = None        
        self.Move =   userinterface.traits.Traits([data.traits.basictraits.FFTMove(unit)])
        self.Move.name = "Move"
        self.Attack = userinterface.traits.Traits([data.traits.basictraits.Attack()])
        self.Attack.name = "Attack"
        pass
    
    def setupAll(self,unit):
        if self.map["Reaction"]:
            self.map["Reaction"].setup(unit)
        if self.map["Movement"]:    
            self.map["Movement"].setup(unit)
        if self.map["Support"]:    
            self.map["Support"].setup(unit)
    def getUsable(self):
        return [self.Primary,self.map["Secondary"],self.Attack]
    #equippable items
    def getMap(self):
        return self.map
        
    def __getitem__(self, name):
        if name == self.Primary.name:
            return self.Primary
        if self.map["Secondary"] and name == self.map["Secondary"].name:
            return self.map["Secondary"]
        if not hasattr(self, name):
            return False
        return getattr(self, name)
    def __setitem__(self, name, value):
        setattr(self, name, value)
        
    def __getstate__(self):
        return dict()
#    def __setstate__(self,dict):
        
#        self.__dict__ = dict
#        self.traits = {}
        #tactics.util.resetAttributes(self)
        #self.reset()        
