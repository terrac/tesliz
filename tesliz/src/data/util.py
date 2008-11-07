import random
import math
import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt
import utilities.physics

from tactics.Singleton import *



s = Singleton()

class VectorMap(dict):
    
   
    def __getitem__(self, key):
        key.x = int(key.x)
        key.Y = int(key.y)
        key.z = int(key.z)
        key = str(key)
        return dict.__getitem__(self,key)
        
    def __setitem__(self, key, value):
        key.x = int(key.x)
        key.Y = int(key.y)
        key.z = int(key.z)
        key = str(key)
        dict.__setitem__(self,key, value)
    
    def __delitem__(self, key):
        key.x = int(key.x)
        key.Y = int(key.y)
        key.z = int(key.z)      
        key = str(key)  
        dict.__delitem__(key)
    def has_key(self,key):
        key.x = int(key.x)
        key.Y = int(key.y)
        key.z = int(key.z)
        key = str(key)
        return dict.has_key(self,key)

def show(pos):
    
    sceneManager = s.app.sceneManager        
    name = s.app.getUniqueName()
    mesh = "cylinder.mesh"
    if not sceneManager.hasSceneNode(name):
        scene_node = sceneManager.rootSceneNode.createChildSceneNode(name)
        attachMe = s.app.sceneManager.createEntity(name,mesh)            
        scene_node.attachObject(attachMe)
        attachMe.setNormaliseNormals(True)
    else:
        scene_node = sceneManager.getSceneNode(name)
    scene_node.position = Ogre.Vector3(pos.x,pos.y,pos.z)
    
    size = .3
    scene_node.scale = Ogre.Vector3(size,size,size)
    
    scene_node.rotate(Ogre.Quaternion(Ogre.Degree(90), Ogre.Vector3.UNIT_Z))
 
    return name

def createEntity(mesh,node):    
    sceneManager = s.app.sceneManager
    name = s.app.getUniqueName()         
    attachMe = s.app.sceneManager.createEntity(name,mesh)            
    node.attachObject(attachMe)
    attachMe.setNormaliseNormals(True)

   

def damageHitpoints(number,type,unit1,unit2):
    unit1.attributes.hitpoints = unit1.attributes.hitpoints - number 
    
    s.log(str(unit2)+" damages "+str(unit1)+" for "+ str(number)+"with type:"+type+" :")
    #s.app.bodies.index(unit1.body)
    if unit1.attributes.hitpoints < 1:
        s.event.death(unit1)
        s.removeUnit(unit1)
        
    return
    #determine resistance
#    if unit1.attributes.resistance.has_key(type):
#        number = (1-unit1.attributes.resistance[type]) * number
    degree1 =Ogre.Degree(0, 0)
    vec1 = Ogre.Vector3(0,0,0)
    degree2 =Ogre.Degree(0, 0)
    vec2 = Ogre.Vector3(0,0,0)
    #unit1.node.getOrientation().ToAngleAxis(degree,vec)
    quat1 =unit1.node.getOrientation()
    quat1.ToAngleAxis(degree1,vec1)
    quat2 =unit2.node.getOrientation()
    quat2.ToAngleAxis(degree2,vec2)
    #quat.getYaw().valueDegrees()
    #quat.FromAxes(vec)
    #Ogre.Quaternion(Ogre.Degree(180), Ogre.Vector3.UNIT_X).ToAngleAxis(degree,vec)
#    dir1 = vec
#    quat.xAxis()
#    quat.zAxis()
#    quat.yAxis()
#    degree.valueDegrees()
#    dir1 = unit1.getDirection()
#    dir2 = unit2.getDirection()
    
        
    #determine chance to hit
    if type == "physical":
        
        
        if random.randint(0,100) < unit1.attributes.physical.tohit: #blindness would have a low to hit for example
            unit2.animate("missed")
            return False 
    #    if both pointing in same direction then 100% as one is behind the other
    #might need to update degree
        if vec1 == vec2 and deg1 == deg2:
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate("missed")
                return False
        # if both are absolutely pointing the the same direction then they are facing each other
        elif vec1 == vec2:
            if random.randint(0,100) < unit1.attributes.physical.classevade: #missed
                unit2.animate("missed")
                return False  
            if random.randint(0,100) < unit1.attributes.physical.shieldevade: #missed
                unit2.animate("blocked")
                return False
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate("missed")
                return False
        else: #on the side
            if random.randint(0,100) < unit1.attributes.physical.shieldevade: #missed
                unit2.animate("blocked")
                return False
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate("missed")
                return False
            
        brav1 = unit1.attributes.bravery
        brav2 = unit2.attributes.bravery    
        #a higher bravery than opponent adds damage
        number += ((brav1 - brav2) / 100) * number 
    else: #magical
        if random.randint(0,100) < unit1.attributes.magical.classevade: #missed
            unit2.animate("missed")
            return False  
        if random.randint(0,100) < unit1.attributes.magical.shieldevade: #missed
            unit2.animate("blocked")
            return False
        if random.randint(0,100) < unit1.attributes.magical.accessoryevade: #missed
            unit2.animate("missed")
            return False
        faith1 = unit1.attributes.faith
        faith2 = unit2.attributes.faith    
        #high faith adds damage, but opponents lower faith reduces total damage so a faith of 0 cannot recieve magical damage or healing
        number += ((faith1  / 100) * number) * (faith2  / 100) 
    rand =random.randint(0,100)    
    
    #    if they are s
    
    unit1.attributes.hitpoints = unit1.attributes.hitpoints - number 
    
    s.log(str(unit2)+" damages "+str(unit1)+" for "+ str(number)+"with type:"+type+" :")
    #s.app.bodies.index(unit1.body)
    if unit1.attributes.hitpoints < 1:
        s.removeUnit(unit1)
    return True



def getChanceToHitAndDamage(number,type,unit1,unit2):
    
    dir1 = unit1.getDirection()
    dir2 = unit2.getDirection()
    
        
    #determine chance to hit
    returned  = 1
    if type == "physical":
        tohit = unit1.attributes.physical.tohit/100 
        ce =unit1.attributes.physical.classevade / 100
        se =unit1.attributes.physical.shieldevade / 100
        ae =unit1.attributes.physical.accessoryevade / 100 
        
        returned = tohit
    #    if both pointing in same direction then 100% as one is behind the other
        if dir1 == dir2:
            returned *=tohit * ae
        # if both are absolutely pointing the the same direction then they are facing each other
        elif math.fabs(dir1.x) == math.fabs(dir2.x) or math.fabs(dir1.z) == math.fabs(dir2.z):
            returned *= tohit * ae * se * ce
        else: #on the side
            returned *= tohit * ae * se
            
        brav1 = unit1.attributes.bravery
        brav2 = unit2.attributes.bravery    
        #a higher bravery than opponent adds damage
        number += ((brav1 - brav2) / 100) * number 
    else: #magical
        returned *= tohit * ae * se * ce
        
        faith1 = unit1.attributes.faith
        faith2 = unit2.attributes.faith    
        #high faith adds damage, but opponents lower faith reduces total damage so a faith of 0 cannot recieve magical damage or healing
        number += ((faith1  / 100) * number) * (faith2  / 100) 
    return returned,number 
#def getDamage(number,type):
#for say a spell you would give a high jump
def withinRange(vec1,vec2,range):
    if hasattr(range,'__iter__'):
        moves,jump = range
    else:
        moves = range
        jump = 50
    list =getClosestValid(vec1,vec2, jump)
    moves -=1
    range = moves,jump
    print moves
    if utilities.physics.distance(vec1, vec2) < 2:
        return True
    if moves < 0:
        return False
    
    lowest = 999
    lvec = None
    
    if list:
        for x in list:
            
            dist = utilities.physics.distance(x, vec2)
            if dist < lowest:
                lowest = dist
                lvec = x 
    
    if withinRange(lvec, vec2, range):
        return True
    return False

def markValid(vec1,range,mark,names = None, prevfound=VectorMap()):
    if not names:
        names = set()
    moves,jump = range
    xlist = [0,0,1,-1]
    zlist = [-1,1,0,0]
    list =getValid(vec1, jump,xlist,zlist)
    for x in list:
        if prevfound.has_key(x):
            list.remove(x)
    moves -=1
    range = moves,jump
    if moves < 0:
        return
    for x in list:
        
        names.add(mark(x))
        prevfound[x] = True
        markValid(x, range,mark,names,prevfound)
    return names

#def getDistance(vec1,vec2,height=55, distance = 0):
#    list =getValid(vec1, height)
#    
#    if utilities.physics.distance(vec1,vec2) < 2:
#        return distance
#    for x in list:
#        y =getDistance(x,vec2,distance)
#        
#
#            

#def getValid(vec,height):
#    xlist = [0,0,1,-1]
#    zlist = [-1,1,0,0]
#    validpos = []
#    for a in range(0,3):
#        x = xlist[a]
#        z = zlist[a]
#        start = Ogre.Vector3(vec.x+x,vec.y+height,vec.z+z)
#        end = Ogre.Vector3(vec.x+x,vec.y-height,vec.z+z)
#        ray = OgreNewt.BasicRaycast( s.app.World, start,end )
#        info = ray.getFirstHit()# will need to do multiple hits eventually 
#        
#        if (info.mBody):
#            dira = (end - start)
#            dira.normalise()        
#            position = start + ( dira* ( (end - start).length() * info.mDistance ));
#            validpos.append(position)
#    return validpos
    
def getShortest(vec1,vec2,range, prevfound=VectorMap()):
    if hasattr(range,'__iter__'):
        moves,jump = range
    else:
        moves = range
        jump = 50
    list =getClosestValid(vec1,vec2, jump)
    for x in list:
        if prevfound.has_key(x):
            list.remove(x)
    moves -=1
    range = moves,jump
    
    if utilities.physics.distance(vec1, vec2) < 2:
        return [vec1]
    if moves < 0:
        return [vec1]
    
    lowest = 999
    lvec = None
    lvlist = None
    if list:
        for x in list:
            prevfound[x] = True
            dist = utilities.physics.distance(x, vec2)
            if dist < lowest:
                lowest = dist
                lvec = x 
        print "chosen" + str(lvec)
        lvlist = getShortest(lvec, vec2, range,prevfound)
            
            
    if lvlist:
        lvlist.insert(0,vec1)
        return lvlist

    #return False
    return [vec1]
unitvalue = 1
def getClosestValid(pos,pos2,height):        
    xlist = []
    zlist = []
    if pos.x < pos2.x:  
        xlist.append(unitvalue)
    else:
        xlist.append(-unitvalue)
    
    zlist.append(0)
    if pos.z < pos2.z:
        zlist.append(unitvalue)
    else:
        zlist.append(-unitvalue)
    xlist.append(0)
    print "aoeu"
    print pos
    print pos2
    print "aoeu2"
    print xlist
    print zlist
    validpos = getValid(pos,height,xlist, zlist)
    for x in validpos:
        print x
    print "aoeu3"
        
    return validpos


def getValid(vec,height,xlist, zlist):
    validpos = []
    for a in range(0, len(xlist)):
        x = xlist[a]
        z = zlist[a]
        start = Ogre.Vector3(vec.x + x, vec.y + height, vec.z + z)
        end = Ogre.Vector3(vec.x + x, vec.y - height, vec.z + z)
        ray = OgreNewt.BasicRaycast(s.app.World, start, end)
        info = ray.getFirstHit() # will need to do multiple hits eventually
        if (info.mBody):
            dira = (end - start)
            dira.normalise()
            position = start + (dira * ((end - start).length() * info.mDistance))
            validpos.append(position)
        
    
    return validpos