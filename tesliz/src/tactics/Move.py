from utilities.physics import *

#from math import *
#def distance(v1,v2):
#    return sqrt(pow(v1.x - v2.x,2) +pow(v1.y - v2.y,2) +pow(v1.z - v2.z,2))

class Move(object):
    action = False
    def __init__ ( self,unit1 = None,pendPos = None):
        if not unit1:
            return
        self.body = unit1.body
        self.endPos = pendPos
    def set(self,unit1 = None,unit2= None):     
        self.unit1 = unit1
        self.unit2 = unit2
        self.body = unit1.body
        self.endPos = unit2.node.getPosition()
        #self.endPos = pendPos
    def getName(self):
        return "Move"
    body = None
    endPos = None
    def overallValue(self):
        return 7
    def setUnitAndPosition(self,unit2,position):
        self.endPos = position
        return True
    
    def execute(self,timer):    	#dir(tactics.util)
    	if not self.body:
    		return
        position = self.body.getOgreNode().getPosition()
         
        direction = self.endPos-position
        direction.normalise()
        self.body.setVelocity(direction*20)
        boo =distance(position, self.endPos) > 2
        
        if not boo:
            self.body.setVelocity(direction*0)
        
        return boo

