
# 
#   OgreNewt library - connecting Ogre and Newton!i
#   Demo01_TheBasics - basic demo that shows a simple OgreNewt world, and how
#   to setup basic rigid bodies.
# 

import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt
import ogre.io.OIS as OIS
import utilities.physics 
import tactics.dotscenea 
import tactics.Turn 
import tactics.Player 
import tactics.Move 
import data.settings 
import data.aisettings 
from utilities.BasicFrameListener import *     # a simple frame listener that updates physics as required..
from utilities.CEGUIFrameListener import *
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
import ogre.gui.CEGUI as CEGUI
import random
import utilities.Console
from userinterface.MainMenu import MainMenu
from tactics.OverviewMap import *
import tactics.Unit
import tactics.TerrainManager

import tactics.Queue

class OgreNewtonApplication (sf.Application):
    
    currentmap=None
    def reset(self):
        
        self.timedbodies = []
        self.animations = []
        self.bodies=[]
        if s.turn:
            s.turn.turnlist = []
        if s.framelistener:
            s.framelistener.unitqueue.clearUnitQueue()
            s.framelistener.textlist = []
        
        for unit in s.unitmap.values():
            #removing like this because letting it be removed once there are no references
            #is far prefererable to getting the root node due to memory issues
            name =unit.name
            if s.app.sceneManager.hasSceneNode(name):
                s.app.sceneManager.destroySceneNode(name)
                unit.node = None
            #the body should dissapear upon all references going away
            unit.body = None
        if self.sceneManager:
            self.sceneManager.destroyAllMovableObjects()
            self.sceneManager.destroyAllEntities()
            
            #s.app.sceneManager.getRootSceneNode().removeAndDestroyAllChildren()
        for name in data.util.meshlist:
            print name
            if s.app.sceneManager.hasSceneNode(name):
                s.app.sceneManager.destroySceneNode(name)
        meshlist = []
        s.unitmap = dict()
        self.World.destroyAllBodies()
        
        
        
    def __init__ ( self,onStartup = None):
        sf.Application.__init__(self)
        self.World = OgreNewt.World()
        
        self.EntityCount = 0
        self.reset()
        self.materialmap=dict()
        sf.Application.debugText = "aeou"
        s.app = self
        if not onStartup:
            self.onStartup = lambda : False
        else:
            self.onStartup = onStartup

    def setupCamera(self):
        if s.app.sceneManager.hasCamera("Camera"):
            camera = s.app.sceneManager.getCamera("Camera")
        else:
            camera = s.app.sceneManager.createCamera("Camera")
        
        s.app.msnCam = s.app.sceneManager.getRootSceneNode().createChildSceneNode()
        s.app.msnCam.attachObject(s.app.camera)
        s.app.camera.setPosition(0.0, 0.0, 0.0)
        s.app.msnCam.setPosition(Ogre.Vector3(0, 25, 0))
        s.app.msnCam.setOrientation(Ogre.Quaternion(0.793987, -0.472373, 0.32888, 0.195663))


    def parseSceneFile(self,map):
        s.terrainmanager.loadTerrain(map)
        #dotscene = tactics.dotscenea.Dotscene()
        #self.sceneManager = dotscene.setup_scene(self.sceneManager, map, self)
        


    def __del__ (self):
        ## delete the world when we're done.
        #OgreNewt.Debugger.getSingleton().deInit()
        del self.bodies
        del self.World;
    
        ## de-initialize the debugger.
#        OgreNewt.Debugger.getSingleton().deInit()
        sf.Application.__del__(self)

    
    def _createScene ( self ):
        self.raySceneQuery = self.sceneManager.createRayQuery(Ogre.Ray())
        # Create all the CEGUI stuff
        self.menus = MainMenu(self.renderWindow, self.sceneManager)
#        self.initCEGUIStuff()
        
        # Create the Main Window
        
        #self.loadScene()
        data.settings.Settings()
        s.terrainmanager = tactics.TerrainManager.TerrainManager()
        
        self.setupCamera()
      #  "0.481707" y="0.212922" z="0.334251" w="0.781600"/>
        ## sky box.
        

        self.createFrame()
        OverviewMap("Terra.player")
        btn = CEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Button", "current")
        CEGUI.System.getSingleton().getGUISheet().addChildWindow(btn)
        btn.setText("current")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.6)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.1)))
        s.framelistener.setCurrentPlayer( s.overviewmap)
        self.onStartup()

    def loadScene(self,scenename, test = False):
        #scenename = "media\\scenes\\" + scenename
        self.reset()
        #data.util.clearMeshes()
        s.playermap["Computer1"] = tactics.Player.ComputerPlayer("Computer1")
        for x in s.cplayer.unitlist:
            s.unitmap[x.getName()] = x
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
        light = s.app.sceneManager.createLight( "Light1" )
        light.setType( Ogre.Light.LT_POINT )
        light.setPosition( Ogre.Vector3(0.0, 100.0, 100.0) )
        ## sky box.
        #self.sceneManager.setSkyBox(True, "Examples/CloudyNoonSkyBox")
        mental = data.aisettings.AIsettings()
        if test:
            tactics.TerrainManager.setupTest(scenename)
        if os.path.exists( "media\\scenes\\" +scenename+".scene"):
            self.parseSceneFile(scenename)
        else:
            self.parseSceneFile("begin")
            s.log("parsed begin file as did not find the regular file")
        tactics.TerrainManager.setupOnlyEvents(scenename)

        if s.event:
            s.event.start()
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
        self.frameListener = OgreNewtonFrameListener( self.renderWindow, self.camera, self.sceneManager, self.World, s.app.msnCam, self.NewtonListener )
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
                s.turn = tactics.Turn.Turn()
                s.AIon = False
            else:
                s.turn = tactics.Turn.RealTimeTurn()
                s.AIon = True
            s.log("turnbased = " +str(s.turnbased))

       
class Timed():
    def __init__(self,seconds,node,body):
        self.seconds = seconds
        self.node = node
        self.body = body
    def __str__(self):
        name = None
        if self.node:
            name = str(self.node.getName())
        return str(self.seconds)+" "+name+"\n"
        
class OgreNewtonFrameListener(CEGUIFrameListener):
    
    def __init__(self, renderWindow, camera, Mgr, World, msnCam, NewtonListener):

        CEGUIFrameListener.__init__(self, renderWindow, camera)
        #self.mouselistener = MouseListener ()
        #self.Mouse.setEventCallback(self.mouselistener)
        
        #TODO see if cegui keyboard actually works
        #OIS.KeyListener.__init__(self)
        #self.Keyboard.setEventCallback(self)
        
        self.World = World
        s.app.msnCam = msnCam
        self.camera= camera
        self.sceneManager = Mgr
        self.timer=1
        self.count=0
        self.bodies=[]
        self.basicframelistener = NewtonListener
        self.Debug = False
        self.ShutdownRequested = False
        self.paused = False
        self.interrupt = []
        self.pauseturns = True
        self.textlist = []
        self.unitqueue = tactics.Queue.Queue()
        self.backgroundqueue = tactics.Queue.Queue()



    def addTimed(self, seconds,node,*extra):
        x = Timed(seconds,node,extra)
        s.app.timedbodies.append(x)

    #then you can have both


    #turn = Turn()
    updatecamera = None
    def frameStarted(self, frameEvent):
        #fix better later todo
  
        ## in this frame listener we control the camera movement, and allow the user to "shoot" cylinders
        ## by pressing the space bar.  first the camera movement...
        #turn.runturns()
              
#        if s.ended:
#            return 
        timesincelastframe = frameEvent.timeSinceLastFrame * s.speed
        for inter in self.interrupt:
            inter.execute(timesincelastframe)
            #seems workable and easy if a bit hard to understand for others
        if len(self.interrupt):
            self.interrupt = []
            return True
        
        for u in s.unitmap.values():
            if u.text:
                u.text.update()
        for text in self.textlist:
            text.update()
        for u in s.unitmap.values():
            if u.node and u.node.getPosition().y < -100:
                s.removeUnit(u)
        
        for x in s.app.animations:
            x.addTime(timesincelastframe)
         
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
    
        tactics.Unit.incrementTimed(timesincelastframe,s.app.timedbodies)
                
                
                       
     
                   
                     
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
        moveamount = timesincelastframe * 20
        if (self.Keyboard.isKeyDown(OIS.KC_UP) or self.Keyboard.isKeyDown(OIS.KC_W)):
            
            s.app.msnCam.translate(trans * moveamount);
        if (self.Keyboard.isKeyDown(OIS.KC_DOWN) or self.Keyboard.isKeyDown(OIS.KC_S)):
            s.app.msnCam.translate(trans * -moveamount);
        if (self.Keyboard.isKeyDown(OIS.KC_LEFT) or self.Keyboard.isKeyDown(OIS.KC_A)):
            s.app.msnCam.translate(strafe * -moveamount);
        if (self.Keyboard.isKeyDown(OIS.KC_RIGHT) or self.Keyboard.isKeyDown(OIS.KC_D)):
            s.app.msnCam.translate(strafe * moveamount);
        ## now "shoot" an object!
        if (self.Keyboard.isKeyDown(OIS.KC_SPACE)):
            if (self.timer <= 0.0):

                ## we get the position and direction from the camera...
                camorient = s.app.msnCam.getOrientation()
                vec = Ogre.Vector3(0,0,-1)
                direct = camorient * vec
    
                ## then make the visual object (again a cylinder)
                #pos = Ogre.Vector3(s.app.msnCam.getWorldPosition())
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
        self.timer -= timesincelastframe
        #if (self.timer > 0.0):
        #    return True

        if not self.pauseturns:
            s.turn.doTurn()   
        
        self.unitqueue.runQueue(timesincelastframe)
        
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
        
        #btn.setAlwaysOnTop(True)
                                
    oncegui = False       
    #runningexecutes = []
    cplayer = None
    def setCurrentPlayer(self,player):
        self.cplayer = player
    def mousePressed(self, evt, id):
        if CEGUIFrameListener.mousePressed(self,evt,id):
            return
                                             

        
                
        
        name,position = data.util.fromCameraToMesh()

        CEGUI.WindowManager.getSingleton().getWindow("current").setText(name+"\n"+str(position))
        self.clickEntity(name,position)

    def keyPressed(self, evt):
       CEGUIFrameListener.keyPressed(self,evt)
       s.app.Console.keyPressed(evt)
       #print evt.key
       
       
       if OIS.KC_RETURN ==evt.key:               
           #s.framelistener.paused != s.framelistener.paused
           if hasattr(s.app.camera,"initialOrientation") and s.app.camera.initialOrientation:
              s.app.camera.setOrientation(s.app.camera.initialOrientation)
           s.app.camera.initialOrientation = None

       if OIS.KC_NUMPAD5 == evt.key:
           s.screenshot()
       if OIS.KC_NUMPAD6 == evt.key:
            print sf.Application.debugText
       return True
 
    def keyReleased(self, evt):
       CEGUIFrameListener.keyReleased(self,evt)
       return True
    def reset(self):
        #pass
        self.bodies = []

import sys
def startup():
    s.framelistener.pauseturns = False
    s.app.loadScene(sys.argv[1],True)
    pass
if __name__ == '__main__':
#    try:
        if len(sys.argv) == 1:
            startup = None
        application = OgreNewtonApplication(startup)
        application.go()
#    except Ogre.OgreException, e:
#        raise e
    #except Exception, e:
        
        #import sys
        #print sys.exc_info()
        #raise e

    
