from tactics.Singleton import *
from tactics.Affect import *
s = Singleton()
import ogre.physics.OgreNewt as OgreNewt
import utilities.OgreText 

class ManageDeath():
    def __init__(self):
        self.count = 3
    def execute(self,unit):
        text = str(self.count)
        print text
        print "aoeu"
        ogretext = utilities.OgreText.OgreText(unit.node.getAttachedObject(0),s.app.camera,text)
        ogretext.enable(True)
        unit.text =ogretext
        if self.count == 0:
            s.removeUnit(unit)
        self.count -= 1
        
          
class Attributes(object):
    def __init__(self):
 
        self.speed = 5
        self.curMovement = 0
        self.moves = 25
        self.level = 1
        self.exp = 0
      #  self.sight = 100,100
      #  self.strength = 5
      #  self.intelligence = 5
      #  self.dexterity = 5
      #  self.resistance = dict()





    def increment(self):
        if self.curMovement < 100:
            self.curMovement += self.speed
            return False
        else:
            self.curMovement = 0        
        return True     
    def __str__( self ):
        return ("hp: "+str(self.physical.points)+"/"+str(self.physical.maxpoints)+
                "\nmp: "+str(self.magical.points)+"/"+str(self.magical.maxpoints)+
                "\nct: "+str(self.curMovement)+"/100"+
                "\nlevel:"+str(self.level)+ 
                "\nexp: "+str(self.exp)+""
                )

    
class Unit(object):
   
    def __str__( self ):
        return str(self.job)+" "+self.getName()
    def destroy(self):
        if self.text:
            self.text.destroy()
    def __init__(self,name = "blah"):
        self.attributes = Attributes()
        self.traits = dict()
        self.affect = AffectHolder(self)
        self.items = AffectHolder(self)
        self.body = None
        self.type = None
        self.timeleft = 0
        self.text = None
        
        
        self.actionqueue = []
        self.visible = True
        self.mental = None
        self.knowledgelist = ["general"]
        self.turncount = 0
        self.death = False
        self.name = name
        self.node = None
    
    def animate(self,text):
        entity = None
        iter = self.node.getAttachedObjectIterator()
        while iter.hasMoreElements():
            x = iter.getNext()
            if hasattr(x, "hasSkeleton") and x.hasSkeleton():
                entity = x
                break;

        if entity:
            animationState = entity.getAnimationState(text)
            animationState.setLoop(False)
            animationState.setEnabled(True)
            s.app.animations.append(animationState)
            
    def getVisible(self):
        return self.visible
    def setVisible(self,bool):
        self.node.setVisible(bool)
        self.visible = bool

    def getName(self):
        return self.name
    def increment(self):
       # print self.getName()+" "+str(self.attributes.curMovement)        
        return self.attributes.increment()
    
     
    def startTurn(self):
        if self.getDeath():
            self.getDeath().execute(self)
            return
        s.framelistener.showAttributesCurrent(self.getName())
        self.turncount += 1
        if s.event:
            s.event.turnStarted(self)
        self.player.startTurn(self)
        self.expaccrued = False
        
    def setDeath(self,bool):
        
        if bool and not self.death:
            self.death = ManageDeath()
            s.event.death(self)
            self.death.execute(self)
            inertia = OgreNewt.CalcSphereSolid( 0, 1 )
            self.body.setMassMatrix( 0.0, inertia )
        else:
            self.death = False
        
        
            
    def getDeath(self):
        return self.death
                    