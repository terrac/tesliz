import ogre.renderer.OGRE as Ogre
import os
import shelve
import data.util
from tactics.Singleton import *
from utilities.physics import *

class Position:
    
    def __init__(self,vec):
        self.plist = []
        self.position = vec
    

class PlayerMap:
    
    def __init__(self,text):
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
        data.util.createMesh("Plane.mesh",Ogre.Vector3(0,5,0),10)
        
        self.raySceneQuery = s.app.sceneManager.createRayQuery(Ogre.Ray())

        node = data.util.createMesh("cylinder.mesh",Ogre.Vector3(0,20,0))
        light = s.app.sceneManager.createLight( s.app.getUniqueName() )
        
        light.setType( Ogre.Light.LT_POINT )
 
        node.attachObject(light)
 
        self.createLocations(self.root)
       # Find the current position, fire a Ray straight down
       # in order to determine the distance to the terrain
       # If we are too close, keep the distance to a certain amount
 
       
        
        
    def createLocations(self,root, vmap = data.util.VectorMap()):
        
        if vmap.has_key(root.position):
            return
        else:
            vmap[root.position] = True
            data.util.createMesh("cylinder.mesh",root.position)
            
            
            
            for x in root.plist:
                self.addDots(root,x)
                self.createLocations(x)
    
    
    def setupDefaultPositions(self):
        self.root = Position(Ogre.Vector3(0,7,0))
        self.root.plist.append(Position(Ogre.Vector3(5,7,0)))
    
    def addPos(self,pos1,pos2):
        pos1.plist.append(pos2)
        
    def addDots(self,pos1,pos2,slow= False):
        vec1 = pos1.position
        vec2 = pos2.position
        direction = vec2-vec1
        direction.normalise()

        while True:
            vec1 = vec1 + (direction * 1)
            
            rayvec = vec1+ Ogre.Vector3(0,40,0)
            updateRay =  Ogre.Ray(rayvec, Ogre.Vector3.NEGATIVE_UNIT_Y)
            print rayvec
            self.raySceneQuery.setQueryTypeMask(1)
            self.raySceneQuery.Ray = updateRay
            print len(self.raySceneQuery.execute())
            for queryResult in self.raySceneQuery.execute():
                if queryResult: 
                    tcpos = Ogre.Vector3(vec1.x,vec1.y-queryResult.distance + 4,vec1.z)            
                    data.util.createMesh("cylinder.mesh", vec1, .5)
            
            if distance(vec1, vec2) < 2:
                break;
            
        return True
        
    def movePlayer(self,pos):
       pass 
    
        