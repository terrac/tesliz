import runthis
from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import os
import tactics.createunits
import shelve

class CreateLand():
    def __init__(self,landlist):
        pass
class CreateUnits():
    def __init__(self,unitlist,player):
        
        
        
        for flatunit in unitlist:

            v = flatunit.position
            level = flatunit.level
            unittype = flatunit.unittype

            start = Ogre.Vector3(v.x,v.y+50,v.z) 
            end = Ogre.Vector3(v.x,v.y-50,v.z) 
           
            self.ray = OgreNewt.BasicRaycast( s.app.World, start,end )
            info = self.ray.getFirstHit()
            
            
            print start
            print end
            if (info.mBody):
                
                #bodpos, bodorient = info.mBody.getPositionOrientation()
                sceneManager = s.app.sceneManager
                name = s.app.getUniqueName()
                 
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

def checkScene():
     if os.path.exists( "test.map"):
         return True
def buildScene():
    #build scenery from the map and then save a copy that the poller can load
    rootmap = shelve.open("test.map")
    landlist = rootmap["landlist"]
    CreateLand(landlist)
    
    player = rootmap["Computer1"]
    CreateUnits(player.unitlist,"Computer1")
    
    player = rootmap["Player1"]
    CreateUnits(player.unitlist,"Player1")
    
    
class PollerListener(ogre.FrameListener):
    def frameStarted(self, frameEvent):
        if checkScene():
            buildScene()
            s.framelistener.pauseturns = False
            s.app.loadScene("test.scene",True)    
def startup():
    s.app.pollerlistener = PollerListener()
    s.app.root.addFrameListener(s.app.pollerlistener)
if __name__ == '__main__':
#    try:

    application = runthis.OgreNewtonApplication(startup)
    application.go()
        

    