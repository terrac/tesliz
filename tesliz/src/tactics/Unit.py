from tactics.Singleton import *

s = Singleton()

class Attributes(object):
    hitpoints = 5
    speed = 5
    curMovement = 0
    player = None
    #node = None
    moves = 5
    #damage = 5
    sight = 100
    strength = 5
    intelligence = 5
    dexterity = 5
    resistance = dict()
    node = None
    type = None
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
    visible = True
    
    
    def getVisible(self):
        return self.visible
    def setVisible(self,bool):
        self.node.setVisible(bool)
        self.visible = bool

    def getName(self):
        return self.node.getName()
    def increment(self):
        return self.attributes.increment()
    
     
    def startTurn(self):
        self.player.startTurn(self)
        
    def damageHitpoints(self,number,type,eunit=None):
        if self.attributes.resistance.has_key(type):
            number = self.attributes.resistance[type] * number
        self.attributes.hitpoints = self.attributes.hitpoints - number
        #s.app.bodies.index(self.body)
        if self.attributes.hitpoints < 0:
            s.removeUnit(self)
            
            #s.app.renderWindow.writeContentsToTimestampedFile("screenshot",".jpg")
                                      
