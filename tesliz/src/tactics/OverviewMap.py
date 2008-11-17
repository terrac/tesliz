import ogre.renderer.OGRE as Ogre
import os
import shelve
import data.util
import tactics.util
import tactics.Move
import time
from tactics.Singleton import *
from utilities.physics import *


def addDots(vec1,vec2,slow = False):

    direction = vec2-vec1
    direction.normalise()

    while True:
        vec1 = vec1 + (direction * 1)
        rvec = data.util.getValidPos(vec1)
        
        
        if rvec:                             
            data.util.createMesh("cylinder.mesh", rvec, .5)
        
        if distance(vec1, vec2) < 2:
            return False
        
        if slow:
            return vec1
        

    
class Position:
    
    def __init__(self,vec,name,visited = False):
        self.plist = []
        #self.dllist = [] do later
        self.position = vec
        #self.node = None
        self.name = name
        self.visited = visited
        self.next = None
    
    def show(self):
        node =data.util.createMesh("cylinder.mesh",self.position,1,self.name)
        tactics.util.buildImmoblePhysics(self,node)
    def getVec(self):
        x,y,z = self.position
        return Ogre.Vector3(x,y,z)
        
class AddPos:
    def __init__(self,cpos,playermap):
        self.actionqueue=[]
        self.timeleft = 0
        if cpos.visited and cpos.next:
            s.framelistener.addToQueue(self,self)
            playermap.map[cpos.next.name] = cpos.next
            playermap.addPos(cpos, cpos.next)
            self.cpos = cpos
            self.vec = self.cpos.getVec()
            self.timel = 0
        
    def execute(self,timer):
        self.timel -= timer
        if self.timel < 0:            
            self.vec = addDots(self.vec,self.cpos.next.getVec(), True)
            s.playsound()
            if not self.vec:
                self.cpos.next.show()
                return False
            self.timel = 1
        return True
        
        
        
class OverviewMap:
    
    timeleft = 0
    newgame = True
    def __init__(self,text):
        self.map = dict()
        self.actionqueue=[]
        self.filename = text
        if os.path.exists(text) and not self.newgame:
            positionmap = shelve.open(text)
            if positionmap.has_key("root"):
                self.root = positionmap["root"]
                self.cpos = positionmap["cpos"]
            else:
                self.setupDefaultPositions()
            positionmap.close()
        else:
            self.setupDefaultPositions()
            
        #if file text exists then load positions from file
        
        #else setup default positions
        
        # load mesh 
        # for each pos create a big dot and call
        
#        camera = s.app.sceneManager.createCamera("wutwut")
        
#        camera.position = Ogre.Vector3(0,5,0)
        #camera.orientation = Ogre.Vector3.NEGATIVE_UNIT_Y
        
        self.buildScene()
        AddPos(self.root, self)

    def buildScene(self):
        s.app.sceneManager.destroyAllMovableObjects()
        s.app.sceneManager.destroyAllEntities()
        s.app.World.destroyAllBodies()
        s.app.parseSceneFile('begin')
        s.app.msnCam.setPosition(Ogre.Vector3(11, 22, -10))
        #s.app.camera.lookAt(Ogre.Vector3(0, 5, 0))
        s.app.msnCam.setOrientation(Ogre.Quaternion(0.305629, -0.144145, 0.851248, 0.401475))
        #data.util.createMesh("Plane.mesh",Ogre.Vector3(0,5,0),10)
        self.raySceneQuery = s.app.sceneManager.createRayQuery(Ogre.Ray())
        node = data.util.createMesh("cylinder.mesh", Ogre.Vector3(0, 20, 0))
        light = s.app.sceneManager.createLight(s.app.getUniqueName())
        light.setType(Ogre.Light.LT_POINT)
        node.attachObject(light)
        #self.createLocations(self.root)
        self.unit = tactics.Unit.Unit()
        self.unit.node = data.util.createMesh("zombie.mesh", self.cpos.getVec() + Ogre.Vector3(0, 5, 0))
        tactics.util.buildPhysics(self.unit)
        self.map.clear()
        
        self.createLocations(self.root)
        
        

        
        #used for
    def createLocations(self,root):
        
        if self.map.has_key(root.name):
            
            return
        else:
            
            self.map[root.name] = root
            root.show()
            
            
            for x in root.plist:
                addDots(root.getVec(),x.getVec())
                self.createLocations(x)
    

            
    #    for x in cpos.plist:
    #        self.addVisits(cpos)
    def setupDefaultPositions(self):
        self.root =pos = Position((0,7,0),"scene01",True)
        pos1 = Position((5,7,0),"fillerscene")
        pos.next = pos1
        
        
        pos1.next = Position((5,7,5),"scene03")
        self.cpos = self.root
        
    def addPos(self,pos1,pos2):
        pos1.plist.append(pos2)
        

    def movePlayer(self,pos):
       pass 
   
    def clickEntity(self,name,position):
       if not self.map.has_key(name):
           return
       self.cpos = self.map[name]
       self.move = tactics.Move.FFTMove()
       self.move.unit1 = self.unit
       self.move.endPos = position
       self.move.list = self.getMoveList(self.root,self.cpos)
       for x in self.move.list:
           print x
       print "aoue"
       s.framelistener.addToQueue(self,self)
    
    def execute(self,timer):
        
        if not self.move.execute(timer) and not self.cpos.visited:
            positionmap = shelve.open(self.filename)
            positionmap["root"] = self.root
            positionmap["cpos"] = self.cpos
            data.util.clearMeshes()
            s.app.loadScene(self.cpos.name)
            return False
        return True
    
    def currentVisited(self,winningplayer):
        self.buildScene()
        self.cpos.visited = True 
        if winningplayer == "Player1":
            AddPos(self.cpos,self)
        
        
    def getMoveList(self,cpos,topos,movedlist =[]):
        
        if cpos == topos:
            return [topos.getVec()]
        for pos in cpos.plist:
             rpos =self.getMoveList(pos,topos,movedlist)
             if rpos:
                 rpos.insert(0,cpos.getVec())
                 return rpos
    
        