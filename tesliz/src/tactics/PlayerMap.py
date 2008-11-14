import ogre.renderer.OGRE as Ogre
import os
import shelve
import data.util
import tactics.util
import tactics.Move
from tactics.Singleton import *
from utilities.physics import *

class Position:
    
    def __init__(self,vec,name,visited = False):
        self.plist = []
        #self.dllist = [] do later
        self.position = vec
        self.node = None
        self.name = name
        self.visited = visited
    
    def show(self):
        self.node =data.util.createMesh("cylinder.mesh",self.position,1,self.name)
        tactics.util.buildImmoblePhysics(self)
class PlayerMap:
    
    timeleft = 0
    
    def __init__(self,text):
        self.map = dict()
        self.actionqueue=[]
        if os.path.exists(text):
            positionmap = shelve.open(text)
            self.root = positionmap["root"]
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
        
        #s.app.msnCam.setPosition(Ogre.Vector3(0, 10, 0))
        #s.app.camera.lookAt(Ogre.Vector3(0, 5, 0))
        s.app.msnCam.setOrientation(Ogre.Quaternion(0.793987, -0.472373, 0.32888, 0.195663))
        #data.util.createMesh("Plane.mesh",Ogre.Vector3(0,5,0),10)
        
        self.raySceneQuery = s.app.sceneManager.createRayQuery(Ogre.Ray())

        node = data.util.createMesh("cylinder.mesh",Ogre.Vector3(0,20,0))
        light = s.app.sceneManager.createLight( s.app.getUniqueName() )
        
        light.setType( Ogre.Light.LT_POINT )
 
        node.attachObject(light)
 
        self.createLocations(self.root)
        self.unit = tactics.Unit.Unit()
        self.unit.node = data.util.createMesh("zombie.mesh", self.root.position + Ogre.Vector3(0,5,0))
        tactics.util.buildPhysics(self.unit)
       
        
        
    def createLocations(self,root, vmap = data.util.VectorMap()):
        
        if vmap.has_key(root.position):
            return
        else:
            vmap[root.position] = True
            self.map[root.name] = root
            root.show()
            
            
            for x in root.plist:
                self.addDots(root,x)
                self.createLocations(x)
    
    
    def setupDefaultPositions(self):
        self.root = Position(Ogre.Vector3(0,7,0),"scene01")
        self.root.plist.append(Position(Ogre.Vector3(5,7,0),"scene02"))
    
    def addPos(self,pos1,pos2):
        pos1.plist.append(pos2)
        
    def addDots(self,pos1,pos2,slow= False):
        vec1 = pos1.position
        vec2 = pos2.position
        direction = vec2-vec1
        direction.normalise()

        while True:
            vec1 = vec1 + (direction * 1)
            rvec = data.util.getValidPos(vec1)
            
            if rvec:                             
                data.util.createMesh("cylinder.mesh", rvec, .5)
            
            if distance(vec1, vec2) < 2:
                break;
            
        return True
        
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
            s.app.loadScene(self.cpos.name)
            return False
        return True
    def getMoveList(self,cpos,topos,movedlist =[]):
        
        if cpos == topos:
            return [topos.position]
        for pos in cpos.plist:
             rpos =self.getMoveList(pos,topos,movedlist)
             if rpos:
                 rpos.insert(0,cpos.position)
                 return rpos
    
        