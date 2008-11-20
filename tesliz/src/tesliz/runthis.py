
# 
#   OgreNewt library - connecting Ogre and Newton!i
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
from data.aisettings import *
from utilities.BasicFrameListener import *     # a simple frame listener that updates physics as required..
from utilities.CEGUIFrameListener import *
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import ogre.gui.CEGUI as CEGUI
import random
import utilities.Console
from tactics.OverviewMap import *
 
s = Singleton()
class OgreNewtonApplication (sf.Application):
    
    currentmap=None
    def __init__ ( self,onStartup = None):
        sf.Application.__init__(self)
        self.World = OgreNewt.World()
        
        self.EntityCount = 0
        self.bodies=[]
        self.timedbodies = []
        self.animations = []
        self.materialmap=dict()
        sf.Application.debugText = "aeou"
        s.app = self
        if not onStartup:
            self.onStartup = lambda : False
        else:
            self.onStartup = onStartup
        # This is for the job list, temporary until refactored to it's own class
        self.ListItems = []

    def parseSceneFile(self,map):
        dotscene = Dotscene()
        self.sceneManager = dotscene.setup_scene(self.sceneManager, map, self)



    def __del__ (self):
        ## delete the world when we're done.
        #OgreNewt.Debugger.getSingleton().deInit()
        del self.bodies
        del self.World;
    
        ## de-initialize the debugger.
#        OgreNewt.Debugger.getSingleton().deInit()
        sf.Application.__del__(self)

    
    def _createScene ( self ):
          
        # Create all the CEGUI stuff
        self.initCEGUIStuff()
        
        # Create the Main Window
        self.startMenu()
        
        #self.loadScene()
        Settings()
        
        
        camera = s.app.sceneManager.createCamera("Camera")
        s.app.msnCam = s.app.sceneManager.getRootSceneNode().createChildSceneNode()
        s.app.msnCam.attachObject( s.app.camera )
        s.app.camera.setPosition(0.0, 0.0, 0.0)
        s.app.msnCam.setPosition( Ogre.Vector3(0,25,0))
        
        s.app.msnCam.setOrientation(Ogre.Quaternion(0.793987, -0.472373, 0.32888, 0.195663))
      #  "0.481707" y="0.212922" z="0.334251" w="0.781600"/>
        ## sky box.
        

        self.createFrame()
        s.overviewmap =overviewmap = OverviewMap("Terra.player")
        btn = CEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Button", "current")
        CEGUI.System.getSingleton().getGUISheet().addChildWindow(btn)
        btn.setText("current")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.6)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        
        s.framelistener.cplayer = s.overviewmap
        self.onStartup()


    def startMenu(self):
        sheet = CEGUI.System.getSingleton().getGUISheet()
        winMgr = CEGUI.WindowManager.getSingleton()
        mainMenuBackground = winMgr.createWindow("TaharezLook/FrameWindow", "Tesliz/MainMenuBackground")
        sheet.addChildWindow(mainMenuBackground)
        mainMenuBackground.setSize(CEGUI.UVector2(CEGUI.UDim(0.25, 0), CEGUI.UDim(0.25, 0)))
        mainMenuBackground.setXPosition(CEGUI.UDim(0, 0))
        mainMenuBackground.setYPosition(CEGUI.UDim(0, 0))
#        mainMenuBackground.setCloseButtonEnabled(false)
        mainMenuBackground.setText("Tesliz Menu Frame")


        startButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/StartButton")
        mainMenuBackground.addChildWindow(startButton)
        startButton.setText("Start Game")
        startButton.setXPosition(CEGUI.UDim(0.375, 0))
        startButton.setYPosition(CEGUI.UDim(0.3, 0))
        startButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        startButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleStartGameFromMenu")
        startButton.setAlwaysOnTop(True)

#        jobButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/JobButton")
#        mainMenuBackground.addChildWindow(jobButton)
#        jobButton.setText("Jobs")
#        jobButton.setXPosition(CEGUI.UDim(0.375, 0))
#        jobButton.setYPosition(CEGUI.UDim(0.5, 0))
#        jobButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
#        jobButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleJobs")
#        jobButton.setAlwaysOnTop(True)

        quitButton = winMgr.createWindow("TaharezLook/Button", "Tesliz/MainMenuBackground/QuitButton")
        mainMenuBackground.addChildWindow(quitButton)
        quitButton.setText("Quit")
        quitButton.setXPosition(CEGUI.UDim(0.375, 0))
        quitButton.setYPosition(CEGUI.UDim(0.7, 0))
#        quitButton.setPosition(CEGUI.UVector2(cegui_reldim(0.035), cegui_reldim( 0.0)))
        quitButton.setSize(CEGUI.UVector2(cegui_reldim(0.25), cegui_reldim( 0.1)))
        quitButton.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleQuitGameFromMenu")
        quitButton.setAlwaysOnTop(True)
        


    def deleteStartMenu(self):
        winMgr = CEGUI.WindowManager.getSingleton()
        winMgr.destroyWindow("Tesliz/MainMenuBackground")

    def initCEGUIStuff(self):
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


    def loadScene(self,scenename):
        data.util.clearMeshes()
        s.app.sceneManager.destroyAllMovableObjects()
        s.app.World.destroyAllBodies()
        # Play Windows exit sound.
        #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        
        # Probably play Windows default sound, if any is registered (because
        # "*" probably isn't the registered name of any sound).

#        if s.turnbased:
#            Turn()
#        else:
#            RealTimeTurn()

       
        
        s.app.camera.initialOrientation = None
        #Settings()
        
        ## sky box.
        #self.sceneManager.setSkyBox(True, "Examples/CloudyNoonSkyBox")
        mental = AIsettings()
        
        self.parseSceneFile(scenename)
        
#        sheet = CEGUI.System.getSingleton().getGUISheet()
#        winMgr = CEGUI.WindowManager.getSingleton() 
#        btn = winMgr.createWindow("TaharezLook/Button", "QuitButton")
#        sheet.addChildWindow(btn)
#        btn.setText("Quit!")
#        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.035), cegui_reldim( 0.0)))
#        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        
 #       btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "handleQuit")
 #       btn.setAlwaysOnTop(True)
        
#        btn = winMgr.createWindow("TaharezLook/Button", "EndTurn")
#        sheet.addChildWindow(btn)
#        btn.setText("endturn")
#        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.8)))
#        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        
#        btn.subscribeEvent(CEGUI.PushButton.EventClicked, s.turn, "endTurn")
#        btn.setAlwaysOnTop(True)
        #s.playerlist = [HumanPlayer(),ComputerPlayer()]
        

        ## this will be a static object that we can throw objects at.  we'll use a simple cylinder primitive.
        ## first I load the visual mesh that represents it.  I have some simple primitive shaped .mesh files in
        ## the "primitives" directory to make this simple... all of them have a basic size of "1" so that they
        ## can easily be scaled to fit any size primitive.
    def _createFrameListener(self):
        pass
    def createFrame(self):
        
        self.Console = utilities.Console.Console(self.root)
        print "blah"
        self.Console.addLocals({'s':s})

        #self.Console.show()
        ## this is a basic frame listener included with OgreNewt that does nothing but update the
        ## physics at a set framerate for you.  complex project will want more control, but this
        ## works for simple demos like this.  feel free to look at the source to see how it works.
        self.NewtonListener = BasicFrameListener( self.renderWindow, self.sceneManager, self.World, 60 )
        self.root.addFrameListener(self.NewtonListener)

#        self.frameListener = CEGUIFrameListener(self.renderWindow, self.camera)
#        self.root.addFrameListener(self.frameListener)
        #self.frameListener.showDebugOverlay(False)
        ## this is our custom frame listener for this app, that lets us shoot cylinders with the space bar, move
        ## the camera, etc.
        self.frameListener = OgreNewtonFrameListener( self.renderWindow, self.camera, self.sceneManager, self.World, self.msnCam, self.NewtonListener )
        self.root.addFrameListener(self.frameListener)

        #self.frameListener.showDebugOverlay(False)
        s.framelistener = self.frameListener
        

        
       # self.handleStartGameFromMenu(None)
    def _configure(self):
        
        cur = self.root.restoreConfig();
        
        #carryOn = self.root.showConfigDialog()
        if not cur:
            cur = self.root.showConfigDialog()
        if cur:    
            self.renderWindow = self.root.initialise(True, "OGRE Render Window")
        
                
        return cur
    
    def handleStartGameFromMenu(self, e):
        # Remove the menu
        self.deleteStartMenu()
        self.loadScene("scene01")
        
    def handleQuitGameFromMenu(self, e):
        self.handleQuit(e)
        
    def handleQuit(self, e):
        #self.frameListener.cont = False
        #self.frameListener.requestShutdown()
        return True
    def getUniqueName(self):
        self.count+= 1
        
        return "unique"+str(self.count)
    count = 0;
    def setTurnbased(self,bool):
            s.turnbased = bool
            if bool:
                s.turn = Turn()
                s.AIon = False
            else:
                s.turn = RealTimeTurn()
                s.AIon = True
            s.log("turnbased = " +str(s.turnbased))

       
class Timed():
    def __init__(self,seconds,node,body):
        self.seconds = seconds
        self.node = node
        self.body = body
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
        self.paused = False

    def addTimed(self, seconds,node,*extra):
        x = Timed(seconds,node,extra)
        s.app.timedbodies.append(x)

    #then you can have both
    def addToQueue(self, unit,action):

        action.running = True
        unit.actionqueue.append(action)
        if not unit in self.unitqueues:
            self.unitqueues.append(unit)

         
    unitqueues = []   
    def getActiveQueue(self):
        return len(self.unitqueues)

    def clearActions(self,unit):
        if self.unitqueues.contains(unit):
            self.unitqueues.remove(unit)
        
        unit.actionqueue = []
        
            
    def isActive(self,unit):
        
        if len( unit.actionqueue):
            return True
        
                  
        return False
    a =       0
    def runQueue(self,timer):
        self.a += timer
        for unit in self.unitqueues:
            
            
            if unit.timeleft > 0:
                unit.timeleft -= timer
                continue
           
            
            if len(unit.actionqueue) == 0:
                self.unitqueues.remove(unit)
                continue
            iexecute = unit.actionqueue[0]
            boo = False
           
            boo = iexecute.execute(timer)
            
            if not boo:
                unit.actionqueue.pop(0)
                if hasattr(iexecute, "timeleft"):
                    
                    unit.timeleft = iexecute.timeleft
                    unit.timeleft += random.random()*.1
                    
               
                
                    
                    
                
            
            if s.turnbased :   
                break    
    #turn = Turn()
    def frameStarted(self, frameEvent):
    
        ## in this frame listener we control the camera movement, and allow the user to "shoot" cylinders
        ## by pressing the space bar.  first the camera movement...
        #turn.runturns()
              
#        if s.ended:
#            return 

        for u in s.unitmap.values():
            if u.text:
                u.text.update()
        for u in s.unitmap.values():
            if u.node and u.node.getPosition().y < -100:
                s.removeUnit(u)
        
        for x in s.app.animations:
            x.addTime(frameEvent.timeSinceLastFrame)
         
        self.Keyboard.capture()    
        self.Mouse.capture()    
        if self.paused:
            return True
            #if not x.hasEnded():
            #    s.app.animations.remove(x)
                
                
        
        if s.fog:
            for eunit in s.playermap["Computer1"].unitlist:
                
                bool = False
                for unit in s.playermap["Player1"].unitlist:
                    if data.util.withinRange(eunit.node.getPosition(),unit.node.getPosition(),unit.attributes.sight):
                        
                        bool = True
                        break
                if eunit.getVisible() != bool:    
                    eunit.setVisible(bool)
                    
                    if bool:
                        line = str(eunit.node.getName())+" a "+eunit.type+" arrives"
                    else:
                        line = str(eunit.node.getName())+" a "+eunit.type+" leaves"
                    #s.grammar.broadcast(line,s.playermap["Computer1"].unitlist)
                    
                    s.log(line)
#        if len(s.playermap["Computer1"].unitlist) == 0:
#            if s.turnbased:
#                s.app.setTurnbased(False)
#                
#        else:
#            if not s.turnbased:
#                s.app.setTurnbased(True)
#                
        #todo somewhat inefficient add a timeexprire variable and make straightforward
    
        for x in s.app.timedbodies:
            
        
            x.seconds -= frameEvent.timeSinceLastFrame
        
            
            if x.seconds < 0:        
                        
                
                s.app.timedbodies.remove(x)
                if isinstance(x.node, Ogre.SceneNode):
                    s.app.sceneManager.getRootSceneNode().removeChild(x.node)
                if hasattr(x.node, "destroy"):
                    getattr(x.node,"destroy")()
                
                
                       
     
                   
                     
        quat = s.app.msnCam.getOrientation()
    
        vec = Ogre.Vector3(0.0,0.0,-0.5)
        trans = quat * vec
    
        vec = Ogre.Vector3(0.5,0.0,0.0)
        strafe = quat * vec
        
        ##Need to capture/update each device - this will also trigger any listeners
        ## OIS specific !!!!
  

        ## now lets handle mouse input
        ms = self.Mouse.getMouseState()
   
        if (self.Keyboard.isKeyDown(OIS.KC_LSHIFT)):        
            rend = CEGUI.System.getSingleton().getRenderer()
            mouse = CEGUI.Point(rend.getWidth() / 2.0, rend.getHeight() / 2.0)
            s.app.msnCam.pitch( Ogre.Degree(ms.Y.rel * -0.5) )
            s.app.msnCam.yaw( Ogre.Degree(ms.X.rel * -0.5), Ogre.Node.TS_WORLD )
            CEGUI.MouseCursor.getSingleton().setPosition(mouse)
            sf.Application.debugText = str(s.app.msnCam.getPosition()) +"\n"+ str(s.app.msnCam.getOrientation())
           
        ##and Keyboard
        moveamount = frameEvent.timeSinceLastFrame * 20
        if (self.Keyboard.isKeyDown(OIS.KC_UP) or self.Keyboard.isKeyDown(OIS.KC_W)):
            
            self.msnCam.translate(trans * moveamount);
        if (self.Keyboard.isKeyDown(OIS.KC_DOWN) or self.Keyboard.isKeyDown(OIS.KC_S)):
            self.msnCam.translate(trans * -moveamount);
        if (self.Keyboard.isKeyDown(OIS.KC_LEFT) or self.Keyboard.isKeyDown(OIS.KC_A)):
            self.msnCam.translate(strafe * -moveamount);
        if (self.Keyboard.isKeyDown(OIS.KC_RIGHT) or self.Keyboard.isKeyDown(OIS.KC_D)):
            self.msnCam.translate(strafe * moveamount);
        ## now "shoot" an object!
        if (self.Keyboard.isKeyDown(OIS.KC_SPACE)):
            if (self.timer <= 0.0):

                ## we get the position and direction from the camera...
                camorient = s.app.msnCam.getOrientation()
                vec = Ogre.Vector3(0,0,-1)
                direct = camorient * vec
    
                ## then make the visual object (again a cylinder)
                #pos = Ogre.Vector3(self.msnCam.getWorldPosition())
                pos = s.app.msnCam.getPosition()
    
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
        #if (self.timer > 0.0):
        #    return True

        s.turn.doTurn()        
        self.runQueue(frameEvent.timeSinceLastFrame)
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
        self.showAttributes(name)                    
        if self.cplayer:
            self.cplayer.clickEntity(name,position)
            

    def showAttributes(self, name):
        if not s.unitmap.has_key(name):
            return
        unit = s.unitmap[name]
        winMgr = CEGUI.WindowManager.getSingleton()
        if not winMgr.isWindowPresent("attributes"):
            btn = winMgr.createWindow("TaharezLook/MultiLineEditbox", "attributes")
            sheet = CEGUI.WindowManager.getSingleton().getWindow("root_wnd")
            sheet.addChildWindow(btn)
        else:
            btn = winMgr.getWindow("attributes")
        text = "\n"+str(unit.attributes)
        #text += "\n"+str(unit.node.getPosition())    
        btn.setText(str(unit)+text)
        #btn.setPosition(CEGUI.UVector2(cegui_reldim(0.0), cegui_reldim( 0.6)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.2)))
    def showAttributesCurrent(self, name):
        if not s.unitmap.has_key(name):
            return
        unit = s.unitmap[name]
        winMgr = CEGUI.WindowManager.getSingleton()
        if not winMgr.isWindowPresent("attributes"):
            btn = winMgr.createWindow("TaharezLook/MultiLineEditbox", "attributes")
            sheet = CEGUI.WindowManager.getSingleton().getWindow("root_wnd")
            sheet.addChildWindow(btn)
        else:
            btn = winMgr.getWindow("attributes")
        text = "\n"+str(unit.attributes)
        #text += "\n"+str(unit.node.getPosition())    
        btn.setText(str(unit)+text)
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.0), cegui_reldim( 0.2)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.2)))        
        
        btn.setAlwaysOnTop(True)
                                
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
       
        #position =info.mDistance * info.mNormal + start
        
    
        if (info.mBody):
            
            bodpos, bodorient = info.mBody.getPositionOrientation()
            position = globalpt = camray.getPoint( 100.0 * info.mDistance )
            
            CEGUI.WindowManager.getSingleton().getWindow("current").setText(info.mBody.OgreNode.Name)
            self.clickEntity(info.mBody.OgreNode.Name,position)

    def keyPressed(self, evt):
       CEGUIFrameListener.keyPressed(self,evt)
       s.app.Console.keyPressed(evt)
       #print evt.key
       if OIS.KC_RETURN ==evt.key:               
           if hasattr(s.app.camera,"initialOrientation") and s.app.camera.initialOrientation:
               s.app.camera.setOrientation(s.app.camera.initialOrientation)
           s.app.camera.initialOrientation = None
           s.framelistener.paused = False
       if OIS.KC_NUMPAD5 == evt.key:
           s.screenshot()
       if OIS.KC_NUMPAD6 == evt.key:
            print sf.Application.debugText
       return True
 
    def keyReleased(self, evt):
       CEGUIFrameListener.keyReleased(self,evt)
       return True


if __name__ == '__main__':
#    try:
    application = OgreNewtonApplication()
    application.go()
#    except Ogre.OgreException, e:
#        print e
#        dir(e)
#    except:
#        import sys
#        sys.exc_info()

    
