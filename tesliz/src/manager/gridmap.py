import ogre.renderer.OGRE as Ogre
import ogre.addons.et as ET
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI
#import SampleFramework
import exceptions, random, os
#from CEGUI_framework import *   ## we need the OIS version of the framelistener etc
import ogre.physics.OgreNewt as OgreNewt


from tactics.Singleton import *

def getValid(vec,height,xlist , zlist):
    validpos = []
    for a in range(0, len(xlist)):
        
        
        
        x = xlist[a]
        z = zlist[a]
        start = Ogre.Vector3(vec.x + x, vec.y + height, vec.z + z)
        
        if getValidUnit(start, height):
            continue
                
        ray =  Ogre.Ray(start,Ogre.Vector3(0,-1,0))
        result = s.terrainmanager.getTerrainInfo().rayIntersects(ray)
        intersects = result[0]
        ## update pointer's position
        if (intersects):
            x = result[1][0]
            y = result[1][1]
            z = result[1][2]
            ## Application.debugText("Intersect %f, %f, %f " % ( x, y, z) )
            position =Ogre.Vector3(x, y, z)   
            

            
            validpos.append(position)
        
    
    return validpos
#gets positions even if there is a unit on the tile
#not for general use only really for when terrain deforms
def getPositions(vec,height = 50,xlist = [0] , zlist= [0]):
    validpos = []
    for a in range(0, len(xlist)):
        
        
        
        x = xlist[a]
        z = zlist[a]
        start = Ogre.Vector3(vec.x + x, vec.y + height, vec.z + z)
        
        
                
        ray =  Ogre.Ray(start,Ogre.Vector3(0,-1,0))
        result = s.terrainmanager.getTerrainInfo().rayIntersects(ray)
        intersects = result[0]
        ## update pointer's position
        if (intersects):
            x = result[1][0]
            y = result[1][1]
            z = result[1][2]
            ## Application.debugText("Intersect %f, %f, %f " % ( x, y, z) )
            position =Ogre.Vector3(x, y, z)   
            

            
            validpos.append(position)
        
    
    return validpos
def getValidPos(vec, height = 50):
    if not vec:
        return 
    vlist = getValid(vec, height, [0], [0])
    if vlist:
        return vlist[0]
    
def getValidName(vec,predicate,height=5):


    start = Ogre.Vector3(vec.x , vec.y + height, vec.z )
    end = Ogre.Vector3(vec.x , vec.y - height, vec.z )
    ray = OgreNewt.BasicRaycast(s.app.World, start, end)
    
    for x in range(0,ray.getHitCount()):
        info = ray.getInfoAt(x)
        
        if (info.mBody and info.mBody.getOgreNode()):
            name = info.mBody.getOgreNode().getName()
            if predicate(name):
                return info.mBody.getOgreNode()
def getValidUnit(vec,height = 5):
    predicate = lambda name:s.unitmap.has_key(name)
    name = getValidName(vec, predicate, height)
    if name:
        return s.unitmap[name.getName()]
    

    #unit.attributes.hitpoints = 500 * level

class Gridmap(dict):
    def __init__(self):        
        s.gridmap = self
        dict.__init__(self)
        
    def generate(self,key):
        
        pos =getValidPos(key, 50)
        if not pos:
            pos = getValidUnit(key,50)
        if not pos:
            pos = getValidName(key, lambda name:True, 50)
        
        #false if nothing there, eventually will need to add meshes I think
        self[key] = pos
    def hasUnit(self,key):
        key =str(key)
        #don't want to really inherit too much here to avoid loops
        #realistically the unit class should be smaller
        if self[key].__class__.__name__ == "Unit":
            return True
    def hasMesh(self,key):
        key =str(key)
        if not isinstance(self[key], Ogre.Vector3):
            return True
    def getName(self,key):        
        return self[key].getName()
            
    def __getitem__(self, key):
        key =str(key)
        return dict.__getitem__(self,key)
        
    def __setitem__(self, key, value):
        key =str(key)
        dict.__setitem__(self,key, value)
    
    def __delitem__(self, key):
        key =str(key)
        
        dict.__delitem__(key)
    def has_key(self,key):
        key =str(key)
        return dict.has_key(self,key)
        