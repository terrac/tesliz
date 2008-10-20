from tesliz.runthis import *
import data.unittypes
from tactics.util import *
import random
class RandomBuilder(OgreNewtonApplication):
    def __init__(self):
        OgreNewtonApplication.__init__(self)
        
    def parseSceneFile(self):
        pass    
    def _createScene ( self ):        
        OgreNewtonApplication._createScene(self)
        self.msnCam = self.sceneManager.getRootSceneNode().createChildSceneNode()
        self.msnCam.attachObject( self.camera )
        self.camera.setPosition(0.0, 0.0, 0.0)
        self.msnCam.setPosition( 0.0, -10.0, 20.0)
    
        ##make a light
        light = self.sceneManager.createLight( "Light1" )
        light.setType( Ogre.Light.LT_POINT )
        light.setPosition( Ogre.Vector3(0.0, 100.0, 100.0) )
        floor = self.sceneManager.createEntity("Floor", "simple_terrain.mesh" )
        floornode = self.sceneManager.getRootSceneNode().createChildSceneNode( "FloorNode" )
        floornode.attachObject( floor )
        floor.setMaterialName( "Examples/DarkMaterial" )
    
        floor.setCastShadows( False )
    
        ##Ogre.Vector3 siz(100.0, 10.0, 100.0)
        col = OgreNewt.TreeCollision( self.World, floornode, True )
        bod = OgreNewt.Body( self.World, col )
        
        ##floornode.setScale( siz )
        bod.attachToNode( floornode )
        bod.setPositionOrientation( Ogre.Vector3(0.0,-10.0,0.0), Ogre.Quaternion.IDENTITY )
        
        self.bodies.append ( bod )
    
        
        ulist = dir(data.unittypes.Unittypes())
        ulist =filter(lambda x: not x.startswith("_"),ulist)
#        ulist = ["Wizard","TimeMage","Ninja","Priest","Knight"]
        ulist = ["Priest"]
        playerlist = s.playermap.keys()
        
        for x in range(0,10):
            for z in range(0,10):
                x = x * 2
                z = z * 2
                start = Ogre.Vector3(x,50,z)
                end = Ogre.Vector3(x,-50,z)
                self.ray = OgreNewt.BasicRaycast( self.World, start,end )
                info = self.ray.getFirstHit()
                
                
                #print "au"
                if (info.mBody):
                    
                    #bodpos, bodorient = info.mBody.getPositionOrientation()
                    sceneManager = s.app.sceneManager
                    name = "blah"+str(x)+" "+str(z)
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
                    level = random.randint(1,3)
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
        for x in s.unitmap.values():
                x.body.freeze()   
        

    
if __name__ == '__main__':
    try:
        application = RandomBuilder()
        application.go()
    except Ogre.OgreException, e:
        print e