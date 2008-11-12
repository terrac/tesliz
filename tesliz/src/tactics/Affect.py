from tactics.Singleton import *

s = Singleton()
class Affects:
    def __init__(self,obj,type):
        if isinstance(obj,list):
            self.alist = obj
        else:
            self.alist = [obj]
    def setup(self,unit):
        for x in self.alist:
            
            x.setup(unit)
    def teardown(self,unit):
            
        for x in self.alist:
            x.teardown(unit)
            
class AffectsLight:
    def __init__(self,obj,type):
        if isinstance(obj,list):
            self.alist = obj
        else:
            self.alist = [obj]
        self.lights = []
        self.type = type
        self.color = 255,0,0
    def setup(self,unit):
        for x in self.alist:
            light = s.app.sceneManager.createLight( s.app.getUniqueName() )
            self.lights.append(light)
            light.setType( Ogre.Light.LT_POINT )
            dir(light)
    #        light.setDiffuseColor(255,0,0)
            light.DiffuseColor = self.color
            light.SpecularColor = self.color
    #        light.setSpecularColor(255,0,0)
            unit.node.attachObject(light)
            
            x.setup(unit)
    def teardown(self,unit):
        for x in self.lights:            
            unit.node.detachObject(x)
            
        for x in self.alist:
            x.teardown(unit)
    

class AffectHolder():
    def __init__(self,unit):
        self.itemmap = dict()
        self.unit = unit
    def add(self,item):

        if self.itemmap.has_key(item.type):
            self.itemmap[item.type].teardown(self.unit)
        self.itemmap[item.type] = item
        self.itemmap[item.type].setup(self.unit)
    def do(self,item):
        item.setup(self.unit)
    def remove(self,type):
        am =self.itemmap[type]
        am.teardown(self.unit)
        del self.itemmap[type]
    def has(self,type):
        return self.itemmap.has_key(type)
    def setupAll(self):
        for item in self.itemmap.values():
            item.setup(self.unit)
    def get(self,type):
        if self.itemmap.has_key(type):
            return self.itemmap[type]
class StatAffect:
    def __init__(self,statsup,amount , color = None):
        self.color = color
        if not self.color:
            self.color = 255,0,0 
        self.statsup = statsup
        self.amount = amount
        
    def setup(self,unit):
        
        obj = unit.attributes
        for x in self.statsup:
            val = getattr(obj,x)
            if isinstance(val, int):        
                y =val + self.amount                            
                setattr(obj,x,y)
            else:
                obj = val
            

        
    def teardown(self,unit):
        
        for x in self.statsup.keys():
            y = getattr(unit.attributes,x)
            z =self.statsup[x]
            y -= z
            setattr(unit.attributes,x,y)

class TraitAffect:
    def __init__(self,traitmap , color = None):
        self.color = color
        if not self.color:
            self.color = 0,255,0 
        self.traits  = set(traitmap.items())
        
    def setup(self,unit):
        
        for x in self.traitmap.keys():
            self.inter = dict.fromkeys(unit.traits.items().intersect(self.traits))
            unit.traits + self.inter 
            

        
    def teardown(self,unit):
        
        for x in self.traitmap.keys():
            unit.traits - self.inter