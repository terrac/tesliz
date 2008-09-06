from tactics.util import *
import utilities.SampleFramework as sf
from math import *
from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import ogre.physics.OgreNewt as OgreNewt
from utilities.physics import *
s = Singleton()

class ObjectCallback ( OgreNewt.ContactCallback ):

    def __init__ ( self, typeID ) :
        OgreNewt.ContactCallback.__init__(self) 
        self.typeID = typeID
        self.hit = False
    
    def userProcess(self):
        
        
        ## first, find which body represents the Object unit1body!
        if (self.m_body0.getType() == self.typeID):
            unit1body = self.m_body0
            object = self.m_body1
    
        if (self.m_body1.getType() == self.typeID):
            unit1body = self.m_body1
            object = self.m_body0
        if not unit1body:
            return 0
        
        
        if s.unitmap.has_key(object.getOgreNode().getName()):
            s.unitmap[object.getOgreNode().getName()].damageHitpoints(50)
            self.hit = True
            unit1body.setVelocity(Ogre.Vector3(0,0,0))
        ## okay, found the unit1body... let's adjust the collision based on this.
        #thedir = unit1body.getGlobalDir()
        
        #self.rotateTangentDirections( thedir )
        #result_accel = (thedir * unit1body.Speed) - object.getVelocity()
        
        #self.setContactTangentAcceleration( result_accel.length(), 0 )

        return 1

class RangeAttack(object):
    def __init__ ( self,unit1 = None,unit2= None):
        self.unit1 = unit1
        self.unit2 = unit2
        #self.MatDefault = s.app.World.getDefaultMaterialID()
        #self.MatObject = OgreNewt.MaterialID( s.app.World )
        #self.MatPairDefaultObject = OgreNewt.MaterialPair( s.app.World, self.MatDefault, self.MatObject )
         
        #self.ObjectCallback =  ObjectMatCallback( 1 )
         
         
        #self.MatPairDefaultObject.setContactCallback( self.ObjectCallback )
        #self.MatPairDefaultObject.setDefaultFriction( 1.5, 1.4 )        
        

    def set(self,unit1 = None,unit2= None):     
        self.unit1 = unit1
        self.unit2 = unit2
    def getName(self):
        return "Fireball"
        
    def overallValue(self):
        return 10             
    unit1 = None
    unit2 = None     

    
    def setUnitAndPosition(self,unit2,position):
        self.unit2 = unit2
        
        
        if not self.unit2:            
            return False
        return True
    
    
    def execute(self,timer):
    	if not self.unit2.body or not self.unit1.body:
    		return
    
        World = s.app.World
        sceneManager = s.app.sceneManager

        vector1 = self.unit1.body.getOgreNode().getPosition()
        vector1.y += 5
        direction = self.unit2.body.getOgreNode().getPosition() - vector1
        
        name = s.app.getUniqueName()
        
        node = sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
                        
        node.setPosition(0.0, 0.0, 0.0)
        
        psm = ogre.ParticleSystemManager.getSingleton()
        particleSystem2 = sceneManager.createParticleSystem('fountain'+s.app.getUniqueName(), 'RedTorch')        
        node.attachObject(particleSystem2)
        
        
        light = s.app.sceneManager.createLight( name )
        light.setType( Ogre.Light.LT_POINT )
        dir(light)
#        light.setDiffuseColor(255,0,0)
        light.DiffuseColor = 255,0,0
        light.SpecularColor = 255,0,0
#        light.setSpecularColor(255,0,0)
        node.attachObject(light)

        ## again, make the collision shape.
        ##col = OgreNewt.CollisionPrimitives.Cylinder(World, 1, 1)
        col = OgreNewt.Cylinder(World, 1, 1)
        
        ## then make the rigid body.    ## need to keep it around see below.......
        body = OgreNewt.Body( World, col)
        #body.setMaterialGroupID( s.app.MatObject )
        body.setMaterialGroupID( s.app.MatObject )
        body.setType(1)
        ##no longer need the collision shape object
        del col

        ## something new: moment of inertia for the body.  this describes how much the body "resists"
        ## rotation on each axis.  realistic values here make for MUCH more realistic results.  luckily
        ## OgreNewt has some helper functions for calculating these values for many primitive shapes!
        inertia = OgreNewt.CalcSphereSolid( 10.0, 1.0 )
        body.setMassMatrix( 10.0, inertia )

        ## attach to the scene node.
        body.attachToNode( node )

        ## this is a standard callback that simply add a gravitational force (-9.8*mass) to the body.
        body.setStandardForceCallback()

        ## set the initial orientation and velocity!
        
        body.setPositionOrientation( vector1, self.unit1.body.getOgreNode().getOrientation() )
        body.setVelocity( (direction * 5.0) )
        
        ## note that we have to keep the bodies around :)
        s.framelistener.addTimedBody(body,5)
        
   
        
        self.unit1.player.endTurn()
        return False
             
   


class JumpAttack(object):
    def __init__ ( self,unit1 = None,unit2= None):
        self.unit1 = unit1
        self.unit2 = unit2
        self.lastlen = None

    def set(self,unit1 = None,unit2= None):     
        self.unit1 = unit1
        self.unit2 = unit2
        self.init = False
    def getName(self):
        return "JumpAttack"
        
    def overallValue(self):
        return 10             
    unit1 = None
    unit2 = None     

    
    def setUnitAndPosition(self,unit2,position):
        self.unit2 = unit2
        
        
        if not self.unit2:            
            return False
        return True
    
    
    def execute(self, timer):
        if not self.unit2.body or not self.unit1.body:
            return
        if self.init:
            if s.app.ObjectCallback.hit or self.unit1.body.getVelocity().length() == self.lastlen:
                return False
            if not s.app.ObjectCallback.hit :
                self.lastlen=self.unit1.body.getVelocity().length()
                #s.screenshot()
                name = s.app.getUniqueName()
            
                node = s.app.sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
                                
                node.setPosition(self.unit1.node.getPosition())
                
                psm = ogre.ParticleSystemManager.getSingleton()
                particleSystem2 = s.app.sceneManager.createParticleSystem('fountain'+s.app.getUniqueName(), 'RedTorch')
                print str(self.unit1.node.getPosition()) + str(self.unit1.body.getVelocity().length())        
                node.attachObject(particleSystem2)
                s.framelistener.timer = .2
                
                return True
        self.init = True
        s.app.ObjectCallback.hit = False
        World = s.app.World
        sceneManager = s.app.sceneManager

        vector1 = self.unit1.body.getOgreNode().getPosition()
     #   vector1.y += 5
        vector2 = self.unit2.body.getOgreNode().getPosition()
        direction = vector2 - vector1
        direction.normalise()
        
        name = s.app.getUniqueName()
        body = self.unit1.body
        body.setMaterialGroupID( s.app.MatObject )
        body.setType(1)
 
        
        quat = Ogre.Quaternion(Ogre.Degree(45),Ogre.Vector3(0,1,0))
        body.setPositionOrientation(vector1,quat)
        velocity = sqrt(distance(vector1,vector2)* 9.8 / sin(2.0 * 45.0 * pi/180.0))
        velocity = velocity *.75
        s.log(str(direction)+" "+str(velocity)+" "+str(vector1))
        body.setVelocity(((quat *Ogre.Vector3(0,1,0))+ direction) *velocity)
        
         

        
        
        ## note that we have to keep the bodies around :)
        
        
        s.framelistener.timer = 5
        self.unit1.player.endTurn()
        return True
             
     
