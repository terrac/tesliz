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
    node = None
    def increment(self):
        if self.curMovement < self.speed:
            self.curMovement += 1
            return False
        return True     
    
class Unit(object):
   
    def __str__( self ):
        return self.type

    def __init__(self):
        self.attributes = Attributes()
        self.traits = dict()
    body = None
    type = None
    traits = None
    attributes = None
    def getName(self):
        return self.node.getName()
    def increment(self):
        return self.attributes.increment()
    
     
    def startTurn(self):
        self.player.startTurn(self)
        
    def damageHitpoints(self,number):
        self.attributes.hitpoints = self.attributes.hitpoints - number
        #s.app.bodies.index(self.body)
        if self.attributes.hitpoints < 0:
            del s.unitmap[self.node.getName()]
            s.app.sceneManager.getRootSceneNode().removeChild(self.node)
            self.body = None
            
                          
