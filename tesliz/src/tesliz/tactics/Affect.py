from tactics.Singleton import *
#import tactics.util
#import data.util

class Affects:
    def __init__(self,obj,type = None):
        if isinstance(obj,list):
            self.alist = obj
        else:
            self.alist = [obj]
        self.type = type
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
class StatSet:
    def __init__(self,stat,amount , color = None):
        self.color = color
        if not self.color:
            self.color = 255,0,0 
        self.stat = stat
        self.amount = amount
        
    def setup(self,unit):
        
        obj = unit.attributes
        for x in self.stat:
            val = getattr(obj,x)
            if isinstance(val, int):        
                #y =val + self.amount                            
                setattr(obj,x,self.amount)
            else:
                obj = val
        
        #return [str(unit.name)+"'s "+ self.stat.join(" ")+" set to "+ str(self.amount)]
        
    
            
        
#class TraitAffect:
#    def __init__(self,traitmap , color = None):
#        self.color = color
#        if not self.color:
#            self.color = 0,255,0 
#        self.traits  = set(traitmap.items())
#        
#    def setup(self,unit):
#        
#        for x in self.traitmap.keys():
#            self.inter = dict.fromkeys(unit.traits.items().intersect(self.traits))
#            unit.traits + self.inter 
#            
#
#        
#    def teardown(self,unit):
#        
#        for x in self.traitmap.keys():
#            unit.traits - self.inter