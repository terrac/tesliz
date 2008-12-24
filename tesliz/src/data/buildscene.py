from tactics.Singleton import *
import ogre.physics.OgreNewt as OgreNewt
import math
class MapInfo():
    def __init__(self,pos):
        self.pos = pos
        self.infos = []
        #self.height = pos.y
        
    
    def getLeft(self):
        if len(self.infos) > 0:
            return self.infos[0]
    def getRight(self):
        if len(self.infos) > 1:
            return self.infos[1]
    def getUp(self):
        if len(self.infos) > 2:
            return self.infos[2]
        
    def getDown(self):
        if len(self.infos) > 3:
            return self.infos[3]
    
    def __str__(self):
        ret = str(self.pos) +":"
        for x in self.infos:
            ret += str(x.pos) +","
        return ret    
class GridMap(dict):
    def __init__(self,pos):
        self.root = MapInfo(pos)
        #self.map = dict()
        self[pos] = self.root 
    def add(self,info1,info2):
        info1.infos.append(info2)
        self[info2.pos] = info2
        
        
    def getOff(self,x,z=0):
        info = self.root
        if z > 0:
            for m in range(0,z):
                info = info.getLeft()
        if z < 0:
            for m in range(0,abs(z)):
                info = info.getRight()
        if x > 0:
            for m in range(0,x):
                info = info.getUp()
        if x < 0:
            for m in range(0,abs(x)):
                info = info.getDown()                
        return info
   
    def __getitem__(self, key):
        key = str(key)
        return dict.__getitem__(self,key)
        
    def __setitem__(self, key, value):
        key = str(key)
        dict.__setitem__(self,key, value)
    
    def __delitem__(self, key):        
        dict.__delitem__(key)
    def has_key(self,key):
        key = str(key)
        return dict.has_key(self,key)
class SetupGrid():
    def __init__(self):
        self.curinfo = s.gridmap.root
        self.map = dict()
    def addValid(self,vec1,range):
        moves,jump = range
        extra = []
        while True:
            
            list =self.getValid(vec1, jump)
           
            info = s.gridmap[vec1]
    
            y = ""

            onenew = False
            for x in list:
                if s.gridmap.has_key(x):
                    info2 = s.gridmap[x]
                    
                else:
                    info2 = MapInfo(x)
                    extra.append(x)
                    onenew = True
               
                s.gridmap.add(info,info2)
                
                     
                vec1 = x
            
            
            if not onenew:
                
                if len(extra) == 0:    
                    break
                else: 
                    vec1 = extra.pop()
    
    
    multiple = 4
    def getValid(self,vec,height):
        xlist = [0,0,self.multiple,-self.multiple]
        zlist = [-self.multiple,self.multiple,0,0]
        validpos = []
        for a in range(0,3):
            x = xlist[a]
            z = zlist[a]
            start = Ogre.Vector3(vec.x+x,vec.y+height,vec.z+z)
            end = Ogre.Vector3(vec.x+x,vec.y-height,vec.z+z)
            ray = OgreNewt.BasicRaycast( s.app.World, start,end )
            info = ray.getFirstHit()# will need to do multiple hits eventually 
            
            if (info.mBody):
                dira = (end - start)
                dira.normalise()        
                position = start + ( dira* ( (end - start).length() * info.mDistance ));
                position = Ogre.Vector3(int(position.x),int(position.y),int(position.z))
                spos = str(position)
                #if not self.map.has_key(spos):
                validpos.append(position)
                
        return validpos    
def setup():
    vec = Ogre.Vector3(0,0,0)
    height = 30
    x = 0
    z = 0
    start = Ogre.Vector3(vec.x+x,vec.y+height,vec.z+z)
    end = Ogre.Vector3(vec.x+x,vec.y-height,vec.z+z)
    ray = OgreNewt.BasicRaycast( s.app.World, start,end )
    info = ray.getFirstHit()# will need to do multiple hits eventually 
    
    if (info.mBody):
        dira = (end - start)
        dira.normalise()        
        position = start + ( dira* ( (end - start).length() * info.mDistance ));
    else:
        raise Exception("This has to be here")
    range = 999,999
    s.gridmap = GridMap(position)
    
    setup = SetupGrid()
    setup.addValid(position,range)
