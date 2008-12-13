import ogre.renderer.OGRE as Ogre
from tactics.Singleton import *
from math import *
import tactics.Unit
class FollowCamera():
    def __init__(self, unit) : 
        self.mDist = 10
        self.mYaw = Ogre.Radian(0, 0)
        self.mPitch = Ogre.Radian(0, 0)
        self.mJustFollowHeight = 0
        self.mMaxDelta = .1
        self.mJustFollow = True 
        self.mCamera = s.app.msnCam
        self.mGoalNode =unit.node
        self.mLookNode = None 
        self.mLookVec = Ogre.Vector3.ZERO
        self.returned = True
        
        self.unit1 = tactics.Unit.Unit()
        self.name = unit.node.getName()

         
    def execute(self, deltat ):
        if self.returned:
            if hasattr(s, "followcamera") and self != s.followcamera:
                s.followcamera.returned = False        
            s.followcamera = self
        # if no goal node is assigned, we can`t move.
        if not self.mGoalNode or not s.app.sceneManager.hasSceneNode(self.name):
            return
    
        mypos = self.mCamera.getPosition()
    
        goalpos = self.mGoalNode._getDerivedPosition()
    
        #first get the Y offset and the XZ plane offset from the pitch angle.

        y = sin( self.mPitch.valueRadians() ) * self.mDist
        xz = cos( self.mPitch.valueRadians() ) * self.mDist
    
        # now get the x any z values from the Yaw angle.
        x = sin( self.mYaw.valueRadians() ) * xz
        z = cos( self.mYaw.valueRadians() ) * xz
        
    
        if self.mJustFollow:
        
            # in this case, don't worry about the orientation of the GoalNode.
            goalpos += Ogre.Vector3(x,y,z)
        
        else:
        
            #take the orientation of the GoalNode into account!
            orient = self.mGoalNode._getDerivedOrientation()
            
            orient.ToRotationMatrix( mat )
            xdir = mat.GetColumn(0)
    
            xdir.y = 0.0
            xdir.normalise()
    
            mat.FromEulerAnglesXYZ(Ogre.Radian(0), Ogre.Math.ATan2(-xdir.z, xdir.x), Ogre.Radian(0) )
    
            orient.FromRotationMatrix( mat )
            goalpos += (orient * Ogre.Vector3(x,y,z))
        
    
        
        # move toward the goal position!
        if deltat > self.mMaxDelta:
            deltat = self.mMaxDelta
    
        togoal = (goalpos - mypos).normalisedCopy() * (goalpos - mypos).length() * 10 * deltat
        if togoal.squaredLength() > (goalpos - mypos).squaredLength():
            togoal = (goalpos - mypos)
    
        mypos += togoal
    
        if mypos.y < -3.5 :
            mypos.y = -3.5 
        
        
        s.app.msnCam.setPosition(mypos)
        #s.app.msnCam.translate(mypos - )
        #self.mGoalNode = None
        #return
        print mypos
        #print s.app.msnCam.getPosition()
        #print s.app.camera.getPosition()
    
#        if self.mLookNode:
#            goallook = self.mLookNode._getDerivedPosition()
#        else:
#            goallook = self.mGoalNode._getDerivedPosition()
    
#        tolook = (goallook - self.mLookVec) * (10*deltat)
    
#        self.mLookVec += tolook
    
        #s.app.camera.lookAt( self.mLookVec )
    
        return self.returned