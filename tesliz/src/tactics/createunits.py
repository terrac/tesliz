#from tesliz.runthis import *
import data.unittypes
from tactics.util import *
import random
import tactics.Unit
import ogre.renderer.OGRE as Ogre
from tactics.Singleton import *
import data.util
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
                    unit.node.getAttachedObject(0).setMaterialName(unit.job.material)
                    #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
                    if hasattr( s.playermap[player], "setVisualMarker"):
                        s.playermap[player].setVisualMarker(unit)
                    
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
                unit = tactics.Unit.Unit()
                unit.name = scene_node.getName()
                unit.node = scene_node
                unittype = u
                player = self.player
                level = l
                
                buildUnit(unit,unittype,"Human",level,player)
                setupExtra(unit)
                unit.node.getAttachedObject(0).setMaterialName(unit.job.material)
                #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
                if hasattr( s.playermap[player], "setVisualMarker"):
                    s.playermap[player].setVisualMarker(unit)
               
                #print scene_node.position
                #print unittype
                #print player
    
                #getattr(unittypes,(unit,rand)
                #CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
                #self.clickEntity(info.mBody.OgreNode.Name,position)
            else:
                print v,u +"doesn't have a valid place to put "
        for x in s.unitmap.values():
            x.body.freeze()   
class SetupPlayer():
    def __init__(self,player="Player1",plist = [Ogre.Vector3(0,0,0),Ogre.Vector3(5,0,0),Ogre.Vector3(0,0,5)]):
        
        self.player = s.playermap[player]
        self.plist = plist
        
        #self.levels = levels,levele
        
        
            
  
        
        
        
    
        for v,unit in zip(self.plist,self.player.unitlist):

            start = Ogre.Vector3(v.x,v.y+10,v.z) 
#            end = Ogre.Vector3(v.x,v.y-50,v.z) 
           # print start
            #self.ray = OgreNewt.BasicRaycast( s.app.World, start,end )
            #info = self.ray.getFirstHit()
            position = data.util.getValidPos(start)
            ## update pointer's position
            if (position):

                ## Application.debugText("Intersect %f, %f, %f " % ( x, y, z) )
                position.y +=1
#            print start
#            print end
                
                #bodpos, bodorient = info.mBody.getPositionOrientation()
                sceneManager = s.app.sceneManager
                name = unit.name
                 
                scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
                
#                dira = (end - start)
#                dira.normalise()
                
#                position = start + ( dira* ( (end - start).length() * info.mDistance ));
#                position.y += 1
                scene_node.position = position 
                
                attachMe = sceneManager.createEntity(name,unit.job.mesh)
        
                scene_node.attachObject(attachMe)
                scene_node.setScale(Ogre.Vector3(1,.5,1))
             
                unit.node = scene_node
                buildPhysics(unit)

                s.unitmap[unit.getName()]=unit
                unit.node.getAttachedObject(0).setMaterialName(unit.job.material)
                #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
                if hasattr( s.playermap[player], "setVisualMarker"):
                    s.playermap[player].setVisualMarker(unit)
               
                print scene_node.position
              
    
                #getattr(unittypes,(unit,rand)
                #CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
                #self.clickEntity(info.mBody.OgreNode.Name,position)
            else:
                print str((v,unit)) +"doesn't have a valid place to put "
        for x in s.unitmap.values():
            if x.body:
                x.body.freeze()
            else:
                pass   
