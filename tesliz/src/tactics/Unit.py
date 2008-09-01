class Attributes(object):
    hitpoints = None
    speed = None
    curMovement = 0
    player = None
    #node = None
    moves = 5
    damage = 5
    def increment(self):
        if self.curMovement < self.speed:
            self.curMovement += 1
            return False
        return True     
    
class Unit(object):
   
    def __str__( self ):
        return "Unit"

   
    body = None
   
    abilities = dict()
    attributes = Attributes()
    def getName(self):
        return self.node.getName()
    def increment(self):
        self.attributes.increment()
    
     
    def startTurn(self):
        self.player.startTurn(self)
        
                    
