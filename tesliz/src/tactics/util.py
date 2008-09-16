from tactics.Singleton import *
import ogre.physics.OgreNewt as OgreNewt
import ogre.renderer.OGRE as Ogre

from data.unittypes import *
s = Singleton()

def buildUnit(unit,unittype,level,playername):
    s.unitmap[unit.getName()]=unit
    
    unit.type = unittype
    getattr(Unittypes(), unittype)(unit,level)
    
    if s.playermap.has_key(playername):
        player = s.playermap[playername]
        player.unitlist.append(unit)
        unit.player = player
        
    else:
        s.playermap[unit.getName()] = player
        
    buildPhysics(unit,"Ellipsoid")


def buildPhysics(unit,type= None):        
    
    col = None

    if type:
    #TODO convex hulls -figure out and do
        col = getattr(OgreNewt, type)(s.app.World,Ogre.Vector3(1,1,1))
    else:    
        col = OgreNewt.Box(s.app.World, Ogre.Vector3(1,1,1))
    body = OgreNewt.Body( s.app.World, col)
      

    ## something new: moment of inertia for the body.  this describes how much the body "resists"
    ## rotation on each axis.  realistic values here make for MUCH more realistic results.  luckily
    ## OgreNewt has some helper functions for calculating these values for many primitive shapes!
    inertia = OgreNewt.CalcSphereSolid( 10.0, 1.0 )
    body.setMassMatrix( 10.0, inertia )

    #node.setPosition(0.0, 0.0, 0.0)
    ## attach to the scene node.
    body.attachToNode( unit.node )
    unit.body= body
    ## this is a standard callback that simply add a gravitational force (-9.8*mass) to the body.
    

    ## set the initial orientation and velocity!
    body.setPositionOrientation( unit.node.getPosition(),unit.node.getOrientation() )
    #body.setVelocity( (direct * 50.0) )
    
    ## note that we have to keep the bodies around :)
  
    body.setAutoFreeze(1)
    body.setLinearDamping(0)
    body.setAngularDamping(Ogre.Vector3(0,0,0))
    body.setStandardForceCallback()
  
    OgreNewt.UpVector(s.app.World,body,s.vector.UNIT_Y)
  #  OgreNewt.UpVector(s.app.World,body,s.vector.UNIT_Z)
    OgreNewt.UpVector(s.app.World,body,s.vector.UNIT_X)
    #body.setUserData(unit)
    

def buildImmoblePhysics(unit):
    #floor = s.app.sceneManager.createEntity("Floor1", "Cube.mesh" )        
    #floornode = s.app.sceneManager.getRootSceneNode().createChildSceneNode( "FloorNode1" )
    #floornode.attachObject( floor )
    #floornode.setScale(Ogre.Vector3(10,10,10))
    #floornode.setPosition(Ogre.Vector3(0,-10,0))
    #floor.setMaterialName( "LightBlue/SOLID" )

    #floor.setCastShadows( False )
    node = unit.node
    ##Ogre.Vector3 siz(100.0, 10.0, 100.0)
    col = OgreNewt.TreeCollision( s.app.World, node, True )
    bod = OgreNewt.Body( s.app.World, col )
    
    ##floornode.setScale( siz )
    bod.attachToNode( node )
    bod.setPositionOrientation( Ogre.Vector3(0.0,-25.0,0.0), Ogre.Quaternion.IDENTITY )
    
    s.app.bodies.append ( bod )