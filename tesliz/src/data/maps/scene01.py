from tactics.util import *

class Unitdata(object):
    def bandit2(self,unit):
        buildUnit(unit,"FastFighter",1,"Computer1")
        
                       
    def bandit1(self,unit):
        buildUnit(unit,"FastFighter",1,"Computer1")
        
    
    def lina(self,unit):
        buildUnit(unit,"Spark",5,"Player1")
        
    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)            