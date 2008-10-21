from tesliz.runthis import *
import data.unittypes
from tactics.util import *
import random

from tactics.Singleton import *
s = Singleton()
class CreateRandom():
    def __init__(self,pos = Ogre.Vector3(0,0,0),dir = Ogre.Vector3.UNIT_X,types=["Squire","Chemist"],levels=1,levele=3):
        self.pos = pos
        self.dir = dir
        self.types = types
        #self.levels = levels,levele
        
        
            
        playerlist = s.playermap.keys()
        ulist = self.types
        
        
        
        floor = s.app.sceneManager.createEntity("Floora.au.", "simple_terrain.mesh" )
        floornode = s.app.sceneManager.getRootSceneNode().createChildSceneNode( "FloorNodea" )
        floornode.attachObject( floor )
        #floor.setMaterialName( "Examples/DarkMaterial" )
    
        floor.setCastShadows( False )
    
        ##Ogre.Vector3 siz(100.0, 10.0, 100.0)
        col = OgreNewt.TreeCollision( s.app.World, floornode, True )
        bod = OgreNewt.Body( s.app.World, col )
        
        ##floornode.setScale( siz )
        bod.attachToNode( floornode )
        bod.setPositionOrientation( Ogre.Vector3(0.0,-10.0,0.0), Ogre.Quaternion.IDENTITY )
        
        s.app.bodies.append ( bod )
    
    
        for x in range(0,10):
            for z in range(0,10):
                x = x 
                z = z 
                start = Ogre.Vector3(x,50,z) + self.pos
                end = Ogre.Vector3(x,-50,z) + self.pos
               # print start
                self.ray = OgreNewt.BasicRaycast( s.app.World, start,end )
                info = self.ray.getFirstHit()
                
                
                
                if (info.mBody):
                    
                    #bodpos, bodorient = info.mBody.getPositionOrientation()
                    sceneManager = s.app.sceneManager
                    name = s.app.getUniqueName()
                    mesh = 'zombie.mesh' 
                    scene_node = sceneManager.rootSceneNode.createChildSceneNode(name)
                    
                    dira = (end - start)
                    dira.normalise()
                    
                    position = start + ( dira* ( (end - start).length() * info.mDistance ));
                    position.y += 1
                    scene_node.position = position 
                    
                    attachMe = sceneManager.createEntity(name,mesh)
            
                    scene_node.attachObject(attachMe)
                    unit = Unit()
                    unit.node = scene_node
                    unittype = ulist[random.randint(1,len(ulist))-1]
                    player = playerlist[random.randint(1,len(playerlist))-1]
                    level = random.randint(levels,levele)
                    level = 2
                    buildUnit(unit,unittype,"Human",level,player)
                    setupExtra(unit)
                    unit.node.getAttachedObject(0).setMaterialName(unittype+"/SOLID")
                    #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
                    try:
                        s.playermap[player].setVisualMarker(unit)
                    except:
                        pass
                    print scene_node.position
                    print unittype
                    print player
                    #getattr(unittypes,(unit,rand)
                    #CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
                    #self.clickEntity(info.mBody.OgreNode.Name,position)
#        for x in s.unitmap.values():
#                x.body.freeze()   
        

    