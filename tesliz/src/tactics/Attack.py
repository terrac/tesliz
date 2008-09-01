from tactics.util import *

from math import *

class Attack(object):
    def __init__ ( self,unit1,unit2= None):
         self.unit1 = unit1
         self.unit2 = unit2
         
    unit1 = None
    unit2 = None     

    
    def setUnitAndPosition(self,unit2,position):
        self.unit2 = unit2
    
    def execute(self):
        direction = self.unit1.body.getOgreNode().getPosition() - self.unit2.body.getOgreNode().getPosition()
        self.unit2.body.setVelocity(direction )
        
        return False
             
        #self.node.translate(  direction* (1))
