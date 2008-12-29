import random
import math
import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt
import utilities.physics
import utilities.OgreText 
#import data.unittypes
from tactics.Singleton import *
import userinterface.traits
#import data.traits.generictraits
#import tactics.trait
import ogre.gui.CEGUI as CEGUI
s = Singleton()
import manager.util

def show(pos, texturename = None ,name = None,size = .3):
    
    sceneManager = s.app.sceneManager        
    if not name:
        name = s.app.getUniqueName()
    if not texturename:
        texturename = "Spark/SOLID"
    mesh = "box.mesh"
    if not sceneManager.hasSceneNode(name):
        scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
        createEntity(mesh, scene_node)
        #attachMe = s.app.sceneManager.createEntity(name,mesh)            
        #scene_node.attachObject(attachMe)
        #attachMe.setNormaliseNormals(True)
    else:
        scene_node = sceneManager.getSceneNode(name)
    scene_node.position = Ogre.Vector3(pos.x,pos.y,pos.z)
    
    
    scene_node.setScale(Ogre.Vector3(size,size,size))
    scene_node.getAttachedObject(0).setMaterialName( texturename)
#    scene_node.rotate(Ogre.Quaternion(Ogre.Degree(90), Ogre.Vector3.UNIT_Z))
 
    return name

def fromCameraToMesh():
    mouse = CEGUI.MouseCursor.getSingleton().getPosition()
    rend = CEGUI.System.getSingleton().getRenderer()
    mx = mouse.d_x / rend.getWidth()
    my = mouse.d_y / rend.getHeight()
    camray = s.app.camera.getCameraToViewportRay(mx,my)
    

    #start = camray.getOrigin()
    #end = camray.getPoint( 100.0 )
    s.app.raySceneQuery.setRay(camray)

    result = s.app.raySceneQuery.execute()
    position = False
    name = None
    
    for item in result:
        
        #if item.worldFragment:
        #dir(item.movable)
    
        if item.movable.Name == "PlayerCam" or item.movable.Name.startswith("ETTerrain/Terrain/Tile"):
            continue
        
        position = item.movable.ParentSceneNode.getPosition()
        
        name = item.movable.Name
        break
    if not position:
        result = s.terrainmanager.getTerrainInfo().rayIntersects(camray)
        intersects = result[0]
        ## update pointer's position
        if (intersects):
            x = result[1][0]
            y = result[1][1]
            z = result[1][2]
            ## Application.debugText("Intersect %f, %f, %f " % ( x, y, z) )
            position =Ogre.Vector3(x, y+1, z)
            name = "terrain"
    if position:
        manager.util.cleanup(position)
    return name,position

def createEntity(mesh,node):    
    sceneManager = s.app.sceneManager
    name = s.app.getUniqueName()

    attachMe = s.app.sceneManager.createEntity(name,mesh)            
    node.attachObject(attachMe)
    #attachMe.setNormaliseNormals(True)


meshlist = []
def createMesh(mesh,pos,size=1,name = None):
    
    sceneManager = s.app.sceneManager     
    if not name:   
        name = s.app.getUniqueName()
    if sceneManager.hasSceneNode(name):
        scene_node = sceneManager.getSceneNode(name)
    else:
        scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
    attachMe = s.app.sceneManager.createEntity(name,mesh)            
    scene_node.attachObject(attachMe)
    meshlist.append(scene_node.getName())
    #attachMe.setNormaliseNormals(True)


    scene_node.setScale(Ogre.Vector3(size,size,size))
    
    scene_node.position = pos
 
    return scene_node
   
#def clearMeshes():
    #s.app.sceneManager.getRootSceneNode().removeAndDestroyAllChildren()
    #s.app.reset()
    #s.app.sceneManager.destroyAllMovableObjects()
    
    #s.app.World.destroyAllBodies()
    
    
    
   
missed = "LOOP"
blocked = "LOOP"
def update(text,unit):
    ogretext = utilities.OgreText.OgreText(unit.node.getAttachedObject(0),text)
    ogretext.enable(True)
    s.framelistener.addTimed(1,ogretext)
    unit.setText(ogretext)
def damageHitpoints(getDamage,unit1,unit2):
    number,type = getDamage(unit1)

    if unit2.death:
        return
    #return
    #determine resistance
#    if unit1.attributes.resistance.has_key(type):
#        number = (1-unit1.attributes.resistance[type]) * number
    deg1 =Ogre.Degree(0, 0)
    vec1 = Ogre.Vector3(0,0,0)
    deg2 =Ogre.Degree(0, 0)
    vec2 = Ogre.Vector3(0,0,0)
    #unit1.node.getOrientation().ToAngleAxis(degree,vec)
    quat1 =unit1.node.getOrientation()
    quat1.ToAngleAxis(deg1,vec1)
    quat2 =unit2.node.getOrientation()
    quat2.ToAngleAxis(deg2,vec2)
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
        
        
        if random.randint(0,100) > unit1.attributes.physical.tohit: #blindness would have a low to hit for example
            unit2.animate(missed)
            update("missed", unit2)
            return False 
    #    if both pointing in same direction then 100% as one is behind the other
    #might need to update degree
        if vec1 == vec2 and deg1 == deg2:
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate(missed)
                update("blocked", unit2)
                return False
        # if both are absolutely pointing the the same direction then they are facing each other
        elif vec1 == vec2:
            if random.randint(0,100) < unit1.attributes.physical.classevade: #missed
                unit2.animate(missed)
                update("missed", unit2)
                return False  
            if random.randint(0,100) < unit1.attributes.physical.shieldevade: #missed
                unit2.animate(blocked)
                update("blocked", unit2)
                return False
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate(missed)
                update("blocked", unit2)
                return False
        else: #on the side
            if random.randint(0,100) < unit1.attributes.physical.shieldevade: #missed
                unit2.animate(blocked)
                update("blocked", unit2)
                return False
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate(missed)
                update("blocked", unit2)
                return False
             
    else: #magical
        if random.randint(0,100) < unit1.attributes.magical.classevade: #missed
            unit2.animate(missed)
            return False  
        if random.randint(0,100) < unit1.attributes.magical.shieldevade: #missed
            unit2.animate(blocked)
            return False
        if random.randint(0,100) < unit1.attributes.magical.accessoryevade: #missed
            unit2.animate(missed)
            return False    
        #high faith adds damage, but opponents lower faith reduces total damage so a faith of 0 cannot recieve magical damage or healing
         
        
    
    #    if they are s
    
    unit2.attributes.physical.points = unit2.attributes.physical.points - number *s.damagemultiplier 
    update(str(number), unit2)
    experienceAccrued(unit1, unit2)
    s.log(str(unit1)+" damages "+str(unit2)+" for "+ str(number)+"with type:"+type+" :")
    #s.app.bodies.index(unit1.body)
    if unit2.attributes.physical.points < 1:
        unit2.setDeath(True)
    return True



def getChanceToHitAndDamage(getDamage,unit1,unit2):
    number,type = getDamage(unit1)

    
        
    #determine chance to hit
    chancetohit  = 1
    if type == "physical":
        dir1 = unit1.getDirection()
        dir2 = unit2.getDirection()
        tohit = (100-unit1.attributes.physical.tohit)/100 
        ce =(100-unit1.attributes.physical.classevade) / 100
        se =(100-unit1.attributes.physical.shieldevade) / 100
        ae =(100-unit1.attributes.physical.accessoryevade) / 100 
        
        chancetohit = tohit
    #    if both pointing in same direction then 100% as one is behind the other
        if dir1 == dir2:
            chancetohit *=tohit * ae
        # if both are absolutely pointing the the same direction then they are facing each other
        elif math.fabs(dir1.x) == math.fabs(dir2.x) or math.fabs(dir1.z) == math.fabs(dir2.z):
            chancetohit *= tohit * ae * se * ce
        else: #on the side
            chancetohit *= tohit * ae * se
            
        brav1 = unit1.attributes.physical.belief
        brav2 = unit2.attributes.physical.belief
        #a higher bravery than opponent adds damage
        number += ((brav1 - brav2) / 100) * number 
    else: #magical
        ae =(100-unit1.attributes.physical.accessoryevade) / 100  
        chancetohit *= 1 * ae
        
        faith1 = unit1.attributes.magical.belief
        faith2 = unit2.attributes.magical.belief    
        #high faith adds damage, but opponents lower faith reduces total damage so a faith of 0 cannot recieve magical damage or healing
        number += ((faith1  / 100) * number) * (faith2  / 100) 
    return chancetohit,number 
#def getDamage(number,type):
#for say a spell you would give a high jump

def experienceAccrued(unit1,unit2):
    if not unit1.expaccrued:
        exp = unit2.attributes.level - unit1.attributes.level + 10
        jp = 10 +unit1.job.level * 3
        
        unit1.attributes.exp += exp
        if unit1.attributes.exp > 100:
            unit1.attributes.exp = 0
            unit1.attributes.level +=1
        unit1.job.addExp(unit1,jp)
        
        unit1.expaccrued = True
        update(str(exp)+" exp "+str(jp)+" jp",unit1)
        
def withinRange(vec1,vec2,range):
    if hasattr(range,'__iter__'):
        moves,jump = range
    else:
        moves = range
        jump = 50
    if not vec1 or not vec2:
        return
    list =getClosestValid(vec1,vec2, jump)
    moves -=1
    range = moves,jump
    
    if utilities.physics.ignoreHeightDistance(vec1, vec2) < 1.3:
        return True
    if moves <= 0:
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

xzlist = [(0,-1),(0,1),(1,0),(-1,0)]
def markValid(vec1,range,mark,names = None, prevfound=None):
    if not names:
        names = set()
    if not prevfound:
        prevfound = manager.util.VectorMap()
    
    if hasattr(range,'__iter__'):
        moves,jump = range
    else:
        moves = range
        jump = 50
    
    #xlist = []
    #zlist = []
    list = []
    
    for x,z in xzlist:
        cvec = Ogre.Vector3(vec1.x+ x,vec1.y,vec1.z+z)
        if not( prevfound.has_key(cvec) and moves < prevfound[cvec]):
            list.append(getValidPos(cvec, jump))

    moves -=1
    

    range = moves,jump
    if moves < 0:
        return
    for x in list:
        if x:
            names.add(mark(x))
            prevfound[x] = moves
            markValid(x, range,mark,names,prevfound)
    return names
xlist = [0,0,1,-1]
zlist = [-1,1,0,0]
def getAllValid(vec1,range,valid = None, prevfound=None):
    if not valid:
        valid = []
    if not prevfound:
        prevfound = manager.util.VectorMap()
    
    moves,jump = range

    list =getValid(vec1, jump,xlist,zlist)
    for x in list:
        if prevfound.has_key(x):
            list.remove(x)
    moves -=1
    range = moves,jump
    if moves < 0:
        return
    for x in list:
        
        valid.append(x)
        prevfound[x] = True
        getAllValid(x, range,valid,prevfound)
    return valid

def getShortest(vec1,vec2,range, prevfound=None):
    if not prevfound:
        prevfound = manager.util.VectorMap()
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
    
    if utilities.physics.ignoreHeightDistance(vec1, vec2) < 1:
        return [vec1]
    if moves < 0 and s.turnbased:
        return [vec1]
#    print vec1
#    print vec2
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
        
        lvlist = getShortest(lvec, vec2, range,prevfound)
            
            
    if lvlist:
        #
        
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
    
    validpos = getValid(pos,height,xlist, zlist)
        
    return validpos


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
                return name
def getValidUnit(vec,height = 5):
    predicate = lambda name:s.unitmap.has_key(name)
    name = getValidName(vec, predicate, height)
    if name:
        return s.unitmap[name]


    #unit.attributes.hitpoints = 500 * level
    #unit.attributes.damage = 50 * level
    #unit.attributes.magical = Fstats()
    #unit.attributes.physical = Fstats()
    #unit.attributes.faith = 50
    #unit.attributes.bravery = 50
    