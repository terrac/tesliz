from tactics.util import *

class Unitdata(object):
    def bandit2(self,unit):
        buildUnit(unit,"FastFighter",1,"Computer1")
        buildPhysics(unit,"Ellipsoid")
                       
    def bandit1(self,unit):
        buildUnit(unit,"FastFighter",1,"Computer1")
        buildPhysics(unit,"Ellipsoid")
    
    def lina(self,unit):
        buildUnit(unit,"Mage",5,"Player1")
        buildPhysics(unit,"Ellipsoid")
    
        
    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        
        buildImmoblePhysics(unit)            