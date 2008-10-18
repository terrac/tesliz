
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
 
s = Singleton()
class OgreNewtonApplication (sf.Application):
    
    currentmap=None
    def __init__ ( self):
        sf.Application.__init__(self)
        self.World = OgreNewt.World()
        
        self.EntityCount = 0
        self.bodies=[]
        self.timedbodies = []
        self.animations = []
        self.materialmap=dict()
        sf.Application.debugText = "aeou"

    def parseSceneFile(self):
        dotscene = Dotscene()
        self.sceneManager = dotscene.setup_scene(self.sceneManager, self.currentmap, self)


    def __del__ (self):
        ## delete the world when we're done.
        #OgreNewt.Debugger.getSingleton().deInit()
        del self.bodies
        del self.World;
    
        ## de-initialize the debugger.
#        OgreNewt.Debugger.getSingleton().deInit()
        sf.Application.__del__(self)

    
    def _createScene ( self ):
        
        
        # Play Windows exit sound.
        #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        
        # Probably play Windows default sound, if any is registered (because
        # "*" probably isn't the registered name of any sound).
    
        

        s.app = self
        Settings()
        
#        if s.turnbased:
#            Turn()
#        else:
#            RealTimeTurn()
        
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
        mental = AIsettings()
        
        self.parseSceneFile()
        
        
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
        #s.playerlist = [HumanPlayer(),ComputerPlayer()]
        
        btn = winMgr.createWindow("TaharezLook/Button", "current")
        sheet.addChildWindow(btn)
        btn.setText("current")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.6)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.036)))
        ## this will be a static object that we can throw objects at.  we'll use a simple cylinder primitive.
        ## first I load the visual mesh that represents it.  I have some simple primitive shaped .mesh files in
        ## the "primitives" directory to make this simple... all of them have a basic size of "1" so that they
        ## can easily be scaled to fit any size primitive.
        
    
        
#        for unit in s.unitmap.values():
#            self.camera.lookAt(unit.node.getPosition())
        
        


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
        self.frameListener.showDebugOverlay(False)
        
    def _configure(self):
        
        cur = self.root.restoreConfig();
        
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

    def addTimed(self, seconds,node,*extra):
        x = Timed(seconds,node,extra)
        s.app.timedbodies.append(x)

    #then you can have both
    def addToQueue(self, unit,action):

        action.running = True
        unit.actionqueue.append(action)
        if not unit in self.unitqueues:
            self.unitqueues.append(unit)
    def addToBackground(self,obj,action):
        obj.bqueue.append(action)
        self.backgroundqueue.append(obj)
         
    unitqueues = []   
    backgroundqueue = []
    def getActiveQueue(self):
        return len(self.unitqueues)

    def clearActions(self,unit):
        try:
            self.unitqueues.remove(unit)
        except:
            pass
        unit.actionqueue = []
        
            
    def isActive(self,unit):
        
        if len( unit.actionqueue):
            return True
        
                  
        return False
    a =       0
    def runQueue(self,timer):
        self.a += timer
        for unit in self.unitqueues:
            #print unit.timeleft
            #print unit
            if unit.timeleft > 0:
                unit.timeleft -= timer
                #print timer
                #print unit.timeleft
                #print unit
                #print unit.timeleft
                continue
           
            
            #print str(self.a) +" "+ str(unit)+" "+str(len(unit.actionqueue))
            #print unit.actionqueue
#            for x in self.unitqueues:
#                print x
            if len(unit.actionqueue) == 0:
                self.unitqueues.remove(unit)
                continue
            iexecute = unit.actionqueue[0]
            boo = False
            boo = iexecute.execute(timer)
            #print iexecute
            #print unit.timeleft
            if not boo:
                unit.actionqueue.pop()
                try:
                    unit.timeleft = iexecute.timeleft
                    unit.timeleft += random.random()*.1
                    
                except:
                    pass
                
                    
                    #print "removed"+str(iexecute)
                
            
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
            if u.node.getPosition().y < -50:
                u.damageHitpoints(50,"darkness")
        for x in s.app.animations:
            x.addTime(frameEvent.timeSinceLastFrame)
            if not x.getEnabled():
                s.app.remove(x)
        
        if s.fog:
            for eunit in s.playermap["Computer1"].unitlist:
                
                bool = False
                for unit in s.playermap["Player1"].unitlist:
                    if distance(eunit.node.getPosition(),unit.node.getPosition()) < unit.attributes.sight:
                        
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
                        
                try:
                    
                    s.app.sceneManager.getRootSceneNode().removeChild(x.node)
                    s.app.timedbodies.remove(x)
                except Exception, e:
                    print e
                       
     
                   
                     
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
        #if (self.timer > 0.0):
        #    return True

        s.turn.doTurn()        
        self.runQueue(frameEvent.timeSinceLastFrame)
#        for bg in self.backgroundqueue:
#            #print self.backgroundqueue
#            if len(bg.bqueue) == 0:
#                self.backgroundqueue.remove(bg)
#            for iexecute in bg.bqueue:    
#                boo = iexecute.execute(frameEvent.timeSinceLastFrame)
#                if not boo:
#                    bg.bqueue.remove(iexecute)
#                if s.turnbased:
#                    break
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
        text += "\n"+str(unit.node.getPosition())    
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
        text += "\n"+str(unit.node.getPosition())    
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

        

if __name__ == '__main__':
    try:
        application = OgreNewtonApplication()
        application.go()
    except Ogre.OgreException, e:
        print e
#    except:
#        import sys
#        sys.exc_info()

    