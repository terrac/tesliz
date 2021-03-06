from tactics.Singleton import *
import tactics.Affect
import tactics.AffectHolder

import ogre.physics.OgreNewt as OgreNewt
import utilities.OgreText
import data.UnitTraits
import data.Stats 
import manager.util

#import tesliz.runthis



class ManageDeath():
    def __init__(self):
        self.count = 3
    def execute(self,unit):
        text = str(self.count)
        ogretext = utilities.OgreText.OgreText(unit.node.getAttachedObject(0),text)
        ogretext.enable(True)
        unit.setText(ogretext)
        if self.count == 0:
            s.removeUnit(unit)
        self.count -= 1
        
          
class Attributes(object):
    def __init__(self):
 
        self.speed = 5
        self.curMovement = 0
        self.moves = 3,3
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
                "\nexp: "+str(self.exp)+
                "\nmoves:"+str(self.moves)
                )
    def extraStuff(self):
        
        return ("       CE,SE,AE"+ 
    "\nphys-EV:"+str(self.physical.classevade)+","+str(self.physical.shieldevade)+","+str(self.physical.accessoryevade)+","+
    "\nmagi-EV:"+str(self.magical.classevade)+","+str(self.magical.shieldevade)+","+str(self.magical.accessoryevade)+","+
    "\nbravery"+str(self.physical.belief)+
    "\nfaith"+str(self.magical.belief))
    
class Unit(object):
    height = 2
    def __str__( self ):
        return str(self.job)+" "+self.getName()
    def destroy(self):
        #if these aren't set to none they could be accessed later even when the nodes are destroyed
        self.node = None
        self.body = None
        if self.text:
            self.text.destroy()
    def __init__(self,name = "blah"):
        self.level = 0
        self.attributes = Attributes()
        self.traits = data.UnitTraits.UnitTraits(self)
        self.affect = tactics.AffectHolder.AffectHolder(self)
        self.items = tactics.AffectHolder.AffectHolder(self)        
        self.mental = None
        self.name = name
        self.job = None
        self.joblist = []
        self.node = None
        self.reset()

    def reset(self):
        self.body = None
        self.type = None
        self.timeleft = 0
        self.text = None
        
        self.actionqueue = []
        self.visible = True
        self.turncount = 0
        self.death = False
        self.node = None
        self.timedbodies = []

    
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
            
    def getJob(self):
        return self.job
    
    def setJob(self, job):
        self.job = job
        
    def getVisible(self):
        return self.visible
    def setVisible(self,bool):
        self.node.setVisible(bool)
        self.visible = bool
    def getDirection(self):
        return self.node.getOrientation()
    def getName(self):
        return self.name
    def increment(self):
       # print self.getName()+" "+str(self.attributes.curMovement)        
        return self.attributes.increment()
    
     
    def incrementTurn(self):
        #print self.timedbodies
        manager.util.incrementTimed(1,self.timedbodies)
    #lasts a number of turns
    def addTurned(self,turns,node,*extra):                 
        x = manager.util.Timed(turns,node,extra)
        self.timedbodies.append(x)
    def startTurn(self):
        if not self.node:
            return
        
        if self.getDeath():
            self.getDeath().execute(self)
            s.turn.nextUnitTurnUnpause()
            return
        if s.turnbased:
            s.framelistener.showAttributesCurrent(self.getName())
            self.incrementTurn()
        self.turncount += 1
        if s.event:
            s.event.turnStarted(self)
        self.player.startTurn(self)
        self.expaccrued = False
        
    def setDeath(self,bool):
        
        if bool and not self.death:
            self.death = ManageDeath()
            if s.event:
                s.event.death(self)
            self.death.execute(self)
            inertia = OgreNewt.CalcSphereSolid( 0, 1 )
            self.body.setMassMatrix( 0.0, inertia )
            

            liveunits = 0
            for e in self.player.unitlist:
                if not e.death and e.node:
                    liveunits +=1            
            if not liveunits:
                s.log("endgame from last unit death",self)
                s.endGame()
#        else:
#            self.death = False
        
        
            
    def getDeath(self):
        return self.death
    def setText(self,text):
        if not self.node:
            return
        if self.text:
            self.text.destroy()
        if isinstance(text, str):
            text = utilities.OgreText.OgreText(self.node.getAttachedObject(0),text)
        self.text = text
        
    def __getstate__(self):
        return {"name":self.name,"attributes":self.attributes,"affect":self.affect,"items":self.items,"job":self.job,"level":self.level,"player":self.player,"joblist":self.joblist}
    def __setstate__(self,dict):
        self.__dict__ = dict
        self.node = None
#        self.traits = {}
        self.traits = data.UnitTraits.UnitTraits(self)
        
        manager.util.resetAttributes(self)
        self.reset()
    