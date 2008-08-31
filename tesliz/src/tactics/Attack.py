from tactics.util import *

from math import *

class Attack(object):
    def __init__ ( self,body,direction):
         self.body = body
         self.direction = direction

    direction = None
    body = None
    
    def execute(self):
        self.body.setVelocity(self.direction )
        
        return False
             
        #self.node.translate(  direction* (1))
