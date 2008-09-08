from tactics.util import *
import utilities.SampleFramework as sf
from math import *
from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import ogre.physics.OgreNewt as OgreNewt
from utilities.physics import *
s = Singleton()
class Attack(object):

    name = "Attack"
    value= 5     

    
    
    def execute(self,timer):
        
        if not self.unit1.body or not self.unit2.body:
            return
        if distance(self.unit2.body.getOgreNode().getPosition(), self.unit1.body.getOgreNode().getPosition()) > 5:
            return 
        
        direction = self.unit2.body.getOgreNode().getPosition() - self.unit1.body.getOgreNode().getPosition()
        
        
        self.unit2.body.setVelocity(direction )        
        s.unitmap[self.unit2.body.getOgreNode().getName()].damageHitpoints(self.unit1.attributes.damage)
        
        return False
