
# 
#   OgreNewt library - connecting Ogre and Newton!
#   Demo01_TheBasics - basic demo that shows a simple OgreNewt world, and how
#   to setup basic rigid bodies.
# 

import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt
import ogre.io.OIS as OIS
from utilities.physics import *
from tactics.dotscenea import *
from tactics.Turn import *
from tactics.Player import *
from tactics.Move import *
from data.settings import *
from utilities.BasicFrameListener import *     # a simple frame listener that updates physics as required..
from utilities.CEGUIFrameListener import *
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import ogre.gui.CEGUI as CEGUI
import random
 
s = Singleton()
class OgreNewtonApplication (sf.Application):
    
    currentmap=None
    def __init__ ( self):
        sf.Application.__init__(self)
        self.World = OgreNewt.World()
        
        self.EntityCount = 0
        self.bodies=[]
        self.timedbodies = []
        sf.Application.debugText = "aeou"

    def __del__ (self):
        ## delete the world when we're done.
        #OgreNewt.Debugger.getSingleton().deInit()
        del self.bodies
        del self.World;
    
        ## de-initialize the debugger.
#        OgreNewt.Debugger.getSingleton().deInit()
        sf.Application.__del__(self)

    
    def _createScene ( self ):
        s.app = self
        s.playermap = Settings().playermap
        if s.turnbased:
            Turn()
        else:
            RealTimeTurn()
        
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
        #self.sceneManager.setSkyBox(True, "Examples/CloudyNoonSkyBox")
        dotscene = Dotscene()
        self.sceneManager = dotscene.setup_scene(self.sceneManager,self.currentmap,self)
        
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
        self.msnCam = self.sceneManager.getRootSceneNode().createChildSceneNode()
        self.msnCam.attachObject( self.camera )
        self.camera.setPosition(0.0, 0.0, 0.0)
        self.msnCam.setPosition( 0.0, -10.0, 20.0)
    
        ##make a light
        #light = self.sceneManager.createLight( "Light1" )
        #light.setType( Ogre.Light.LT_POINT )
        #light.setPosition( Ogre.Vector3(0.0, 100.0, 100.0) )
        
        World = s.app.World
        sceneManager = s.app.sceneManager
        s.app.MatDefault = World.getDefaultMaterialID()
        s.app.MatObject = OgreNewt.MaterialID( World )
        s.app.MatPairDefaultObject = OgreNewt.MaterialPair( World, s.app.MatDefault, s.app.MatObject )
        s.app.ObjectCallback = ObjectCallback( 1 )
        s.app.MatPairDefaultObject.setContactCallback( s.app.ObjectCallback )
        s.app.MatPairDefaultObject.setDefaultFriction( 1.5, 1.4 )
       


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
    def getUniqueName(self):
        self.count+= 1
        
        return "unique"+str(self.count)
    count = 0;

       
class OgreNewtonFrameListener(CEGUIFrameListener):
    def __init__(self, renderWindow, camera, Mgr, World, msnCam, NewtonListener):

        CEGUIFrameListener.__init__(self, renderWindow, camera)
        #self.mouselistener = MouseListener ()
        #self.Mouse.setEventCallback(self.mouselistener)
        
        #TODO see if cegui keyboard actually works
        #OIS.KeyListener.__init__(self)
        #self.Keyboard.setEventCallback(self)
        
        self.World = World
        self.msnCam = msnCam
        self.camera= camera
        self.sceneManager = Mgr
        self.timer=1
        self.count=0
        self.bodies=[]
        self.basicframelistener = NewtonListener
        self.Debug = False
        self.ShutdownRequested = False

    def addTimedBody(self, body,seconds):
        x = body,seconds
        s.app.timedbodies.append(x)

    #then you can have both
    def addToQueue(self, unit,action):
        try:
            dist =distance(action.unit2.node.getPosition(),action.unit1.node.getPosition())
#            mindis = None
            try:
                mindis = action.minimumDistance
            except :
                mindis = 0
#            maxdis 
            try:
                maxdis = action.maximumDistance
            except:
                maxdis = 0            
            
            
            if mindis > 0:
                if mindis > dist:
                    return False
            if maxdis > 0:
                if maxdis < dist:
                    return False    
        except Exception, e:
            print e
        unit.actionqueue.append(action)
        self.unitqueues.append(unit)
    unitqueues = []   
    #turn = Turn()
    def frameStarted(self, frameEvent):
        ## in this frame listener we control the camera movement, and allow the user to "shoot" cylinders
        ## by pressing the space bar.  first the camera movement...
        #turn.runturns()
        
                    
#        if s.ended:
#            return 
        
        #todo somewhat inefficient
        list = []
        while len(s.app.timedbodies) > 0:
            body, time = s.app.timedbodies.pop()
            time -= frameEvent.timeSinceLastFrame
            tuple = body,time
            #print tuple
            if time > 0:
               list.append(tuple) 
            else:
                s.app.sceneManager.getRootSceneNode().removeChild(body.getOgreNode())
                   
        s.app.timedbodies = list
                   
                     
        quat = self.msnCam.getOrientation()
    
        vec = Ogre.Vector3(0.0,0.0,-0.5)
        trans = quat * vec
    
        vec = Ogre.Vector3(0.5,0.0,0.0)
        strafe = quat * vec
        
        ##Need to capture/update each device - this will also trigger any listeners
        ## OIS specific !!!!
        self.Keyboard.capture()    
        self.Mouse.capture()

        ## now lets handle mouse input
        ms = self.Mouse.getMouseState()
   
        if (self.Keyboard.isKeyDown(OIS.KC_LSHIFT)):        
            rend = CEGUI.System.getSingleton().getRenderer()
            mouse = CEGUI.Point(rend.getWidth() / 2.0, rend.getHeight() / 2.0)
            self.msnCam.pitch( Ogre.Degree(ms.Y.rel * -0.5) )
            self.msnCam.yaw( Ogre.Degree(ms.X.rel * -0.5), Ogre.Node.TS_WORLD )
            CEGUI.MouseCursor.getSingleton().setPosition(mouse)
            sf.Application.debugText = str(self.msnCam.getPosition())
        ##and Keyboard
        if (self.Keyboard.isKeyDown(OIS.KC_UP) or self.Keyboard.isKeyDown(OIS.KC_W)):
            self.msnCam.translate(trans * 0.1);
        if (self.Keyboard.isKeyDown(OIS.KC_DOWN) or self.Keyboard.isKeyDown(OIS.KC_S)):
            self.msnCam.translate(trans * -0.1);
        if (self.Keyboard.isKeyDown(OIS.KC_LEFT) or self.Keyboard.isKeyDown(OIS.KC_A)):
            self.msnCam.translate(strafe * -0.1);
        if (self.Keyboard.isKeyDown(OIS.KC_RIGHT) or self.Keyboard.isKeyDown(OIS.KC_D)):
            self.msnCam.translate(strafe * 0.1);
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
    
                #ent = self.sceneManager.createEntity( name, "cylinder.mesh" )
                node = self.sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
                #node.attachObject( ent )
                
                node.setPosition(0.0, 0.0, 0.0)
                
                self.fountainNode = self.sceneManager.getRootSceneNode().createChildSceneNode()
                psm = ogre.ParticleSystemManager.getSingleton()
                particleSystem2 = self.sceneManager.createParticleSystem('fountain'+str(self.count), 'RedTorch')
                node = self.fountainNode.createChildSceneNode()
                node.attachObject(particleSystem2)
                #ent.setMaterialName( "Examples/RustySteel" )
                #ent.setNormaliseNormals(True)
             #   self.MatDefault = self.World.getDefaultMaterialID()
             #   self.MatConveyor = OgreNewt.MaterialID( self.World )
    
             #   self.MatPairDefaultConveyor = OgreNewt.MaterialPair( self.World, self.MatDefault, self.MatConveyor )
             #   self.ConveyorCallback = conveyorMatCallback( 1 )
             #   self.MatPairDefaultConveyor.setContactCallback( self.ConveyorCallback )
             #   self.MatPairDefaultConveyor.setDefaultFriction( 1.5, 1.4 )
                ## again, make the collision shape.
                ##col = OgreNewt.CollisionPrimitives.Cylinder(self.World, 1, 1)
                col = OgreNewt.Cylinder(self.World, 1, 1)
                
                ## then make the rigid body.    ## need to keep it around see below.......
                body = OgreNewt.Body( self.World, col)
              #  body.setMaterialGroupID( self.MatConveyor )
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
        if (self.timer > 0.0):
            return True

        s.turn.doTurn()        
        for unit in self.unitqueues:
            if len(unit.actionqueue) == 0:
                self.unitqueues.remove(unit)
            for iexecute in unit.actionqueue:
                boo = iexecute.execute(frameEvent.timeSinceLastFrame)
                if not boo:
                    unit.actionqueue.remove(iexecute)
                    
                break
            if s.turnbased :   
                    break

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
        if self.cplayer:
            self.cplayer.clickEntity(name,position)            
    oncegui = False       
    #runningexecutes = []
    cplayer = None
    def mousePressed(self, evt, id):
        if CEGUIFrameListener.mousePressed(self,evt,id):
            return
                                             
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
        #position =info.mDistance * info.mNormal + start
        
    
        if (info.mBody):
            
            bodpos, bodorient = info.mBody.getPositionOrientation()
            globalpt = camray.getPoint( 100.0 * info.mDistance )
            position = bodorient.Inverse() * (globalpt - bodpos)
            CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
            self.clickEntity(info.mBody.OgreNode.Name,position)
if __name__ == '__main__':
    try:
        application = OgreNewtonApplication()
        application.go()
    except Ogre.OgreException, e:
        print e
#    except:
#        import sys
#        sys.exc_info()

    