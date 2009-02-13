from tactics.Singleton import *
import ogre.physics.OgreNewt as OgreNewt
import ogre.renderer.OGRE as Ogre
#from mental.mind import *
#from mental.background import *
import tactics.Unit
#from mental.combat import *
import data.unittypes
import mental.combat as combat
import data.jobs
import data.util
import userinterface.traits
import mental.mind
import manager.util
#import data.joblist
s = Singleton()


    
def buildUnit(unit,unittype,race,level,playername):
    s.unitmap[unit.getName()]=unit
    
    #unit.type = unittype
    
    
    if s.playermap.has_key(playername):
        player = s.playermap[playername]
        player.addToUnitlist(unit)
        unit.player = player
        
    else:

        s.playermap[unit.getName()] = player
    setupBasic(unit, level)
    getattr(data.unittypes.Unittypes(), unittype)(unit,level)
    
    
    buildPhysics(unit,"Ellipsoid")
    manager.util.resetAttributes(unit)
    tactics.util.setupMaxPoints(unit)
#creates a unit given a specific job
def buildUnitNoNode(name,playername,unittype,level=1):
    
    unit = tactics.Unit.Unit(name)
    s.unitmap[unit.getName()]=unit
    #s.unitmap[unit.getName()]=unit
    
    
    if s.playermap.has_key(playername):
        player = s.playermap[playername]
        player.addToUnitlist(unit)
        unit.player = player
    setupBasic(unit, level)
    getattr(data.unittypes.Unittypes(), unittype)(unit,level)
    manager.util.resetAttributes(unit)
    tactics.util.setupMaxPoints(unit)
    setupExtra(unit)
    return unit

def setupMaxPoints(unit):
    unit.attributes.physical.points = unit.attributes.physical.maxpoints
    unit.attributes.magical.points = unit.attributes.magical.maxpoints 
    
def setupBasic(unit, level):
    
    #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
   
#    move = userinterface.traits.Traits([data.traits.basictraits.FFTMove(unit)])
#    move.action = False
#    unit.traits["Move"] = move
#    attack = userinterface.traits.Traits([data.traits.generictraits.Attack()])
#    unit.traits["Attack"] = attack
    unit.level = level
        
    
    
    
    
def buildPhysics(unit,type= None,scale = Ogre.Vector3(1,1,1)):        
    
    col = None

    if type:
    #TODO convex hulls -figure out and do
        col = getattr(OgreNewt, type)(s.app.World,Ogre.Vector3(1,1,1))
    else:    
        col = OgreNewt.Box(s.app.World, Ogre.Vector3(.5,3,.5))
    body = OgreNewt.Body( s.app.World, col)
      

    ## something new: moment of inertia for the body.  this describes how much the body "resists"
    ## rotation on each axis.  realistic values here make for MUCH more realistic results.  luckily
    ## OgreNewt has some helper functions for calculating these values for many primitive shapes!
    
    #removed because its not really necessary for fft
    #inertia = OgreNewt.CalcSphereSolid( 10.0, scale.y )
    #body.setMassMatrix( 10.0, inertia )

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
  
    #OgreNewt.UpVector(s.app.World,body,Ogre.Vector3.UNIT_Y)
  #  OgreNewt.UpVector(s.app.World,body,s.vector.UNIT_Z)
    #OgreNewt.UpVector(s.app.World,body,Ogre.Vector3.UNIT_X)
    #body.setUserData(unit)
    

def buildImmoblePhysics(unit,node = None):
    #floor = s.app.sceneManager.createEntity("Floor1", "Cube.mesh" )        
    #floornode = s.app.sceneManager.getRootSceneNode().createChildSceneNode( "FloorNode1" )
    #floornode.attachObject( floor )
    #floornode.setScale(Ogre.Vector3(10,10,10))
    #floornode.setPosition(Ogre.Vector3(0,-10,0))
    #floor.setMaterialName( "LightBlue/SOLID" )

    #floor.setCastShadows( False )
    if not node:
        node = unit.node
    ##Ogre.Vector3 siz(100.0, 10.0, 100.0)
    col = OgreNewt.TreeCollision( s.app.World, node, True )
    bod = OgreNewt.Body( s.app.World, col )
    
    ##floornode.setScale( siz )
    bod.attachToNode( node )
    bod.setPositionOrientation( node.getPosition(),node.getOrientation() )
    
    s.app.bodies.append ( bod )

def setupExtra(unit, mentalstate = None):
    player = unit.player
    if unit.node:
        if hasattr( player, "setVisualMarker"):
            player.setVisualMarker(unit)
   
        if s.fog and player.name == "Computer1":
            unit.setVisible(False)
    
#    if not mentalstate:
#        mentalstate = mental.mind.Mind([mental.combat.Combat(unit,mental.action.Attack,combat.isWanted)])    
        #mental.state = {"angry":0,"happy":0}
#    has = hasattr(unit,"mental")
#    if has and not unit.mental or not has:
#        unit.mental = mentalstate
    data.joblist.setupJobList(unit)
    return unit
def createUnit(position,player,unittype,level=1,name = None,material = None ,mesh = None ,mental = None):
    player = s.playermap[player]
    if not name:
        name = s.app.getUniqueName()+unittype +"-"+player.name   
    
    sceneManager = s.app.sceneManager                        
    scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)                        
    scene_node.position = position             
    
    unit = tactics.Unit.Unit(name)
    unit.node = scene_node
    buildUnit(unit,unittype,"Human",level,player.name)
    
    if not mesh:
        mesh = unit.job.mesh
    if not material:
        material = unit.job.material
    
    attachMe = sceneManager.createEntity(name,mesh)
        
    scene_node.attachObject(attachMe)
    unit.node.getAttachedObject(0).setMaterialName(material)
    setupExtra(unit, mental)
    return unit

def showUnit(unit, position):
    #we want to override any saved players with the current player
    if s.playermap.has_key(unit.player.name) and not unit in s.playermap[unit.player.name].unitlist :
        player = s.playermap[unit.player.name]        
        player.addToUnitlist(unit)
        unit.player = player
    
    sceneManager = s.app.sceneManager
    name = unit.name
    
    prevhad = False
    if sceneManager.hasSceneNode(name):
        scene_node = sceneManager.getSceneNode(name)
        prevhad = True
    else:
        scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
    scene_node.position = position
    if not prevhad:
        if s.app.sceneManager.hasEntity(name):
            attachMe = s.app.sceneManager.getEntity(name)
        else:
            attachMe = sceneManager.createEntity(name, unit.job.mesh)
        scene_node.attachObject(attachMe)
    scene_node.setScale(Ogre.Vector3(1, .5, 1))
    
    unit.node = scene_node
    
    if not prevhad:
        tactics.util.buildPhysics(unit)
    #s.unitmap[unit.getName()]=unit
    unit.node.getAttachedObject(0).setMaterialName(unit.job.material)
    #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
    if hasattr(unit.player, "setVisualMarker"):
        unit.player.setVisualMarker(unit)
        
def showBuilding(building, position):
    
    sceneManager = s.app.sceneManager
    name = building.name
    
    prevhad = False
    if sceneManager.hasSceneNode(name):
        scene_node = sceneManager.getSceneNode(name)
        prevhad = True
    else:
        scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
    scene_node.position = position
    if not prevhad:
        if s.app.sceneManager.hasEntity(name):
            attachMe = s.app.sceneManager.getEntity(name)
        else:
            attachMe = sceneManager.createEntity(name, building.mesh)
        scene_node.attachObject(attachMe)
    scene_node.setScale(Ogre.Vector3(1, 1, 1))
    
    building.node = scene_node
    
#    if not prevhad:
#        tactics.util.buildPhysics(building)
    #s.buildingmap[building.getName()]=building
    #building.node.getAttachedObject(0).setMaterialName(building.job.material)
    #building.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
    

