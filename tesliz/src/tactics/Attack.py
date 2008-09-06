from tactics.util import *
import utilities.SampleFramework as sf
from math import *
from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import ogre.physics.OgreNewt as OgreNewt
s = Singleton()
class Attack(object):
    def __init__ ( self,unit1=None,unit2= None):
        if not unit1:
            return
        self.unit1 = unit1
        self.unit2 = unit2
    def set(self,unit1 = None,unit2= None):     
        self.unit1 = unit1
        self.unit2 = unit2
    def getName(self):
        return "Attack"
    def overallValue(self):
        return 5
    unit1 = None
    unit2 = None     

    
    def setUnitAndPosition(self,unit2,position):
        self.unit2 = unit2
        if not self.unit2:            
            return False
        return True
    
    def execute(self,timer):
        
        if not self.unit1.body or not self.unit2.body:
            return
        direction = self.unit2.body.getOgreNode().getPosition() - self.unit1.body.getOgreNode().getPosition()
        self.unit2.body.setVelocity(direction )
        s.unitmap[self.unit2.body.getOgreNode().getName()].damageHitpoints(self.unit1.attributes.damage)
        
        return False
