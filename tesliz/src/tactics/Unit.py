from tactics.Singleton import *

s = Singleton()

class Attributes(object):
    hitpoints = 5
    speed = 5
    curMovement = 0
    #player = None
    #node = None
    moves = 5
    #damage = 5
    sight = 100
    strength = 5
    intelligence = 5
    dexterity = 5
    resistance = dict()
    #node = None
    type = None
    def increment(self):
        if self.curMovement < self.speed:
            self.curMovement += 1
            return False
        else:
            self.curMovement = 0        
        return True     
    def __str__( self ):
        return str(self.hitpoints)
    
class Unit(object):
   
    def __str__( self ):
        return self.type+" "+self.getName()

    def __init__(self):
        self.attributes = Attributes()
        self.traits = dict()
        self.body = None
        self.type = None
        self.timeleft = 0
        
        
        self.actionqueue = []
        self.visible = True
        self.mental = None
        self.knowledgelist = ["General"]
        
    def getVisible(self):
        return self.visible
    def setVisible(self,bool):
        self.node.setVisible(bool)
        self.visible = bool

    def getName(self):
        return self.node.getName()
    def increment(self):
       # print self.getName()+" "+str(self.attributes.curMovement)        
        return self.attributes.increment()
    
     
    def startTurn(self):
        self.player.startTurn(self)
        
    def damageHitpoints(self,number,type = None,eunit=None):
        if self.attributes.resistance.has_key(type):
            number = (1-self.attributes.resistance[type]) * number
        self.attributes.hitpoints = self.attributes.hitpoints - number
        s.log(str(eunit)+" damages "+str(self)+" for "+ str(number)+"with type:"+type)
        #s.app.bodies.index(self.body)
        if self.attributes.hitpoints < 0:
            s.removeUnit(self)
            print self
            #s.app.renderWindow.writeContentsToTimestampedFile("screenshot",".jpg")
                                      
    def getWantedRange(self):
        hv = 0
        ha = None
        for trait in self.traits.values():
            for action in trait.getClassList():
                if action.value > hv:
                    hv = action.value
                    ha = action
        try:
            return action.range -2
        except:
            return 2
                    