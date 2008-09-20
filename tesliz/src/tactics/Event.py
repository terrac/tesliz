from utilities.physics import *
from tactics.Singleton import *
import ogre.physics.OgreNewt as OgreNewt
from tactics.Unit import *
from tactics.util import *
import random
s = Singleton()

class Event:
    def __init__(self,str,level,pos):
        self.str = str
        self.level = level
        self.pos = pos
    
    def execute(self):
        ulist = ["Spark"]
        

        playerlist = s.playermap.keys()
        
        for x in range(0,self.level):
            for z in range(0,self.level):
                #x = x * 3
                #z = z * 3
                start = Ogre.Vector3(self.pos.x+x,self.pos.y+50,self.pos.z+z)
                end = Ogre.Vector3(self.pos.x+x,self.pos.y+-50,self.pos.z+z)
                self.ray = OgreNewt.BasicRaycast( s.app.World, start,end )
                info = self.ray.getFirstHit()
                
                
                #print "au"
                if (info.mBody):
                    
                    #bodpos, bodorient = info.mBody.getPositionOrientation()
                    sceneManager = s.app.sceneManager
                    name = "blah"+str(x)+" "+str(z)
                    mesh = 'cylinder.mesh' 
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
                    buildUnit(unit,unittype,random.randint(1,3),player)
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
        for x in s.unitmap.values():
                x.body.freeze()   

class EventPositions:
    def __init__(self,map):
        self.map = map
    def update(self,pos):
        for x in self.map.keys():
            print distance(x,pos)
            if distance(x,pos) < 10:
                self.map[x].execute()
                del self.map[x]