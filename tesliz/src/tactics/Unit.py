from tactics.Singleton import *
from tactics.Affect import *
s = Singleton()


        

class Attributes(object):
    def __init__(self):
        self.maxhitpoints = 5
        self.hitpoints = 5
        self.speed = 5
        self.curMovement = 0
        self.moves = 25
        self.sight = 100
        self.strength = 5
        self.intelligence = 5
        self.dexterity = 5
        self.resistance = dict()

    def getHitpoints(self):
        return self.__hitpoints


    def setHitpoints(self, value):
        if value > self.maxhitpoints:
            value = self.maxhitpoints
        self.__hitpoints = value


    def delHitpoints(self):
        del self.__hitpoints




    def increment(self):
        if self.curMovement < self.speed:
            self.curMovement += 1
            return False
        else:
            self.curMovement = 0        
        return True     
    def __str__( self ):
        return str(self.hitpoints)

    hitpoints = property(getHitpoints, setHitpoints, delHitpoints, "Hitpoints's Docstring")
    
class Unit(object):
   
    def __str__( self ):
        return self.type+" "+self.getName()

    def __init__(self):
        self.attributes = Attributes()
        self.traits = dict()
        self.affect = AffectHolder(self)
        self.items = AffectHolder(self)
        self.body = None
        self.type = None
        self.timeleft = 0
        
        
        self.actionqueue = []
        self.visible = True
        self.mental = None
        self.knowledgelist = ["general"]
    
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
        s.framelistener.showAttributesCurrent(self.getName())
        self.player.startTurn(self)
        
#    def damageHitpoints(self,number,type = None,eunit=None):
#        if self.attributes.resistance.has_key(type):
#            number = (1-self.attributes.resistance[type]) * number
#        self.attributes.hitpoints = self.attributes.hitpoints - number
#        s.log(str(eunit)+" damages "+str(self)+" for "+ str(number)+"with type:"+type+" :")
#        #s.app.bodies.index(self.body)
#        if self.attributes.hitpoints < 0:
#            s.removeUnit(self)
#            print self
#        if self.attributes.hitpoints > self.attributes.maxhitpoints:
#            self.attributes.hitpoints = self.attributes.maxhitpoints
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
                    