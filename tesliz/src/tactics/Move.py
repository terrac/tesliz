from tactics.util import *

class Move(object):
    def __init__ ( self,pbody,pendPos):

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
             
        #self.node.translate(  direction* (1))
        

        
                        