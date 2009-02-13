import ogre.renderer.OGRE as Ogre
from tactics.Singleton import *
import userinterface.util
def cleanup(key):

    if not key:
        return key
    
    if int(key.x) + .50 > key.x:
        key.x = int(key.x)
    else:
        key.x = int(key.x) + 1
    try:
        if int(key.y) + .50 > key.y:
            key.y = int(key.y)
        else:
            key.y = int(key.y) + 1
    except:#infinity
        key.y = 0
    if int(key.z) + .50 > key.z:
        key.z = int(key.z)
    else:
        key.z = int(key.z) + 1        

    return key


class VectorMap(dict):
    
   
    def __getitem__(self, key):
        key =cleanup(key)
        key = str(key)
        return dict.__getitem__(self,key)
        
    def __setitem__(self, key, value):
        key =cleanup(key)
        key = str(key)
        dict.__setitem__(self,key, value)
    
    def __delitem__(self, key):
              
        key = str(key)  
        dict.__delitem__(key)
    def has_key(self,key):
        key =cleanup(key)
        key = str(key)
        return dict.has_key(self,key)

def incrementTimed(timesincelastframe, timedbodies):
    toremove = []
    for x in timedbodies:
        x.seconds -= timesincelastframe
        if x.seconds < 0:
            toremove.append(x)
            if isinstance(x.node, Ogre.SceneNode):
                s.app.sceneManager.getRootSceneNode().removeChild(x.node)
            
            if hasattr(x.node, "destroy"):
                getattr(x.node, "destroy")()
                
    for x in toremove:
        timedbodies.remove(x)
class Timed():
    def __init__(self,seconds,node,body):
        self.seconds = seconds
        self.node = node
        self.body = body
    def __str__(self):
        name = None
        if self.node:
            name = str(self.node.getName())
        return str(self.seconds)+" "+name+"\n"
    
def showAttributes(name):
    if not s.unitmap.has_key(name):
        return
    unit = s.unitmap[name]

    frame = userinterface.util.getNewWindow("attributes", userinterface.util.frame, "root_wnd",.0,.0,.4,.3)
    
    text = "\n"+str(unit.attributes)
    #text += "\n"+str(unit.node.getPosition())    
    text =str(unit)+text
    userinterface.util.getNewWindow("regUnitStuff",userinterface.util.statictext, frame, 0,0,.5,1, text)                
    userinterface.util.getNewWindow("extraUnitStuff",userinterface.util.statictext, frame, .5,0,.5,1, unit.attributes.extraStuff())
    
def resetAttributes(unit):
    try:
        hitpoints = unit.attributes.physical.points
        magicpoints = unit.attributes.magical.points
    except:
        hitpoints = 0
        magicpoints = 0
        #if they don't exist yet then ignore
        # the 0s should only be called in an unimportant part I think so don't worry about them
    
    if unit.job:
        unit.job.resetAttributes(unit)
    unit.items.setupAll()
    unit.affect.setupAll()
    unit.traits.setupAll(unit)
    unit.attributes.physical.points = hitpoints
    unit.attributes.magical.points = magicpoints
    unit.traits.Move.getClassList()[0].range = unit.attributes.moves