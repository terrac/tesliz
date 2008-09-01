from tactics.util import *
import utilities.SampleFramework as sf
from math import *

class Fireball(object):
    def __init__ ( self,unit1,unit2= None):
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
        
        
        direction = self.unit2.body.getOgreNode().getPosition() - self.unit1.body.getOgreNode().getPosition()
        
                name = "fireballo"
                ent = self.sceneManager.createEntity( name, "cylinder.mesh" )
                node = self.sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
                node.attachObject( ent )
                                
                node.setPosition(0.0, 0.0, 0.0)
                
                ent.setMaterialName( "Examples/RustySteel" )
                ent.setNormaliseNormals(True)
    
                ## again, make the collision shape.
                ##col = OgreNewt.CollisionPrimitives.Cylinder(self.World, 1, 1)
                col = OgreNewt.Cylinder(self.World, 1, 1)
                
                ## then make the rigid body.    ## need to keep it around see below.......
                body = OgreNewt.Body( self.World, col)
    
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
                body.setPositionOrientation( pos, camorient )
                body.setVelocity( (direct * 50.0) )
                
                ## note that we have to keep the bodies around :)
                self.bodies.append(body)
                
                self.timer = 0.2
    
        #create cylinder
        #add lighting for fire
        #set velocity
        self.unit2.body.setVelocity(direction )
        
        return False
             
        #self.node.translate(  direction* (1))
