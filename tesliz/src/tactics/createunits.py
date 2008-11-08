from tesliz.runthis import *
import data.unittypes
from tactics.util import *
import random

from tactics.Singleton import *
s = Singleton()
class CreateRandom():
    def __init__(self,ulist=["Squire","Chemist"],player="Player1",pos = Ogre.Vector3(0,0,0),dir = Ogre.Vector3.UNIT_X,levels=1,levele=3):
        self.pos = pos
        self.dir = dir
        #self.levels = levels,levele
        
        
            
        playerlist = [player]
        
        
        
    
        for x in range(0,1):
            for z in range(0,5):
                x = x * 2 
                z = z * 2
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
                    except NameError, e:
                        pass
                    print scene_node.position
                    print unittype
                    print player
        
                    #getattr(unittypes,(unit,rand)
                    #CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
                    #self.clickEntity(info.mBody.OgreNode.Name,position)
        for x in s.unitmap.values():
                x.body.freeze()   
                

class CreateList():
    def __init__(self,ulist=["Squire","Chemist","Squire"],player="Player1",plist = [Ogre.Vector3(0,0,0),Ogre.Vector3(5,0,0),Ogre.Vector3(0,0,5)],levels= [1,2,1]):
        self.ulist = ulist
        self.player = player
        self.plist = plist
        self.levels = levels
        #self.levels = levels,levele
        
        
            
        playerlist = [player]
        
        
        
    
        for v,u,l in zip(self.plist,self.ulist,self.levels):

            start = Ogre.Vector3(v.x,v.y+50,v.z) 
            end = Ogre.Vector3(v.x,v.y-50,v.z) 
           # print start
            self.ray = OgreNewt.BasicRaycast( s.app.World, start,end )
            info = self.ray.getFirstHit()
            
            
            print start
            print end
            if (info.mBody):
                
                #bodpos, bodorient = info.mBody.getPositionOrientation()
                sceneManager = s.app.sceneManager
                name = s.app.getUniqueName()
                mesh = 'zombie.mesh' 
                scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
                
                dira = (end - start)
                dira.normalise()
                
                position = start + ( dira* ( (end - start).length() * info.mDistance ));
                position.y += 1
                scene_node.position = position 
                
                attachMe = sceneManager.createEntity(name,mesh)
        
                scene_node.attachObject(attachMe)
                unit = Unit()
                unit.node = scene_node
                unittype = u
                player = self.player
                level = l
                
                buildUnit(unit,unittype,"Human",level,player)
                setupExtra(unit)
                unit.node.getAttachedObject(0).setMaterialName(unittype+"/SOLID")
                #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
                try:
                    s.playermap[player].setVisualMarker(unit)
                except AttributeError, e:
                    pass
                print scene_node.position
                print unittype
                print player
    
                #getattr(unittypes,(unit,rand)
                #CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
                #self.clickEntity(info.mBody.OgreNode.Name,position)
            else:
                print v,u +"doesn't have a valid place to put "
        for x in s.unitmap.values():
            x.body.freeze()   
