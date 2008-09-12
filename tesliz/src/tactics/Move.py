from utilities.physics import *
from tactics.Singleton import *
s = Singleton()
#from math import *
#def distance(v1,v2):
#    return sqrt(pow(v1.x - v2.x,2) +pow(v1.y - v2.y,2) +pow(v1.z - v2.z,2))

class Move(object):
    action = False
    
    name= "Move"

    value= 0

    
    startPos = None
    time = 5
    def execute(self,timer):    	#dir(tactics.util)
    	if self.unit1:
    		self.body = self.unit1.body
        if not self.body:
            s.log("looks like a destroyed unit got here")
            return
    	self.time -= timer
        if self.time < 0:
            return
        	
        position = self.body.getOgreNode().getPosition()
        if not self.startPos:
            self.startPos =position  
            self.endPos.y = position.y
        direction = self.endPos-position
        direction.normalise()
        self.body.setVelocity(direction*20)
        boo =distance(self.startPos, position) < self.unit1.attributes.moves
        #print distance(self.startPos, position)
        if not boo:
            self.body.setVelocity(direction*1)
            self.body.freeze()
        
        return boo

