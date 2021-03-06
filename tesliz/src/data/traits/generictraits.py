
import tactics.Material
import utilities.SampleFramework as sf
import math
from tactics.Singleton import *
import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt
import utilities.physics 
import data.util 
import data.damage
import basictraits 
s = Singleton()


    
    #scene_node.rotate(Ogre.Quaternion(Ogre.Degree(90), Ogre.Vector3.UNIT_Z))
    

class ObjectCallback ( OgreNewt.ContactCallback ):

    def __init__ ( self, typeID ) :
        OgreNewt.ContactCallback.__init__(self) 
        self.typeID = typeID
        self.hit = False
    
    def userProcess(self):
        unit1body = None
        
        ## first, find which body represents the Object unit1body!
        if (self.m_body0.getType() == self.typeID):
            unit1body = self.m_body0
            object = self.m_body1
    
        if (self.m_body1.getType() == self.typeID):
            unit1body = self.m_body1
            object = self.m_body0
            
        if not unit1body:
            return 0

        
        if object.getOgreNode() and s.unitmap.has_key(object.getOgreNode().getName()):
            attack = unit1body.getUserData()
             #s.screenshot()
            attack.onContact(object.getOgreNode().getName())
            
            unit1body.setVelocity(Ogre.Vector3(0,0,0))
            object.setVelocity(Ogre.Vector3(0,0,0))
            unit1body.freeze()
            object.freeze()
            
        ## okay, found the unit1body... let's adjust the collision based on this.
        #thedir = unit1body.getGlobalDir()
        
        #self.rotateTangentDirections( thedir )
        #result_accel = (thedir * unit1body.Speed) - object.getVelocity()
        
        #self.setContactTangentAcceleration( result_accel.length(), 0 )

        return 1


class ProjectileAttack(object):
    
    def __init__(self):
        self.particlename = 'RedTorch'
        self.name="Fireball"
        self.value=10     
        self.range = 10
        self.type = "fire"
        self.unit2 = None
        self.timeleft = 3
        self.needsasecondclick = True
        self.sound = "fireball.wav"
   
#    def ready(self):
#        dis = distance(self.endPos, self.unit1.body.getOgreNode().getPosition())
#        if dis > self.range:
#            return False
#        return True
   
    def execute(self,timer):
        
        
    	if not self.unit1 or  not self.unit1.body or  not self.endPos:
    		return
        
#        if distance(self.endPos, self.unit1.body.getOgreNode().getPosition()) > self.range:
#            s.log(str(self.unit1)+" Attack failed")
#            return
        vector1 = self.unit1.body.getOgreNode().getPosition()
        if self.unit2 and self.unit2.body:
            vector2 = self.unit2.body.getOgreNode().getPosition()
        else:
            self.endPos.y = vector1.y
            vector2 = self.endPos    
        World = s.app.World
        sceneManager = s.app.sceneManager

        self.damage = self.unit1.attributes.intelligence
        
        vector1.y += 5
        direction = vector2 - vector1
        #direction.normalise()
        #vector1 = vector1 +direction * 2
        
        name = s.app.getUniqueName()
        
        node = sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
                        
        node.setPosition(0.0, 0.0, 0.0)
        
        psm = Ogre.ParticleSystemManager.getSingleton()

        particleSystem2 = sceneManager.createParticleSystem('fountain'+s.app.getUniqueName(), self.particlename)        
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
        
    
        material =Material(name,ObjectCallback( 2))
        
        body.setMaterialGroupID( material.MatObject )
        body.setType(2)
        body.setUserData(self)
        
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
        s.framelistener.addTimed(5,node,body,self)
        
   
        s.framelistener.timer = 2
        s.playsound(self.sound)
        return False
             
   


class JumpAttack(object):
    def __init__ ( self,unit1 = None,unit2= None):
        self.lastlen = None
        self.init = False
    name= "JumpAttack"
        
    value = 10   
    
    def ready(self):
        return self.unit2
    
    def execute(self, timer):
        if not self.unit2.body or not self.unit1.body:
            return
#        if self.init:
#            if s.app.ObjectCallback.hit or self.unit1.body.getVelocity().length() == self.lastlen:
#                return False
#            if not s.app.ObjectCallback.hit :
#                self.lastlen=self.unit1.body.getVelocity().length()
#                s.framelistener.timer = .2
#                
#                return True
#        self.init = True
#        s.app.ObjectCallback.hit = False
        World = s.app.World
        sceneManager = s.app.sceneManager

        vector1 = self.unit1.body.getOgreNode().getPosition()
     #   vector1.y += 5
        vector2 = self.unit2.body.getOgreNode().getPosition()
        direction = vector2 - vector1
        direction.normalise()
        
        name = s.app.getUniqueName()
        body = self.unit1.body
        
        World = s.app.World
        sceneManager = s.app.sceneManager
        material =Material(name,ObjectCallback( 1 ))
        
        body.setMaterialGroupID( material.MatObject )
        body.setType(1)
        
        body.setUserData(self.unit1.attributes.strength)
        
        quat = Ogre.Quaternion(Ogre.Degree(45),Ogre.Vector3(0,1,0))
        body.setPositionOrientation(vector1,quat)
        velocity = sqrt(distance(vector1,vector2)* 9.8 / sin(2.0 * 45.0 * pi/180.0))
        velocity = velocity *.75
        s.log(str(direction)+" "+str(velocity)+" "+str(vector1))
        body.setVelocity(((quat *Ogre.Vector3(0,1,0))+ direction) *velocity)
        
         

        
        
        ## note that we have to keep the bodies around :)
        
        
        s.framelistener.timer = 5
        self.unit1.player.endTurn()
        s.playsound()
        return False
             
     
class DoubleAttack(basictraits.Attack):
    def __init__(self):
        
        self.times = 2
        self.time = 2
        self.curT = 0
    def execute(self,timer):
        self.curT -= timer
        if self.curT < 0:
            Attack.execute(self,timer)
            self.times -= 1
            self.curT = self.time
        
        return self.times
            
    
class Boost(object):
    def __init__(self,affect,name = "Boost"):
        self.name = name
        self.value= 5     
        self.timeleft = 0
        self.range=0
        self.animation = "LOOP"
        self.affect = affect
        self.type = "music"
    sound = "boost.wav"
    needsasecondclick = False

    def execute(self,timer):
        
     
        #print self.unit1
        if not self.unit1.body:
            return
        
        show (self.unit1)
        
        am = self.unit1.affect
        
        am.add(self.affect)

        
        entity = self.unit1.node.getAttachedObject(0)
        if entity.hasSkeleton():
            animationState = entity.getAnimationState(self.animation)
            animationState.setLoop(False)
            animationState.setEnabled(True)
            s.app.animations.append(animationState)
           
        s.playsound(self.sound)    
        
        return False

#class SummonUnit(object):    


