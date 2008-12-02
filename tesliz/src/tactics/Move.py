from utilities.physics import *
from tactics.Singleton import *
import data.util 
import data.Affects
s = Singleton()
#from math import *
#def distance(v1,v2):
#    return sqrt(pow(v1.x - v2.x,2) +pow(v1.y - v2.y,2) +pow(v1.z - v2.z,2))

class Move(object):
    def __init__(self):
        self.type = "move"
    needsasecondclick = True
    def getEndPos(self):
        return self.__endPos


    def setEndPos(self, value):
        self.__endPos = value


    def delEndPos(self):
        del self.__endPos

    action = False
    
    name= "Move"

    value= 0

    timeleft = -1
    startPos = None
    endPos = None
    time = 5
    def choiceStart(self):
        pos = self.unit1.body.getOgreNode().getPosition()        
        #self.startPos =position  
        #self.endPos.y = position.y
        name = "circle"
        mesh = "cylinder.mesh"
        scene_node = s.app.sceneManager.rootSceneNode.createChildSceneNode(name)
        scene_node.position = Ogre.Vector3(pos.x,pos.y+5,pos.z)
        size = self.unit1.attributes.moves
        size = size * .60
        scene_node.scale = Ogre.Vector3(size,1,size)
        
        scene_node.rotate(Ogre.Quaternion(Ogre.Degree(90), Ogre.Vector3.UNIT_Z))
        attachMe = s.app.sceneManager.createEntity(name,mesh)
        
        scene_node.attachObject(attachMe)
        #TODO: for later 
      #  attachMe.setMaterialName( "Examples/RustySteel" )
        attachMe.setNormaliseNormals(True)
        
        
    def choiceEnd(self):        
        s.app.sceneManager.rootSceneNode.removeChild("circle")
             
    def execute(self,timer):    	#dir(tactics.util)
#    	if self.unit1:
#    		self.unit1.body = self.unit1.body
        if not self.unit1.body:
            s.log("looks like a destroyed unit got here")
            return
    	self.time -= timer
        if self.time < 0:
            return
        self.unit1.body.unFreeze()	
        position = self.unit1.body.getOgreNode().getPosition()
        if s.event:
            s.event.updateMove(position)
        if not self.startPos:
            
            self.startPos =position  
            self.endPos.y = position.y
    
            entity = self.unit1.node.getAttachedObject(0)
            if entity.hasSkeleton():
                self.animationState = entity.getAnimationState("LOOP")
                self.animationState.setLoop(True)
                self.animationState.setEnabled(True)

        entity = self.unit1.node.getAttachedObject(0)
        if entity.hasSkeleton():        
            self.animationState.addTime(timer)    
        direction = self.endPos-position
        direction.normalise()
        self.unit1.body.setVelocity(direction*5)
        finishedMoving = False
        if s.turnbased:
            finishedMoving = not data.util.withinRange(self.startPos, position, self.unit1.attributes.moves)
            #distance(self.startPos, position) > self.unit1.attributes.moves
        if not finishedMoving:
            finishedMoving = data.util.withinRange(self.startPos, position, 2)
            #finishedMoving =distance(self.endPos, position) < 2
        #   self.unit1.body.setVelocity(direction*1)
        #    self.unit1.body.freeze()
            

        if finishedMoving:
            for x in s.unitmap.values():
                x.body.freeze()    
        
        return not finishedMoving

    endPos = property(getEndPos, setEndPos, delEndPos, "EndPos's Docstring")


def markmove(pos):
            
    
    name = s.app.getUniqueName()
    mesh = "cylinder.mesh"
    scene_node = s.app.sceneManager.rootSceneNode.createChildSceneNode(name)
    scene_node.position = Ogre.Vector3(pos.x,pos.y+5,pos.z)
    #size = self.unit1.attributes.moves
    #size = size * .60
    #scene_node.scale = Ogre.Vector3(size,1,size)
    
    #scene_node.rotate(Ogre.Quaternion(Ogre.Degree(90), Ogre.Vector3.UNIT_Z))
    attachMe = s.app.sceneManager.createEntity(name,mesh)
    
    scene_node.attachObject(attachMe)
    #TODO: for later 
  #  attachMe.setMaterialName( "Examples/RustySteel" )
    #attachMe.setNormaliseNormals(True)
class FFTMove():
    action = False
    type = "move"
    value = -1
    name = "move"
    
    def __init__(self,unit = None,endPos = None,speed = 1):
        if unit:
            self.range = unit.attributes.moves
        else:
            self.range = 500,500
            
        self.unit1 = unit
        self.endPos = data.util.getValidPos(endPos)
        self.list = None
        self.cur = 0
        self.speed = speed
        self.affect = None

    needsasecondclick = True
    def choiceStart(self):
        #create a mark that creates a small block
        self.toremove =data.util.markValid(self.unit1.node.getPosition(), self.range, data.util.show)
        
    def choiceEnd(self):
        if self.toremove:
            for x in self.toremove:
                    
                s.app.sceneManager.getRootSceneNode().removeChild(x)
        self.toremove = None
        

    def execute(self,timer):
        #s.playsound("walk.wav")
        if not self.unit1 or not self.unit1.body or not self.unit1.node:
            return
        entity = None
        iter = self.unit1.node.getAttachedObjectIterator()

        
        if not self.list:
            vec1 = self.unit1.body.getOgreNode().getPosition()
            vec2 = self.endPos
            self.list =data.util.getShortest(vec1, vec2, self.unit1.attributes.moves)
            self.list.pop(0)
            if not self.list:
                s.log("cant move",self)
                return False
            self.endPos = self.list[len(self.list)-1]
            self.cur = 0
#            for x in self.list:
#                print x
#            for x in self.list:
#                x.y +=1# don't know why buh will probably need to standardize sizes or offset by size
                #x.x -=10
            if entity:
                self.animationState = entity.getAnimationState("LOOP")
                self.animationState.setLoop(True)
                self.animationState.setEnabled(True)
            return True
            

        
        if entity:        
            self.animationState.addTime(timer)    
        if len(self.list) == self.cur:
            print "end"
            return False
        vec1 = self.unit1.node.getPosition()
        vec2 = self.list[self.cur]
        
        direction = vec2-vec1
        direction.normalise()#techincally this shouldn't be necessary if the grid attribute is 1
        
        vec1 = vec1 + (direction * timer * 3 * self.speed)
        rotateto = vec2 * 1
        rotateto.y = vec1.y
        self.unit1.body.setPositionOrientation(vec1,vec1.getRotationTo(rotateto))

        #print self.unit1.body.getVelocity()
        
        #print vec1
        #print vec2
        #print self.cur
        #print distance(self.unit1.node.getPosition(), vec2)
        
        #print self.unit1
        #print vec1
        #print vec2
        if distance(self.unit1.node.getPosition(), vec2) < .3:
            self.unit1.body.freeze()    
            self.cur += 1

            
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

        