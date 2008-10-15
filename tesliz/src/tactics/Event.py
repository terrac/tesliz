from utilities.physics import *
from tactics.Singleton import *
import ogre.physics.OgreNewt as OgreNewt
from tactics.Unit import *
from tactics.util import *
import random
s = Singleton()

class Event:
    def __init__(self,umap,level,pos):
        self.umap = umap
        self.level = level
        self.pos = pos
    
    def execute(self):
        umap = self.umap
        
        s.grammar.broadcast("revolution has occurred",None)
        playerlist = s.playermap.values()
        
        for x in range(0,self.level):
            for z in range(0,self.level):
                x = x * 1.5
                z = z * 1.5
                start = Ogre.Vector3(self.pos.x+x,self.pos.y+50,self.pos.z+z)
                end = Ogre.Vector3(self.pos.x+x,self.pos.y+-50,self.pos.z+z)
                self.ray = OgreNewt.BasicRaycast( s.app.World, start,end )
                info = self.ray.getFirstHit()
                
                
                
                if (info.mBody):
                    
                    #bodpos, bodorient = info.mBody.getPositionOrientation()
                 
                    dira = (end - start)
                    dira.normalise()
                    
                    position = start + ( dira* ( (end - start).length() * info.mDistance ));
                    position.y += 1
                    
                    rlist = umap.keys()
                    racetype = rlist[random.randint(1,len(rlist))-1]
                    ulist = umap[racetype]
                    unittype = ulist[random.randint(1,len(ulist))-1]
                    player = playerlist[random.randint(1,len(playerlist))-1]
                    player = playerlist[0]
                    level = random.randint(1,3)
                    unit = createUnit(position,player,unittype,racetype,level,unittype+"/SOLID")
                    unit.mental = Mind()
                    unit.mental.map  ={"combat":Combat(unit,action.Attack),"follower":Follower(unit)}
                    
                    
                    s.log(str(position) +str(unittype) +str(player),self)
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
            #print distance(x,pos)
            if distance(x,pos) < 10:
                self.map[x].execute()
                del self.map[x]