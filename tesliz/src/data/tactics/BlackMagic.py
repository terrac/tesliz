from tactics.util import *
import utilities.SampleFramework as sf
from math import *
from tactics.Singleton import *
import ogre.renderer.OGRE as ogre

s = Singleton()
class Fireball(object):
    def __init__ ( self,unit1 = None,unit2= None):
         self.unit1 = unit1
         self.unit2 = unit2
         
    unit1 = None
    unit2 = None     

    
    def setUnitAndPosition(self,unit2,position):
        self.unit2 = unit2
        if not self.unit2:            
            return False
        return True
    
    def execute(self):
        World = s.app.World
        sceneManager = s.app.sceneManager
        
        direction = self.unit2.body.getOgreNode().getPosition() - self.unit1.body.getOgreNode().getPosition()
        
        name = s.app.getUniqueName()
        
        node = sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
                        
        node.setPosition(0.0, 0.0, 0.0)
        fountainNode = sceneManager.getRootSceneNode().createChildSceneNode()
        psm = ogre.ParticleSystemManager.getSingleton()
        particleSystem2 = sceneManager.createParticleSystem('fountain'+s.app.getUniqueName(), 'RedTorch')
        node = fountainNode.createChildSceneNode()
        node.attachObject(particleSystem2)

        ## again, make the collision shape.
        ##col = OgreNewt.CollisionPrimitives.Cylinder(self.World, 1, 1)
        col = OgreNewt.Cylinder(World, 1, 1)
        
        ## then make the rigid body.    ## need to keep it around see below.......
        body = OgreNewt.Body( World, col)

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
        body.setPositionOrientation( self.unit1.body.getOgreNode().getPosition(), self.unit1.body.getOgreNode().getOrientation() )
        body.setVelocity( (direction * 50.0) )
        
        ## note that we have to keep the bodies around :)
        s.app.bodies.append(body)
        
        
    
        #create cylinder
        #add lighting for fire
        #set velocity
        #self.unit2.body.setVelocity(direction )
        
        return False
             
        #self.node.translate(  direction* (1))
