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
s = Singleton()


    
def buildUnit(unit,unittype,race,level,playername):
    s.unitmap[unit.getName()]=unit
    
    #unit.type = unittype
    
    
    if s.playermap.has_key(playername):
        player = s.playermap[playername]
        player.unitlist.append(unit)
        unit.player = player
        
    else:

        s.playermap[unit.getName()] = player
    setupBasic(unit, level)
    getattr(data.unittypes.Unittypes(), unittype)(unit,level)
    
    unit.node.setScale(s.racemap[race].scale)
    buildPhysics(unit,"Ellipsoid",s.racemap[race].scale)
    tactics.util.resetAttributes(unit)
    tactics.util.setupMaxPoints(unit)
#creates a unit given a specific job
def buildUnitNoNode(name,playername,unittype,level=1):
    unit = tactics.Unit.Unit(name)
    
    #s.unitmap[unit.getName()]=unit
    
    
    if s.playermap.has_key(playername):
        player = s.playermap[playername]
        player.unitlist.append(unit)
        unit.player = player
    setupBasic(unit, level)
    getattr(data.unittypes.Unittypes(), unittype)(unit,level)
    tactics.util.resetAttributes(unit)
    tactics.util.setupMaxPoints(unit)
    return unit
def resetAttributes(unit):
    try:
        hitpoints = unit.attributes.physical.points
        magicpoints = unit.attributes.magical.points
    except:
        hitpoints = 0
        magicpoints = 0
        #if they don't exist yet then ignore 
    setupBasic(unit, unit.level)
    unit.job.changeTo(unit)
    unit.items.setupAll()
    unit.affect.setupAll()
    unit.attributes.physical.points = hitpoints
    unit.attributes.magical.points = magicpoints
def setupMaxPoints(unit):
    unit.attributes.physical.points = unit.attributes.physical.maxpoints
    unit.attributes.magical.points = unit.attributes.magical.maxpoints 
    
def setupBasic(unit, level):
    
    #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
    unit.attributes.moves = 5,5
    move = userinterface.traits.Traits([tactics.Move.FFTMove(unit)])
    move.action = False
    unit.traits["Move"] = move
    attack = userinterface.traits.Traits([data.traits.generictraits.Attack()])
    unit.traits["Attack"] = attack
    unit.level = level
        
    
    
    
    
def buildPhysics(unit,type= None,scale = Ogre.Vector3(1,1,1)):        
    
    col = None

    if type:
    #TODO convex hulls -figure out and do
        col = getattr(OgreNewt, type)(s.app.World,Ogre.Vector3(1,1,1))
    else:    
        col = OgreNewt.Box(s.app.World, Ogre.Vector3(1,3,1))
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
    if hasattr( player, "setVisualMarker"):
        player.setVisualMarker(unit)
   
    if s.fog and player.name == "Computer1":
        unit.setVisible(False)
    
    if not mentalstate:
        mentalstate = mental.mind.Mind([mental.combat.Combat(unit,mental.action.Attack,combat.isWanted)])    
        #mental.state = {"angry":0,"happy":0}
    has = hasattr(unit,"mental")
    if has and not unit.mental or not has:
        unit.mental = mentalstate
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

    