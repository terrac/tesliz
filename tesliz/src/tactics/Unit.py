from tactics.Singleton import *

s = Singleton()

class Attributes(object):
    hitpoints = 5
    speed = None
    curMovement = 0
    player = None
    #node = None
    moves = 5
    damage = 5
    sight = 10
    node = None
    
    def increment(self):
        if self.curMovement < self.speed:
            self.curMovement += 1
            return False
        return True     
    def __str__( self ):
        return str(self.hitpoints)
    
class Unit(object):
   
    def __str__( self ):
        return self.type+" "+self.getName()

    def __init__(self):
        self.attributes = Attributes()
        self.traits = dict()
    body = None
    type = None
    traits = None
    attributes = None
    actionqueue = []
    def getName(self):
        return self.node.getName()
    def increment(self):
        return self.attributes.increment()
    
     
    def startTurn(self):
        self.player.startTurn(self)
        
    def damageHitpoints(self,number,eunit=None):
        self.attributes.hitpoints = self.attributes.hitpoints - number
        #s.app.bodies.index(self.body)
        if self.attributes.hitpoints < 0:
            s.removeUnit(self)
            
           # s.app.renderWindow.writeContentsToTimestampedFile("screenshot",".jpg")
                                      
