# 
#   OgreNewt library - connecting Ogre and Newton!
#   Demo01_TheBasics - basic demo that shows a simple OgreNewt world, and how
#   to setup basic rigid bodies.
# 

import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt
import ogre.io.OIS as OIS

from tactics.dotscenea import *
from tactics.Turn import *
from tactics.Player import *
from tactics.Move import *
from data.playermap import *
from utilities.BasicFrameListener import *     # a simple frame listener that updates physics as required..
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import ogre.gui.CEGUI as CEGUI
import random

 

class OgreNewtonApplication (sf.Application):
    def __init__ ( self):
        sf.Application.__init__(self)
        self.World = OgreNewt.World()
        self.EntityCount = 0
        self.bodies=[]
        sf.Application.debugText = "Press Space Bar to fire.  ESC to end"

    def __del__ (self):
        ## delete the world when we're done.
        #OgreNewt.Debugger.getSingleton().deInit()
        del self.bodies
        del self.World;
    
        ## de-initialize the debugger.
#        OgreNewt.Debugger.getSingleton().deInit()
        sf.Application.__del__(self)

    
    def _createScene ( self ):
        Turn()
        s = Singleton()
        s.app = self
        s.playermap = Playermap().playermap
        self.GUIRenderer = CEGUI.OgreCEGUIRenderer( self.renderWindow, 
                Ogre.RENDER_QUEUE_OVERLAY, False, 3000, self.sceneManager )
        self.GUIsystem = CEGUI.System( self.GUIRenderer )
        ## load up CEGUI stuff...
        CEGUI.Logger.getSingleton().setLoggingLevel( CEGUI.Informative )
#         CEGUI.SchemeManager.getSingleton().loadScheme("WindowsLook.scheme") #../../Media/GUI/schemes/WindowsLook.scheme")
#         self.GUIsystem.setDefaultMouseCursor("WindowsLook", "MouseArrow")
#         self.GUIsystem.setDefaultFont("Commonwealth-10")
        CEGUI.SchemeManager.getSingleton().loadScheme("TaharezLookSkin.scheme") 
        self.GUIsystem.setDefaultMouseCursor("TaharezLook",  "MouseArrow") 
        self.GUIsystem.setDefaultFont( "BlueHighway-12") 
        
        sheet = CEGUI.WindowManager.getSingleton().createWindow( "DefaultWindow", "root_wnd" )
        CEGUI.System.getSingleton().setGUISheet( sheet )
        ## sky box.
        self.sceneManager.setSkyBox(True, "Examples/CloudyNoonSkyBox")
        dotscene = Dotscene()
        self.sceneManager = dotscene.setup_scene(self.sceneManager, minidom.parse('axis.scene'),self)
        
        winMgr = CEGUI.WindowManager.getSingleton() 
        btn = winMgr.createWindow("TaharezLook/Button", "QuitButton")
        sheet.addChildWindow(btn)
        btn.setText("Quit!")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.035), cegui_reldim( 0.0)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleQuit")
        btn.setAlwaysOnTop(True)
        
        btn = winMgr.createWindow("TaharezLook/Button", "EndTurn")
        sheet.addChildWindow(btn)
        btn.setText("endturn")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.8)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, s.turn, "endTurn")
        btn.setAlwaysOnTop(True)
        s.playerlist = [HumanPlayer(),ComputerPlayer()]
        
        btn = winMgr.createWindow("TaharezLook/Button", "current")
        sheet.addChildWindow(btn)
        btn.setText("current")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.6)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        ## this will be a static object that we can throw objects at.  we'll use a simple cylinder primitive.
        ## first I load the visual mesh that represents it.  I have some simple primitive shaped .mesh files in
        ## the "primitives" directory to make this simple... all of them have a basic size of "1" so that they
        ## can easily be scaled to fit any size primitive.
        floor = self.sceneManager.createEntity("Floor", "cylinder.mesh" )
        floor.setNormaliseNormals(True)
        floornode = self.sceneManager.getRootSceneNode().createChildSceneNode( "FloorNode" )
        floornode.attachObject( floor )
        floor.setMaterialName( "Examples/DarkMaterial" )
        floor.setCastShadows( False )
        
        ## okay, the basic mesh is loaded.  now let's decide the size of the object, and scale the node.
        siz = Ogre.Vector3(50,2.5,2.5)
        floornode.setScale( siz )

             
        ## here's where we make a collision shape for the physics.  note that we use the same size as
        ## above.
        col = OgreNewt.Cylinder(self.World, 2.5, 50)
        #col = OgreNewt.CollisionPrimitives.Cylinder(self.World, 2.5, 5)
    
        ## now we make a new rigid body based on this collision shape.
        body = OgreNewt.Body( self.World, col )
    
        ## we`re done with the collision shape, we can delete it now.
        del col
    
        ## now we "attach" the rigid body to the scene node that holds the visual object, and set it's
        ## original position and orientation.  all rigid bodies default to mass=0 (static, immobile), so
        ## that's all we'll need to do for this object.  dynamic objects have a few more steps, so look
        ## at the code in the FrameListener for more.
        body.attachToNode( floornode )
        body.setPositionOrientation( Ogre.Vector3(0.0,-15.0,0.0), Ogre.Quaternion.IDENTITY )
        
        self.bodies.append(body)
        ## position camera
        
        floor = self.sceneManager.createEntity("Floor1", "simple_terrain.mesh" )
        floornode = self.sceneManager.getRootSceneNode().createChildSceneNode( "FloorNode1" )
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
        self.msnCam = self.sceneManager.getRootSceneNode().createChildSceneNode()
        self.msnCam.attachObject( self.camera )
        self.camera.setPosition(0.0, 0.0, 0.0)
        self.msnCam.setPosition( 0.0, -10.0, 20.0)
    
        ##make a light
        light = self.sceneManager.createLight( "Light1" )
        light.setType( Ogre.Light.LT_POINT )
        light.setPosition( Ogre.Vector3(0.0, 100.0, 100.0) )
       # self.renderWindow.writeContentsToTimestampedFile("screenshot",".jpg")


    def _createFrameListener(self):
        
        ## this is a basic frame listener included with OgreNewt that does nothing but update the
        ## physics at a set framerate for you.  complex project will want more control, but this
        ## works for simple demos like this.  feel free to look at the source to see how it works.
        self.NewtonListener = BasicFrameListener( self.renderWindow, self.sceneManager, self.World, 60 )
        self.root.addFrameListener(self.NewtonListener)
        
        ## this is our custom frame listener for this app, that lets us shoot cylinders with the space bar, move
        ## the camera, etc.
        self.frameListener = OgreNewtonFrameListener( self.renderWindow, self.camera, self.sceneManager, self.World, self.msnCam, self.NewtonListener )
        self.root.addFrameListener(self.frameListener)
        Singleton().framelistener = self.frameListener
    def _configure(self):
        
        cur = self.root.restoreConfig();
        print cur
        #carryOn = self.root.showConfigDialog()
        if not cur:
            cur = self.root.showConfigDialog()
        if cur:    
            self.renderWindow = self.root.initialise(True, "OGRE Render Window")
        
                
        return cur
    def handleQuit(self, e):
        self.frameListener.requestShutdown() 
        return True
    

       
class OgreNewtonFrameListener(GuiFrameListener):
    def __init__(self, renderWindow, camera, Mgr, World, msnCam, NewtonListener):

        sf.FrameListener.__init__(self, renderWindow, camera)
        self.mouselistener = MouseListener ()
        self.Mouse.setEventCallback(self.mouselistener)
        
        #TODO see if cegui keyboard actually works
        OIS.KeyListener.__init__(self)
        self.Keyboard.setEventCallback(self)
        
        self.World = World
        self.msnCam = msnCam
        self.camera= camera
        self.sceneManager = Mgr
        self.timer=0
        self.count=0
        self.bodies=[]
        self.basicframelistener = NewtonListener
        self.Debug = False
        self.ShutdownRequested = False

    #turn = Turn()
    def frameStarted(self, frameEvent):
        ## in this frame listener we control the camera movement, and allow the user to "shoot" cylinders
        ## by pressing the space bar.  first the camera movement...
        #turn.runturns()
        
        for iexecute in self.runningexecutes:
            boo = iexecute.execute()
            if not boo:
                self.runningexecutes.remove(iexecute)
        
        self.debugText = "aoeu"
        quat = self.msnCam.getOrientation()
    
        vec = Ogre.Vector3(0.0,0.0,-0.5)
        trans = quat * vec
    
        vec = Ogre.Vector3(0.5,0.0,0.0)
        strafe = quat * vec
        
        ##Need to capture/update each device - this will also trigger any listeners
        ## OIS specific !!!!
        self.Keyboard.capture()    
        self.Mouse.capture()
        s.turn.doTurn()
        ## now lets handle mouse input
        ms = self.Mouse.getMouseState()
        if (ms.buttonDown(OIS.MouseButtonID.MB_Left)):
            mouse = CEGUI.MouseCursor.getSingleton().getPosition()
            rend = CEGUI.System.getSingleton().getRenderer()
            mx = mouse.d_x / rend.getWidth()
            my = mouse.d_y / rend.getHeight()
            camray = self.camera.getCameraToViewportRay(mx,my)

            start = camray.getOrigin()
            end = camray.getPoint( 100.0 )

            self.ray = OgreNewt.BasicRaycast( self.World, start, end )  ## should I keep hold of this?
            info = self.ray.getFirstHit()
        
            #dir(info.mBody).OgreNode.Name)
           # print dir(info.mBody)
            position =info.mDistance * info.mNormal + start
            if (info.mBody):
                CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
                self.clickEntity(info.mBody.OgreNode.Name,position)
                
        self.msnCam.pitch( Ogre.Degree(ms.Y.rel * -0.5) )
        self.msnCam.yaw( Ogre.Degree(ms.X.rel * -0.5), Ogre.Node.TS_WORLD )

        ##and Keyboard
        if (self.Keyboard.isKeyDown(OIS.KC_UP)):
            self.msnCam.translate(trans);
        if (self.Keyboard.isKeyDown(OIS.KC_DOWN)):
            self.msnCam.translate(trans * -1.0);
        if (self.Keyboard.isKeyDown(OIS.KC_LEFT)):
            self.msnCam.translate(strafe * -1.0);
        if (self.Keyboard.isKeyDown(OIS.KC_RIGHT)):
            self.msnCam.translate(strafe);
        ## now "shoot" an object!
        if (self.Keyboard.isKeyDown(OIS.KC_SPACE)):
            if (self.timer <= 0.0):

                ## we get the position and direction from the camera...
                camorient = self.msnCam.getWorldOrientation()
                vec = Ogre.Vector3(0,0,-1)
                direct = camorient * vec
    
                ## then make the visual object (again a cylinder)
                #pos = Ogre.Vector3(self.msnCam.getWorldPosition())
                pos = self.msnCam.getWorldPosition()
    
                name = "Body"+str( self.count )
                self.count += 1
    
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
        self.timer -= frameEvent.timeSinceLastFrame
        if (self.Keyboard.isKeyDown(OIS.KC_F3)):
            if self.Debug:
                self.Debug = False
            else:
                self.Debug = True
            self.basicframelistener.debug ( self.Debug )
            
        if (self.Keyboard.isKeyDown(OIS.KC_ESCAPE)):
            ##OgreNewt.Debugger.getSingleton().deInit()
            return False
        return True        
    def clickEntity(self,name,position):
        if self.iexecute:            
            self.iexecute.endPos = position
            self.runningexecutes.append(self.iexecute)
            self.iexecute = None       
    runningexecutes = []
    iexecute=None
            
if __name__ == '__main__':
    try:
        application = OgreNewtonApplication()
        application.go()
    except Ogre.OgreException, e:
        print e
    
    