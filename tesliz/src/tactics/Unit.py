class Unit(object):
   
    def __str__( self ):
        return "Unit"

   
    body = None
    hitpoints = None
    speed = None
    curMovement = 0
    player = None
    #node = None
    moves = 5
    damage = 5
    def getName(self):
        return self.node.getName()
    def increment(self):
        if self.curMovement < self.speed:
            self.curMovement += 1
            return False
        return True
    
     
    def startTurn(self):
        self.player.startTurn(self)
        
                    
    def move(self):
        mAnimationState = entity.getAnimationState("Walk");
        mAnimationState.setLoop(True);
        mAnimationState.setEnabled(True);
    
    def idling(self):
        mAnimationState = entity.getAnimationState("Idle");
        mAnimationState.setLoop(True);
        mAnimationState.setEnabled(True);

    def attack(self):
        mAnimationState = entity.getAnimationState("Attack");
        mAnimationState.setLoop(True);
        mAnimationState.setEnabled(True);    
        