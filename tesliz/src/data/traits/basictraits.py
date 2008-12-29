import data.util
import utilities.physics
from tactics.Singleton import *
import ogre.renderer.OGRE as Ogre
import manager.util

def show(unit):
    pos = unit.body.getOgreNode().getPosition()
    sceneManager = s.app.sceneManager        
    name = "turncircle"
    mesh = "cylinder.mesh"
    if not sceneManager.hasSceneNode(name):
        scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
        attachMe = s.app.sceneManager.createEntity(name,mesh)            
        scene_node.attachObject(attachMe)
        #attachMe.setNormaliseNormals(True)
    else:
        scene_node = sceneManager.getSceneNode(name)
    scene_node.position = Ogre.Vector3(pos.x,pos.y+5,pos.z)
    
    size = 1
    scene_node.scale = Ogre.Vector3(size,size,size) 
class Trait():
    action = True
    type = "None"
    value = -1
    name = "notnamed"
    unittargeting = True
    needsasecondclick = True
    timeleft = 0
    jobpoints = 50
    unit2 = None
    endPos = None
    unit1 = None
    offset = [(0,0,0)]
    def getName(self):
        return self.name
    
class FFTMove(Trait):
    action = False
    type = "move"
    name = "move"
    
    unittargeting = False
    def __init__(self,unit = None,endPos = None,speed = 1):

            
        self.unit1 = unit
        self.endPos = data.util.getValidPos(endPos)
        
#        if self.endPos:
#            self.endPos.y +=5
        self.list = None
        self.cur = 0
        self.speed = speed
        self.affect = None

    
    animationState = None

        

    def execute(self,timer):
        #s.playsound("walk.wav")
        if not self.unit1 or not self.unit1.body or not self.unit1.node:
            return
        entity = self.unit1.node.getAttachedObject(0)
        #iter = self.unit1.node.getAttachedObjectIterator()
        
        
        if not self.list:
            
            vec1 = self.unit1.body.getOgreNode().getPosition()
            vec2 = manager.util.cleanup(self.endPos)
            
           # s.gridmap[vec1] = vec1 
            
            if not vec2:
                s.log("vec 2 in move is empty "+str(self.unit1),self)
                aoue
            if hasattr(self, "range") and self.range:
                range = self.range
            else:
                range = self.unit1.attributes.moves
            self.list =data.util.getShortest(vec1, vec2, range)
            
            #offset to not walk in the ground
            for x in self.list:
                x.y +=1
            
            self.list.pop(0)
            size = len(self.list)
            if size and data.util.getValidUnit(self.list[len(self.list)-1], 50):
                self.list.pop()
            if not self.list:
                s.log("cant move",self)
                return False
            self.endPos = self.list[len(self.list)-1]

            if entity:
                self.animationState = entity.getAnimationState("LOOP")
                self.animationState.setLoop(True)
                self.animationState.setEnabled(True)
            return True
            

        
        if entity and self.animationState:        
            self.animationState.addTime(timer)    
        if len(self.list) == self.cur:
            print "end"
            if self.animationState:
                self.animationState.setTimePosition(0)
            
            return False
        vec1 = self.unit1.node.getPosition()
        vec2 = self.list[self.cur]
        
#        print vec1
        #vec2.y = vec1.y
        direction = vec2-vec1
        direction.normalise()#techincally this shouldn't be necessary if the grid attribute is 1
        
        vec1 = vec1 + (direction * timer * 3 * self.speed)
        xzdirection = direction * 1
        xzdirection.y = 0
        xzdirection.normalise()
        xzsrc = vec1 * 1
        xzsrc.y = 0
        xzsrc.normalise()
        #vec1.y +=1
        self.unit1.body.setPositionOrientation(vec1,xzsrc.getRotationTo(xzdirection))

        
        if utilities.physics.distance(self.unit1.node.getPosition(), vec2) < .3:
            self.unit1.body.freeze()    
            self.cur += 1
            if len(self.list) == self.cur:
                self.unit1.body.setPositionOrientation(vec2,xzsrc.getRotationTo(xzdirection))
               # s.gridmap[vec2] = self.unit1
                
            predicate = lambda name: data.Affects.affectmap.has_key(name.split("-")[0])
            name =data.util.getValidName(vec2, predicate)
            if name:                                
                affect = data.Affects.affectmap[name.split("-")[0]]
                if self.affect != affect:
                    self.affect.teardown(self.unit1)
                self.affect.setup(self.unit1)
            elif self.affect:
                self.affect.teardown(self.unit1)
                self.affect = None
                
        return True
class Attack(Trait):
    def __init__(self):
        pass
    name = "Attack"
    value= 5     
    timeleft = 3
    range=1,10
    animation = "LOOP"
    type = "bludgeon"
    sound = "sword.wav"


    

    def getDamage(self,unit):
        return data.damage.weaponPhysical(unit)
    

    def execute(self,timer):
        
  
        if not self.unit1.body or not self.unit2.body:

            return
        

        show(self.unit1)
        
        
        direction = self.unit2.body.getOgreNode().getPosition() - self.unit1.body.getOgreNode().getPosition()
        
        self.unit1.animate(self.animation)
           
        s.playsound(self.sound)    
        #self.unit2.body.setVelocity(direction )        
        unittobehit =s.unitmap[self.unit2.body.getOgreNode().getName()]
    #lambda self,unit2: damageHitpoints(damage.basicPhysical,self.unit1,unit2)
        data.util.damageHitpoints(self.getDamage, self.unit1, unittobehit)

        return False

class GridTargeting(Trait):
    
    
    def __init__(self,offset,todo,name,type="physical",range=(1,1),value = 4):
        self.offset = offset(self)
        self.particlename = 'RedTorch'
        self.name=name
        self.value = value
        
        self.range = range
        #elf.type = type#
        
        self.timeleft = 3
        
        self.sound = "fireball.wav"
        self.todo = todo
        for action in todo:
            if hasattr(action, "getDamage"):
                self.getDamage = action.getDamage
                break
        
    def offset1(self):
        x = 0,0,0
        return [x]
    def offset2(self):
        a = 0,0,0
        b = 1,0,0
        c = 0,0,1
        d = -1,0,0
        e = 0,0,-1
        return [a,b,c,d,e]
    def execute(self,timer):
        print self
        if not self.unit1 or  not self.unit1.body or  not self.endPos:
            return
        unitlist = []
        for pos in self.offset:
            x,y,z = pos
            x = x + self.endPos.x            
            y = y + self.endPos.y
            z = z + self.endPos.z
            vec = Ogre.Vector3(x,y,z)
            unit = data.util.getValidUnit(vec)
            for to in self.todo:
                to.execute(self.unit1,unit,vec)
    
    def __str__( self ):
        return "GridTargeting"+self.name
        
