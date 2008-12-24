from utilities.physics import *
from tactics.Singleton import *
import data.util 
import data.Affects

import ogre.renderer.OGRE as Ogre

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
