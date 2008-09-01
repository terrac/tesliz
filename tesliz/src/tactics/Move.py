from tactics.util import *

from math import *

class Move(object):
    def __init__ ( self,unit1,pendPos = None):

         self.body = unit1.body
         self.endPos = pendPos

    body = None
    endPos = None
    
    def setUnitAndPosition(self,unit2,position):
        self.endPos = position
        return True
    
    def execute(self):
        position = self.body.getOgreNode().getPosition()
        direction = self.endPos-position
        direction.normalise()
        self.body.setVelocity(direction*50)
        boo =distance(position, self.endPos) > 2
        
        if not boo:
            self.body.setVelocity(direction*0)
        
        return boo
             
        #self.node.translate(  direction* (1))
   
#not finished        
class GridMove(object):
    def __init__ ( self,pbody,pendPos):
         #for grids
         pendpos.x = floor(pendpos.x)

         self.body = pbody         
         
         self.endPos = pendPos

    endPos = None
    b = 0;
    def execute(self):
        #this should really orient towards the end pos
        self.b += 1
        print str(self.b)
        #direction =self.node.Orientation * self.node.Position.UNIT_X
        position = self.body.getOgreNode().getPosition()
        direction = self.endPos-position
        direction.normalise()
        self.body.setVelocity(direction*50)
        boo =distance(position, self.endPos) > 2
        
        if not boo:
            self.body.setVelocity(direction*0)
        
        return boo

        
                        